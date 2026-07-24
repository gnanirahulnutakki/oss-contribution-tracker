from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_tracker.py"
SPEC = importlib.util.spec_from_file_location("update_tracker", MODULE_PATH)
assert SPEC and SPEC.loader
tracker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = tracker
SPEC.loader.exec_module(tracker)


class TrackerTests(unittest.TestCase):
    def test_api_uses_owner_neutral_user_agent(self) -> None:
        class Response(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args: object) -> None:
                self.close()

        api = tracker.GitHubAPI()
        with mock.patch.object(
            tracker.urllib.request,
            "urlopen",
            return_value=Response(b'{"ok": true}'),
        ) as urlopen:
            result = api.get_json("/rate_limit")

        request = urlopen.call_args.args[0]
        self.assertEqual(result, {"ok": True})
        self.assertEqual(request.get_header("User-agent"), "oss-contribution-tracker")

    def test_api_retries_a_transient_transport_failure(self) -> None:
        class Response(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *_args: object) -> None:
                self.close()

        delays: list[float] = []
        api = tracker.GitHubAPI(max_attempts=2, sleep=delays.append)
        with mock.patch.object(
            tracker.urllib.request,
            "urlopen",
            side_effect=[
                tracker.urllib.error.URLError("temporary timeout"),
                Response(b'{"ok": true}'),
            ],
        ) as urlopen:
            result = api.get_json("/rate_limit")

        self.assertEqual(result, {"ok": True})
        self.assertEqual(urlopen.call_count, 2)
        self.assertEqual(delays, [1.0])

    def test_api_does_not_retry_a_nonretryable_http_error(self) -> None:
        error = tracker.urllib.error.HTTPError(
            "https://api.github.com/example",
            404,
            "Not Found",
            {},
            io.BytesIO(b'{"message":"Not Found"}'),
        )
        delays: list[float] = []
        api = tracker.GitHubAPI(max_attempts=3, sleep=delays.append)

        with mock.patch.object(
            tracker.urllib.request,
            "urlopen",
            side_effect=error,
        ) as urlopen:
            with self.assertRaisesRegex(RuntimeError, r"\(404\)"):
                api.get_json("/example")

        self.assertEqual(urlopen.call_count, 1)
        self.assertEqual(delays, [])

    def test_profile_queries_use_fixed_program_window(self) -> None:
        class RecordingAPI:
            def __init__(self) -> None:
                self.queries: list[str] = []

            def get_json(self, path: str, params: dict[str, object]) -> dict:
                self.queries.append(str(params["q"]))
                return {"total_count": 0, "items": []}

        api = RecordingAPI()
        profile = {
            "username": "example",
            "program_start": "2026-07-23",
            "window_days": 90,
            "excluded_owners": ["example", "employer"],
            "goals": {},
        }

        metrics = tracker.fetch_profile_metrics(api, profile, [])

        self.assertEqual(metrics["window_end"], "2026-10-20")
        self.assertTrue(all("2026-07-23..2026-10-20" in query for query in api.queries))
        self.assertTrue(all("-user:employer" in query for query in api.queries))

    def test_first_review_timestamp_ignores_pending_and_pre_program_reviews(
        self,
    ) -> None:
        reviews = [
            {
                "state": "COMMENTED",
                "submitted_at": "2026-07-22T23:59:59Z",
                "user": {"login": "example"},
            },
            {
                "state": "PENDING",
                "submitted_at": "2026-07-23T09:00:00Z",
                "user": {"login": "example"},
            },
            {
                "state": "COMMENTED",
                "submitted_at": "2026-07-23T10:00:00Z",
                "user": {"login": "other"},
            },
            {
                "state": "COMMENTED",
                "submitted_at": "2026-07-23T11:00:00Z",
                "user": {"login": "example"},
            },
            {
                "state": "APPROVED",
                "submitted_at": "2026-07-23T12:00:00Z",
                "user": {"login": "example"},
            },
        ]

        submitted_at = tracker.first_review_submitted_at(
            reviews, "example", "2026-07-23"
        )

        self.assertEqual(submitted_at, "2026-07-23T11:00:00Z")

    def test_review_cadence_waits_for_second_newest_review_to_expire(
        self,
    ) -> None:
        contributions = [
            {
                "kind": "review",
                "repository": "example/repo",
                "number": number,
                "first_review_submitted_at": submitted_at,
            }
            for number, submitted_at in enumerate(
                [
                    "2026-07-24T08:00:00Z",
                    "2026-07-24T12:00:00Z",
                    "2026-07-24T21:40:05Z",
                    "2026-07-24T22:14:25Z",
                ],
                start=1,
            )
        ]

        cadence = tracker.summarize_review_cadence(
            contributions,
            {
                "window_hours": 24,
                "max_fresh_reviews": 2,
                "min_spacing_hours": 4,
            },
            now=datetime(2026, 7, 24, 22, 55, tzinfo=UTC),
        )

        self.assertFalse(cadence["eligible_now"])
        self.assertEqual(cadence["next_eligible_at"], "2026-07-25T21:40:05Z")
        self.assertEqual(cadence["fresh_reviews_in_window"], 4)

    def test_review_cadence_spacing_can_be_the_active_boundary(self) -> None:
        cadence = tracker.summarize_review_cadence(
            [
                {
                    "kind": "review",
                    "repository": "example/repo",
                    "number": 1,
                    "first_review_submitted_at": "2026-07-24T22:00:00Z",
                }
            ],
            {
                "window_hours": 24,
                "max_fresh_reviews": 2,
                "min_spacing_hours": 4,
            },
            now=datetime(2026, 7, 24, 23, 0, tzinfo=UTC),
        )

        self.assertFalse(cadence["eligible_now"])
        self.assertEqual(cadence["next_eligible_at"], "2026-07-25T02:00:00Z")

    def test_review_cadence_ignores_explicit_exemptions(self) -> None:
        cadence = tracker.summarize_review_cadence(
            [
                {
                    "kind": "review",
                    "repository": "example/repo",
                    "number": 1,
                    "first_review_submitted_at": "2026-07-24T18:00:00Z",
                },
                {
                    "kind": "review",
                    "repository": "example/requested",
                    "number": 2,
                    "first_review_submitted_at": "2026-07-24T22:00:00Z",
                    "cadence_exempt": True,
                },
            ],
            {
                "window_hours": 24,
                "max_fresh_reviews": 2,
                "min_spacing_hours": 4,
            },
            now=datetime(2026, 7, 24, 23, 0, tzinfo=UTC),
        )

        self.assertTrue(cadence["eligible_now"])
        self.assertEqual(cadence["fresh_reviews_in_window"], 1)
        self.assertEqual(cadence["latest_fresh_review_at"], "2026-07-24T18:00:00Z")

    def test_review_cadence_renders_a_fixed_utc_boundary(self) -> None:
        rendered = tracker.render_review_cadence(
            {
                "eligible_now": False,
                "next_eligible_at": "2026-07-25T21:40:05Z",
                "window_hours": 24,
                "max_fresh_reviews": 2,
                "min_spacing_hours": 4,
            }
        )

        self.assertIn("paused until 2026-07-25 21:40 UTC", rendered)
        self.assertIn("Requested follow-ups", rendered)

    def test_summarize_checks_separates_expected_gate(self) -> None:
        checks = [
            {"name": "tests", "status": "completed", "conclusion": "success"},
            {
                "name": "check-issue-link",
                "status": "completed",
                "conclusion": "failure",
            },
            {"name": "lint", "status": "in_progress", "conclusion": None},
        ]

        summary = tracker.summarize_checks(checks, {"check-issue-link"})

        self.assertEqual(summary["passing"], 1)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["expected_gates"], ["check-issue-link"])
        self.assertEqual(summary["unexpected_failures"], [])

    def test_legacy_commit_statuses_are_counted_without_duplicates(self) -> None:
        checks = [{"name": "tests", "status": "completed", "conclusion": "success"}]
        statuses = [
            {"context": "EasyCLA", "state": "failure"},
            {"context": "tests", "state": "failure"},
        ]

        merged = tracker.merge_commit_statuses(checks, statuses)
        summary = tracker.summarize_checks(merged, {"EasyCLA"})

        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["passing"], 1)
        self.assertEqual(summary["expected_gates"], ["EasyCLA"])
        self.assertEqual(summary["unexpected_failures"], [])

    def test_workflow_authorization_failure_is_an_expected_gate(self) -> None:
        workflows = [
            {
                "name": "PR Test",
                "status": "completed",
                "conclusion": "failure",
            },
            {
                "name": "Lint",
                "status": "completed",
                "conclusion": "success",
            },
        ]

        summary = tracker.summarize_workflows(workflows, {"PR Test"})

        self.assertEqual(summary["expected_gates"], 1)
        self.assertEqual(summary["failure"], 0)
        self.assertEqual(summary["success"], 1)

    def test_assignment_gate_is_not_reported_as_rejection(self) -> None:
        entry = {"kind": "pull_request", "gate": "assignment"}
        stage = tracker.derive_stage(
            entry=entry,
            pull_request={"state": "closed", "merged_at": None},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue={"state": "open", "assignees": []},
            own_review_count=0,
            username="gnanirahulnutakki",
        )

        self.assertEqual(stage, "Awaiting assignment")

    def test_open_draft_waiting_for_assignment_is_reported(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "pull_request", "gate": "assignment"},
            pull_request={"state": "open", "merged_at": None, "draft": True},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue={"state": "open", "assignees": []},
            own_review_count=0,
            username="gnanirahulnutakki",
        )

        self.assertEqual(stage, "Awaiting assignment")

    def test_first_time_contributor_gate_is_visible(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "pull_request"},
            pull_request={"state": "open", "merged_at": None, "draft": False},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 1,
                "pending": 0,
                "success": 0,
                "failure": 0,
            },
            linked_issue=None,
            own_review_count=0,
            username="gnanirahulnutakki",
        )

        self.assertEqual(stage, "Awaiting CI approval")

    def test_review_on_current_head_is_submitted(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "review"},
            pull_request={"state": "open", "merged_at": None},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue=None,
            own_review_count=1,
            username="gnanirahulnutakki",
            own_review_on_head=True,
        )

        self.assertEqual(stage, "Review submitted")

    def test_review_on_old_head_requests_recheck(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "review"},
            pull_request={"state": "open", "merged_at": None},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue=None,
            own_review_count=1,
            username="gnanirahulnutakki",
            own_review_on_head=False,
        )

        self.assertEqual(stage, "Review update available")

    def test_thread_reply_after_latest_review_requires_attention(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[],
            review_comments=[
                {
                    "id": 10,
                    "created_at": "2026-07-24T10:00:00Z",
                    "user": {"login": "example", "type": "User"},
                },
                {
                    "id": 11,
                    "in_reply_to_id": 10,
                    "created_at": "2026-07-24T11:00:00Z",
                    "html_url": "https://example.test/reply",
                    "user": {"login": "author", "type": "User"},
                },
            ],
            reviews=[
                {
                    "state": "COMMENTED",
                    "submitted_at": "2026-07-24T10:00:00Z",
                    "user": {"login": "example", "type": "User"},
                }
            ],
            username="example",
        )

        self.assertEqual(attention["unanswered_review_thread_replies"], 1)
        self.assertEqual(attention["latest_response_url"], "https://example.test/reply")

    def test_later_own_review_clears_an_earlier_thread_reply(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[],
            review_comments=[
                {
                    "id": 10,
                    "created_at": "2026-07-24T10:00:00Z",
                    "user": {"login": "example", "type": "User"},
                },
                {
                    "id": 11,
                    "in_reply_to_id": 10,
                    "created_at": "2026-07-24T11:00:00Z",
                    "user": {"login": "author", "type": "User"},
                },
            ],
            reviews=[
                {
                    "state": "COMMENTED",
                    "submitted_at": "2026-07-24T12:00:00Z",
                    "user": {"login": "example", "type": "User"},
                }
            ],
            username="example",
        )

        self.assertEqual(attention["unanswered_review_thread_replies"], 0)

    def test_direct_mention_ignores_bots_and_requires_a_newer_comment(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[
                {
                    "created_at": "2026-07-24T09:00:00Z",
                    "body": "@example old request",
                    "user": {"login": "maintainer", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T11:00:00Z",
                    "body": "@example automated request",
                    "user": {"login": "automation[bot]", "type": "Bot"},
                },
            ],
            review_comments=[],
            reviews=[
                {
                    "state": "COMMENTED",
                    "submitted_at": "2026-07-24T10:00:00Z",
                    "user": {"login": "example", "type": "User"},
                }
            ],
            username="example",
        )

        self.assertEqual(attention["unanswered_direct_mentions"], 0)

    def test_linked_issue_response_requires_a_trusted_human_or_mention(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[],
            review_comments=[],
            reviews=[],
            username="example",
            linked_issue_floor_at="2026-07-24T10:00:00Z",
            linked_issue_comments=[
                {
                    "created_at": "2026-07-24T09:00:00Z",
                    "body": "@example old direction",
                    "author_association": "MEMBER",
                    "user": {"login": "maintainer", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T11:00:00Z",
                    "body": "general participant discussion",
                    "author_association": "NONE",
                    "user": {"login": "participant", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T12:00:00Z",
                    "body": "please update the proposed scope",
                    "author_association": "MEMBER",
                    "html_url": "https://example.test/maintainer-response",
                    "user": {"login": "maintainer", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T13:00:00Z",
                    "body": "@example can you confirm this edge case?",
                    "author_association": "NONE",
                    "html_url": "https://example.test/direct-mention",
                    "user": {"login": "participant", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T14:00:00Z",
                    "body": "@example automated reminder",
                    "author_association": "MEMBER",
                    "user": {"login": "automation[bot]", "type": "Bot"},
                },
            ],
        )

        self.assertEqual(attention["unanswered_linked_issue_responses"], 2)
        self.assertEqual(
            attention["latest_response_url"],
            "https://example.test/direct-mention",
        )

    def test_later_linked_issue_comment_clears_earlier_response(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[],
            review_comments=[],
            reviews=[],
            username="example",
            linked_issue_floor_at="2026-07-24T10:00:00Z",
            linked_issue_comments=[
                {
                    "created_at": "2026-07-24T11:00:00Z",
                    "body": "please update the proposed scope",
                    "author_association": "MEMBER",
                    "user": {"login": "maintainer", "type": "User"},
                },
                {
                    "created_at": "2026-07-24T12:00:00Z",
                    "body": "updated in the pull request",
                    "author_association": "NONE",
                    "user": {"login": "example", "type": "User"},
                },
            ],
        )

        self.assertEqual(attention["unanswered_linked_issue_responses"], 0)
        self.assertEqual(
            attention["linked_issue_latest_own_activity_at"],
            "2026-07-24T12:00:00Z",
        )

    def test_closed_assignment_gate_surfaces_linked_issue_response(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "pull_request", "gate": "assignment"},
            pull_request={"state": "closed", "merged_at": None},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue={"state": "open", "assignees": []},
            own_review_count=0,
            username="example",
            attention={"unanswered_linked_issue_responses": 1},
        )

        self.assertEqual(stage, "Maintainer response")

    def test_change_request_survives_comments_until_approval(self) -> None:
        base_reviews = [
            {
                "state": "CHANGES_REQUESTED",
                "submitted_at": "2026-07-24T09:00:00Z",
                "user": {"login": "maintainer", "type": "User"},
            },
            {
                "state": "COMMENTED",
                "submitted_at": "2026-07-24T10:00:00Z",
                "user": {"login": "maintainer", "type": "User"},
            },
        ]

        requested = tracker.summarize_attention([], [], base_reviews, "example")
        approved = tracker.summarize_attention(
            [],
            [],
            [
                *base_reviews,
                {
                    "state": "APPROVED",
                    "submitted_at": "2026-07-24T11:00:00Z",
                    "user": {"login": "maintainer", "type": "User"},
                },
            ],
            "example",
        )

        self.assertEqual(requested["changes_requested_by"], ["maintainer"])
        self.assertEqual(approved["changes_requested_by"], [])

    def test_response_available_stage_requires_current_head_review(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "review"},
            pull_request={"state": "open", "merged_at": None},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 0,
                "pending": 0,
                "success": 1,
                "failure": 0,
            },
            linked_issue=None,
            own_review_count=1,
            username="example",
            own_review_on_head=True,
            attention={
                "unanswered_direct_mentions": 0,
                "unanswered_review_thread_replies": 1,
            },
        )

        self.assertEqual(stage, "Response available")

    def test_change_request_takes_priority_for_authored_pr(self) -> None:
        stage = tracker.derive_stage(
            entry={"kind": "pull_request"},
            pull_request={"state": "open", "merged_at": None, "draft": False},
            checks={"pending": 0, "unexpected_failures": []},
            workflows={
                "action_required": 1,
                "pending": 0,
                "success": 0,
                "failure": 0,
            },
            linked_issue=None,
            own_review_count=0,
            username="example",
            attention={"changes_requested_by": ["maintainer"]},
        )

        self.assertEqual(stage, "Changes requested")

    def test_external_review_change_request_is_not_our_action(self) -> None:
        attention = tracker.summarize_attention(
            issue_comments=[],
            review_comments=[],
            reviews=[
                {
                    "state": "CHANGES_REQUESTED",
                    "submitted_at": "2026-07-24T09:00:00Z",
                    "user": {"login": "maintainer", "type": "User"},
                }
            ],
            username="example",
            include_change_requests=False,
        )

        self.assertEqual(attention["changes_requested_by"], [])

    def test_stable_snapshot_preserves_timestamp_on_noop(self) -> None:
        current = {"profile": {"merged": 1}, "contributions": []}
        previous = {
            **current,
            "state_changed_at": "2026-07-23T12:00:00+00:00",
        }

        result = tracker.stabilize_snapshot(
            current,
            previous,
            now=datetime(2026, 7, 24, 12, 0, tzinfo=UTC),
        )

        self.assertEqual(result["state_changed_at"], "2026-07-23T12:00:00+00:00")

    def test_stable_snapshot_ignores_bot_only_pull_request_timestamp_churn(
        self,
    ) -> None:
        current = {
            "profile": {"merged": 1},
            "contributions": [
                {
                    "id": "example-pr",
                    "head_sha": "abc123",
                    "stage": "PR open",
                    "updated_at": "2026-07-24T13:00:00Z",
                }
            ],
        }
        previous = {
            "profile": {"merged": 1},
            "contributions": [
                {
                    "id": "example-pr",
                    "head_sha": "abc123",
                    "stage": "PR open",
                    "updated_at": "2026-07-24T12:00:00Z",
                }
            ],
            "state_changed_at": "2026-07-24T12:00:00+00:00",
        }

        result = tracker.stabilize_snapshot(
            current,
            previous,
            now=datetime(2026, 7, 24, 13, 0, tzinfo=UTC),
        )

        self.assertEqual(
            result["contributions"][0]["updated_at"], "2026-07-24T12:00:00Z"
        )
        self.assertEqual(result["state_changed_at"], "2026-07-24T12:00:00+00:00")
        self.assertEqual(
            current["contributions"][0]["updated_at"], "2026-07-24T13:00:00Z"
        )

    def test_stable_snapshot_keeps_timestamp_for_material_pull_request_change(
        self,
    ) -> None:
        current = {
            "profile": {"merged": 1},
            "contributions": [
                {
                    "id": "example-pr",
                    "head_sha": "def456",
                    "stage": "PR open",
                    "updated_at": "2026-07-24T13:00:00Z",
                }
            ],
        }
        previous = {
            "profile": {"merged": 1},
            "contributions": [
                {
                    "id": "example-pr",
                    "head_sha": "abc123",
                    "stage": "PR open",
                    "updated_at": "2026-07-24T12:00:00Z",
                }
            ],
            "state_changed_at": "2026-07-24T12:00:00+00:00",
        }

        result = tracker.stabilize_snapshot(
            current,
            previous,
            now=datetime(2026, 7, 24, 13, 0, tzinfo=UTC),
        )

        self.assertEqual(
            result["contributions"][0]["updated_at"], "2026-07-24T13:00:00Z"
        )
        self.assertEqual(result["state_changed_at"], "2026-07-24T13:00:00+00:00")

    def test_marker_replacement_preserves_static_readme(self) -> None:
        original = (
            "# Header\n\n"
            f"{tracker.START_MARKER}\nold\n{tracker.END_MARKER}\n\n"
            "## Static\n"
        )

        result = tracker.replace_generated_section(original, "new")

        self.assertIn(f"{tracker.START_MARKER}\nnew\n{tracker.END_MARKER}", result)
        self.assertTrue(result.endswith("## Static\n"))

    def test_config_rejects_duplicate_ids(self) -> None:
        config = {
            "schema_version": 1,
            "profile": {
                "username": "example",
                "program_start": "2026-07-23",
                "window_days": 90,
                "excluded_owners": ["example"],
                "goals": {},
            },
            "contributions": [
                {
                    "id": "same",
                    "kind": "review",
                    "repository": "owner/repo",
                    "number": 1,
                    "started_at": "2026-07-23",
                    "next_action": "wait",
                },
                {
                    "id": "same",
                    "kind": "review",
                    "repository": "owner/repo",
                    "number": 2,
                    "started_at": "2026-07-23",
                    "next_action": "wait",
                },
            ],
        }

        with self.assertRaisesRegex(ValueError, "duplicate contribution id"):
            tracker.validate_config(config)

    def test_config_rejects_unknown_review_cadence_fields(self) -> None:
        config = {
            "schema_version": 1,
            "profile": {
                "username": "example",
                "program_start": "2026-07-23",
                "window_days": 90,
                "review_cadence": {"daily_limit": 2},
                "excluded_owners": ["example"],
                "goals": {},
            },
            "contributions": [],
        }

        with self.assertRaisesRegex(ValueError, "unknown fields: daily_limit"):
            tracker.validate_config(config)


if __name__ == "__main__":
    unittest.main()
