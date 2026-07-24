from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "update_tracker.py"
SPEC = importlib.util.spec_from_file_location("update_tracker", MODULE_PATH)
assert SPEC and SPEC.loader
tracker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = tracker
SPEC.loader.exec_module(tracker)


class TrackerTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
