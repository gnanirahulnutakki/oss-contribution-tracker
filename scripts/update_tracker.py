#!/usr/bin/env python3
"""Refresh the public contribution dashboard from GitHub's REST API."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from copy import deepcopy
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

API_ROOT = "https://api.github.com"
USER_AGENT = "oss-contribution-tracker"
START_MARKER = "<!-- TRACKER:START -->"
END_MARKER = "<!-- TRACKER:END -->"
NON_FAILING_CONCLUSIONS = {"success", "neutral", "skipped"}
FAILING_CONCLUSIONS = {
    "failure",
    "timed_out",
    "cancelled",
    "action_required",
    "stale",
    "startup_failure",
}
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}
TRUSTED_AUTHOR_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
DEFAULT_REVIEW_CADENCE = {
    "window_hours": 24,
    "max_fresh_reviews": 2,
    "min_spacing_hours": 4,
}


class GitHubAPI:
    """Small standard-library GitHub API client for public repository data."""

    def __init__(
        self,
        token: str | None = None,
        *,
        max_attempts: int = 3,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.token = token
        self.max_attempts = max_attempts
        self.sleep = sleep

    @staticmethod
    def _retry_delay(error: urllib.error.HTTPError, attempt: int) -> float:
        retry_after = error.headers.get("Retry-After") if error.headers else None
        try:
            return min(float(retry_after), 30.0) if retry_after else 2.0**attempt
        except ValueError:
            return 2.0**attempt

    def get_json(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | list[dict[str, Any]]:
        url = path if path.startswith("https://") else f"{API_ROOT}{path}"
        if params:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}{urllib.parse.urlencode(params)}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(url, headers=headers)
        for attempt in range(self.max_attempts):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as error:
                retry_after = (
                    error.headers.get("Retry-After") if error.headers else None
                )
                retryable = error.code in RETRYABLE_HTTP_CODES or (
                    error.code == 403 and retry_after is not None
                )
                if retryable and attempt + 1 < self.max_attempts:
                    self.sleep(self._retry_delay(error, attempt))
                    continue
                detail = error.read(500).decode("utf-8", errors="replace")
                raise RuntimeError(
                    f"GitHub API request failed ({error.code}) for {url}: {detail}"
                ) from error
            except (urllib.error.URLError, TimeoutError) as error:
                if attempt + 1 < self.max_attempts:
                    self.sleep(2.0**attempt)
                    continue
                raise RuntimeError(
                    f"GitHub API request failed for {url}: {error}"
                ) from error
        raise AssertionError("unreachable")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def resolve_review_cadence(profile: dict[str, Any]) -> dict[str, int]:
    raw = profile.get("review_cadence", {})
    if not isinstance(raw, dict):
        raise ValueError("profile.review_cadence must be an object")
    unknown = set(raw) - set(DEFAULT_REVIEW_CADENCE)
    if unknown:
        raise ValueError(
            "profile.review_cadence has unknown fields: " + ", ".join(sorted(unknown))
        )
    cadence = {**DEFAULT_REVIEW_CADENCE, **raw}
    for field, value in cadence.items():
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(
                f"profile.review_cadence.{field} must be a positive integer"
            )
    return cadence


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")

    profile = config.get("profile")
    if not isinstance(profile, dict) or not profile.get("username"):
        raise ValueError("profile.username is required")
    try:
        date.fromisoformat(profile.get("program_start", ""))
    except (TypeError, ValueError) as error:
        raise ValueError("profile.program_start must use YYYY-MM-DD") from error
    if not isinstance(profile.get("window_days"), int) or profile["window_days"] <= 0:
        raise ValueError("profile.window_days must be a positive integer")
    excluded_owners = profile.get("excluded_owners")
    if (
        not isinstance(excluded_owners, list)
        or not excluded_owners
        or any(not isinstance(owner, str) or not owner for owner in excluded_owners)
    ):
        raise ValueError("profile.excluded_owners must be a non-empty string list")
    if not isinstance(profile.get("goals"), dict):
        raise ValueError("profile.goals is required")
    resolve_review_cadence(profile)

    contributions = config.get("contributions")
    if not isinstance(contributions, list):
        raise ValueError("contributions must be a list")

    seen: set[str] = set()
    for index, entry in enumerate(contributions):
        prefix = f"contributions[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{prefix} must be an object")
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            raise ValueError(f"{prefix}.id is required")
        if entry_id in seen:
            raise ValueError(f"duplicate contribution id: {entry_id}")
        seen.add(entry_id)
        if entry.get("kind") not in {"pull_request", "review", "issue"}:
            raise ValueError(f"{prefix}.kind must be pull_request, review, or issue")
        if "cadence_exempt" in entry and (
            entry["kind"] != "review" or not isinstance(entry["cadence_exempt"], bool)
        ):
            raise ValueError(
                f"{prefix}.cadence_exempt must be a boolean on a review entry"
            )
        attention_acknowledged_at = entry.get("attention_acknowledged_at")
        if attention_acknowledged_at is not None:
            if not isinstance(attention_acknowledged_at, str):
                raise ValueError(
                    f"{prefix}.attention_acknowledged_at must be a timestamp string"
                )
            try:
                _parse_timestamp(attention_acknowledged_at)
            except ValueError as error:
                raise ValueError(
                    f"{prefix}.attention_acknowledged_at must be a "
                    "timezone-aware timestamp"
                ) from error
        repository = entry.get("repository")
        if (
            not isinstance(repository, str)
            or repository.count("/") != 1
            or any(not part for part in repository.split("/"))
        ):
            raise ValueError(f"{prefix}.repository must use owner/name")
        if not isinstance(entry.get("number"), int) or entry["number"] <= 0:
            raise ValueError(f"{prefix}.number must be a positive integer")
        try:
            date.fromisoformat(entry.get("started_at", ""))
        except (TypeError, ValueError) as error:
            raise ValueError(f"{prefix}.started_at must use YYYY-MM-DD") from error
        if not isinstance(entry.get("next_action"), str) or not entry["next_action"]:
            raise ValueError(f"{prefix}.next_action is required")


def summarize_checks(
    check_runs: list[dict[str, Any]], expected_failures: set[str]
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "total": len(check_runs),
        "passing": 0,
        "successful": 0,
        "non_failing": 0,
        "skipped": 0,
        "neutral": 0,
        "pending": 0,
        "expected_gates": [],
        "unexpected_failures": [],
    }
    for check in check_runs:
        name = str(check.get("name", "unnamed check"))
        if check.get("status") != "completed":
            summary["pending"] += 1
            continue
        conclusion = check.get("conclusion")
        if conclusion in NON_FAILING_CONCLUSIONS:
            # `passing` is a legacy public snapshot field that historically
            # included successful, skipped, and neutral checks.
            summary["passing"] += 1
            summary["non_failing"] += 1
            if conclusion == "success":
                summary["successful"] += 1
            elif conclusion == "skipped":
                summary["skipped"] += 1
            else:
                summary["neutral"] += 1
        elif name in expected_failures:
            summary["expected_gates"].append(name)
        elif conclusion in FAILING_CONCLUSIONS or conclusion is None:
            summary["unexpected_failures"].append(name)
    return summary


def merge_commit_statuses(
    check_runs: list[dict[str, Any]], commit_statuses: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Add legacy commit statuses without double-counting named check runs."""
    merged = list(check_runs)
    seen_names = {str(check.get("name", "")) for check in check_runs}
    for commit_status in commit_statuses:
        name = str(commit_status.get("context", "unnamed status"))
        if name in seen_names:
            continue
        state = commit_status.get("state")
        if state == "pending":
            status = "in_progress"
            conclusion = None
        else:
            status = "completed"
            conclusion = "success" if state == "success" else "failure"
        merged.append(
            {
                "name": name,
                "status": status,
                "conclusion": conclusion,
            }
        )
        seen_names.add(name)
    return merged


def summarize_workflows(
    runs: list[dict[str, Any]], expected_failures: set[str] | None = None
) -> dict[str, int]:
    expected_failures = expected_failures or set()
    summary = {
        "action_required": 0,
        "expected_gates": 0,
        "pending": 0,
        "success": 0,
        "failure": 0,
    }
    for run in runs:
        if run.get("status") != "completed":
            summary["pending"] += 1
        elif run.get("conclusion") == "action_required":
            summary["action_required"] += 1
        elif run.get("conclusion") == "success":
            summary["success"] += 1
        elif (
            run.get("conclusion") == "failure"
            and str(run.get("name", "")) in expected_failures
        ):
            summary["expected_gates"] += 1
        elif run.get("conclusion") not in {"skipped", "neutral"}:
            summary["failure"] += 1
    return summary


def summarize_base_drift(
    pull_request: dict[str, Any], comparison: dict[str, Any]
) -> dict[str, bool]:
    """Bucket base drift without recording a noisy per-commit counter."""
    behind_by = comparison.get("behind_by")
    if not isinstance(behind_by, int) or isinstance(behind_by, bool):
        raise ValueError("GitHub comparison response must include integer behind_by")
    behind = behind_by > 0
    return {
        "behind": behind,
        "update_required": behind and pull_request.get("mergeable_state") == "behind",
    }


def fetch_live_base_sha(
    api: GitHubAPI, repository: str, pull_request: dict[str, Any]
) -> str:
    """Resolve the current target-branch tip instead of the PR's embedded base."""
    base_ref = pull_request.get("base", {}).get("ref")
    if not isinstance(base_ref, str) or not base_ref:
        raise RuntimeError("Open pull request is missing its base ref")
    encoded_ref = urllib.parse.quote(base_ref, safe="")
    response = api.get_json(f"/repos/{repository}/commits/{encoded_ref}")
    if not isinstance(response, dict) or not isinstance(response.get("sha"), str):
        raise RuntimeError(f"Unexpected live base response for {repository}:{base_ref}")
    return response["sha"]


def _login(item: dict[str, Any]) -> str:
    user = item.get("user")
    if not isinstance(user, dict):
        return ""
    return str(user.get("login") or "")


def _is_other_human(item: dict[str, Any], username: str) -> bool:
    user = item.get("user")
    if not isinstance(user, dict):
        return False
    login = _login(item)
    return bool(
        login
        and login.casefold() != username.casefold()
        and user.get("type") != "Bot"
        and not login.casefold().endswith("[bot]")
    )


def _latest_timestamp(values: list[str | None]) -> str | None:
    timestamps = [value for value in values if value]
    return max(timestamps) if timestamps else None


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"invalid GitHub timestamp: {value}") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"GitHub timestamp must include a timezone: {value}")
    return parsed.astimezone(UTC)


def _format_timestamp(value: datetime) -> str:
    return (
        value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )


def first_review_submitted_at(
    reviews: list[dict[str, Any]], username: str, started_at: str
) -> str | None:
    floor = _parse_timestamp(f"{started_at}T00:00:00Z")
    timestamps = [
        str(review["submitted_at"])
        for review in reviews
        if _login(review).casefold() == username.casefold()
        and review.get("state") != "PENDING"
        and review.get("submitted_at")
        and _parse_timestamp(str(review["submitted_at"])) >= floor
    ]
    return min(timestamps, key=_parse_timestamp) if timestamps else None


def _response_count(attention: dict[str, Any]) -> int:
    return sum(
        int(attention.get(key, 0))
        for key in (
            "unanswered_direct_mentions",
            "unanswered_review_thread_replies",
            "unanswered_linked_issue_responses",
        )
    )


def summarize_attention(
    issue_comments: list[dict[str, Any]],
    review_comments: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
    username: str,
    *,
    include_change_requests: bool = True,
    linked_issue_comments: list[dict[str, Any]] | None = None,
    linked_issue_floor_at: str | None = None,
    attention_acknowledged_at: str | None = None,
) -> dict[str, Any]:
    """Find high-confidence public activity that still needs a response."""
    linked_issue_comments = linked_issue_comments or []
    own_activity_at = _latest_timestamp(
        [
            *[
                comment.get("created_at")
                for comment in issue_comments
                if _login(comment).casefold() == username.casefold()
            ],
            *[
                comment.get("created_at")
                for comment in review_comments
                if _login(comment).casefold() == username.casefold()
            ],
            *[
                review.get("submitted_at")
                for review in reviews
                if _login(review).casefold() == username.casefold()
                and review.get("state") != "PENDING"
            ],
        ]
    )
    attention_floor_at = _latest_timestamp(
        [own_activity_at, attention_acknowledged_at]
    )

    own_thread_roots = {
        comment.get("in_reply_to_id") or comment.get("id")
        for comment in review_comments
        if _login(comment).casefold() == username.casefold()
    }
    thread_replies = [
        comment
        for comment in review_comments
        if _is_other_human(comment, username)
        and comment.get("in_reply_to_id") in own_thread_roots
        and (
            attention_floor_at is None
            or (comment.get("created_at") or "") > attention_floor_at
        )
    ]

    mention_pattern = re.compile(
        rf"(?<![\w-])@{re.escape(username)}(?![\w-])",
        flags=re.IGNORECASE,
    )
    direct_mentions = [
        comment
        for comment in issue_comments
        if _is_other_human(comment, username)
        and mention_pattern.search(str(comment.get("body") or ""))
        and (
            attention_floor_at is None
            or (comment.get("created_at") or "") > attention_floor_at
        )
    ]

    linked_issue_own_activity_at = _latest_timestamp(
        [
            comment.get("created_at")
            for comment in linked_issue_comments
            if _login(comment).casefold() == username.casefold()
        ]
    )
    linked_issue_response_floor = _latest_timestamp(
        [
            linked_issue_floor_at,
            linked_issue_own_activity_at,
            attention_acknowledged_at,
        ]
    )
    linked_issue_responses = [
        comment
        for comment in linked_issue_comments
        if _is_other_human(comment, username)
        and (
            comment.get("author_association") in TRUSTED_AUTHOR_ASSOCIATIONS
            or mention_pattern.search(str(comment.get("body") or ""))
        )
        and (
            linked_issue_response_floor is None
            or (comment.get("created_at") or "") > linked_issue_response_floor
        )
    ]

    active_change_requests: set[str] = set()
    ordered_reviews = sorted(
        (
            review
            for review in reviews
            if _is_other_human(review, username) and review.get("state") != "PENDING"
        ),
        key=lambda review: str(review.get("submitted_at") or ""),
    )
    for review in ordered_reviews:
        login = _login(review)
        state = review.get("state")
        if state == "CHANGES_REQUESTED":
            active_change_requests.add(login)
        elif state in {"APPROVED", "DISMISSED"}:
            active_change_requests.discard(login)

    response_candidates = [
        *thread_replies,
        *direct_mentions,
        *linked_issue_responses,
    ]
    latest_response = max(
        response_candidates,
        key=lambda item: str(item.get("created_at") or ""),
        default=None,
    )
    return {
        **(
            {"acknowledged_at": attention_acknowledged_at}
            if attention_acknowledged_at
            else {}
        ),
        "changes_requested_by": (
            sorted(active_change_requests) if include_change_requests else []
        ),
        "latest_own_activity_at": own_activity_at,
        "linked_issue_latest_own_activity_at": linked_issue_own_activity_at,
        "latest_response_at": (
            latest_response.get("created_at") if latest_response else None
        ),
        "latest_response_url": (
            latest_response.get("html_url") if latest_response else None
        ),
        "unanswered_direct_mentions": len(direct_mentions),
        "unanswered_linked_issue_responses": len(linked_issue_responses),
        "unanswered_review_thread_replies": len(thread_replies),
    }


def derive_stage(
    entry: dict[str, Any],
    pull_request: dict[str, Any],
    checks: dict[str, Any],
    workflows: dict[str, int],
    linked_issue: dict[str, Any] | None,
    own_review_count: int,
    username: str,
    own_review_on_head: bool = False,
    attention: dict[str, Any] | None = None,
    base_drift: dict[str, bool] | None = None,
) -> str:
    attention = attention or {}
    base_drift = base_drift or {}
    response_count = _response_count(attention)
    if pull_request.get("merged_at"):
        return "Review landed" if entry["kind"] == "review" else "Merged"

    if entry["kind"] == "review":
        if own_review_count:
            if pull_request.get("state") != "open":
                return "Review complete"
            if not own_review_on_head:
                return "Review update available"
            if response_count:
                return "Response available"
            return "Review submitted"
        return "Review not found"

    if pull_request.get("state") == "open" and attention.get("changes_requested_by"):
        return "Changes requested"
    if response_count:
        return "Maintainer response"

    if pull_request.get("state") == "open":
        if workflows["action_required"]:
            return "Awaiting CI approval"
        if checks["unexpected_failures"] or workflows["failure"]:
            return "CI failing"
        if checks["pending"] or workflows["pending"]:
            return "CI running"
        if entry.get("gate") == "assignment" and linked_issue:
            assignees = {
                assignee.get("login")
                for assignee in linked_issue.get("assignees", [])
                if isinstance(assignee, dict)
            }
            if linked_issue.get("state") == "open" and username not in assignees:
                return "Awaiting assignment"
        if not pull_request.get("draft") and base_drift.get("update_required"):
            return "Branch update required"
        return "Draft" if pull_request.get("draft") else "PR open"

    if entry.get("gate") == "assignment" and linked_issue:
        assignees = {
            assignee.get("login")
            for assignee in linked_issue.get("assignees", [])
            if isinstance(assignee, dict)
        }
        if linked_issue.get("state") == "open" and username not in assignees:
            return "Awaiting assignment"
    return "Closed"


def derive_issue_stage(
    issue: dict[str, Any],
    attention: dict[str, Any],
    username: str,
) -> str:
    if issue.get("state") != "open":
        return "Issue closed"
    if _response_count(attention):
        return "Maintainer response"

    assignees = {
        str(assignee.get("login")).casefold()
        for assignee in issue.get("assignees", [])
        if isinstance(assignee, dict) and assignee.get("login")
    }
    if username.casefold() in assignees:
        return "Assigned"
    if assignees:
        return "Assigned elsewhere"
    return "Issue open"


def fetch_issue_contribution(
    api: GitHubAPI,
    entry: dict[str, Any],
    username: str,
) -> dict[str, Any]:
    repository = entry["repository"]
    number = entry["number"]
    issue = api.get_json(f"/repos/{repository}/issues/{number}")
    if not isinstance(issue, dict) or "pull_request" in issue:
        raise RuntimeError(f"Unexpected issue response for {repository}#{number}")

    issue_comments = api.get_json(
        f"/repos/{repository}/issues/{number}/comments",
        {"per_page": 100},
    )
    if not isinstance(issue_comments, list):
        raise RuntimeError(
            f"Unexpected issue comment response for {repository}#{number}"
        )

    attention = summarize_attention(
        issue_comments=[],
        review_comments=[],
        reviews=[],
        username=username,
        include_change_requests=False,
        linked_issue_comments=issue_comments,
        linked_issue_floor_at=issue.get("created_at"),
        attention_acknowledged_at=entry.get("attention_acknowledged_at"),
    )
    assignees = [
        assignee.get("login")
        for assignee in issue.get("assignees", [])
        if isinstance(assignee, dict) and assignee.get("login")
    ]
    return {
        "attention": attention,
        "assignees": assignees,
        "checks": {
            "total": 0,
            "passing": 0,
            "successful": 0,
            "non_failing": 0,
            "skipped": 0,
            "neutral": 0,
            "pending": 0,
            "expected_gates": [],
            "unexpected_failures": [],
        },
        "draft": False,
        "exclude_from_landing_rate": False,
        "first_review_submitted_at": None,
        "id": entry["id"],
        "kind": entry["kind"],
        "linked_issue": None,
        "merged_at": None,
        "next_action": entry["next_action"],
        "number": number,
        "own_review_count": 0,
        "own_review_on_head": False,
        "repository": repository,
        "review_url": None,
        "role": entry["role"],
        "stage": derive_issue_stage(issue, attention, username),
        "started_at": entry["started_at"],
        "state": issue["state"],
        "tier": entry["tier"],
        "title": issue["title"],
        "updated_at": issue["updated_at"],
        "url": issue["html_url"],
        "workflows": {
            "action_required": 0,
            "expected_gates": 0,
            "failure": 0,
            "pending": 0,
            "success": 0,
        },
    }


def fetch_contribution(
    api: GitHubAPI, entry: dict[str, Any], username: str
) -> dict[str, Any]:
    if entry["kind"] == "issue":
        return fetch_issue_contribution(api, entry, username)

    repository = entry["repository"]
    number = entry["number"]
    pull_request = api.get_json(f"/repos/{repository}/pulls/{number}")
    if not isinstance(pull_request, dict):
        raise RuntimeError(
            f"Unexpected pull request response for {repository}#{number}"
        )

    head_sha = pull_request["head"]["sha"]
    check_response = api.get_json(
        f"/repos/{repository}/commits/{head_sha}/check-runs",
        {"per_page": 100},
    )
    if not isinstance(check_response, dict):
        raise RuntimeError(f"Unexpected check response for {repository}#{number}")
    commit_status_response = api.get_json(
        f"/repos/{repository}/commits/{head_sha}/status", {"per_page": 100}
    )
    if not isinstance(commit_status_response, dict):
        raise RuntimeError(
            f"Unexpected commit status response for {repository}#{number}"
        )
    checks = summarize_checks(
        merge_commit_statuses(
            check_response.get("check_runs", []),
            commit_status_response.get("statuses", []),
        ),
        set(entry.get("expected_check_failures", [])),
    )

    workflow_response = api.get_json(
        f"/repos/{repository}/actions/runs",
        {"head_sha": head_sha, "event": "pull_request", "per_page": 100},
    )
    if not isinstance(workflow_response, dict):
        raise RuntimeError(f"Unexpected workflow response for {repository}#{number}")
    workflows = summarize_workflows(
        workflow_response.get("workflow_runs", []),
        set(entry.get("expected_workflow_failures", [])),
    )

    base_drift: dict[str, bool] | None = None
    if entry["kind"] == "pull_request" and pull_request.get("state") == "open":
        base_sha = fetch_live_base_sha(api, repository, pull_request)
        comparison_response = api.get_json(
            f"/repos/{repository}/compare/{base_sha}...{head_sha}"
        )
        if not isinstance(comparison_response, dict):
            raise RuntimeError(
                f"Unexpected comparison response for {repository}#{number}"
            )
        base_drift = summarize_base_drift(pull_request, comparison_response)

    linked_issue: dict[str, Any] | None = None
    linked_issue_comments: list[dict[str, Any]] = []
    if entry.get("linked_issue"):
        issue_response = api.get_json(
            f"/repos/{repository}/issues/{entry['linked_issue']}"
        )
        if isinstance(issue_response, dict):
            linked_issue = issue_response
        if entry["kind"] == "pull_request":
            linked_issue_comment_response = api.get_json(
                f"/repos/{repository}/issues/{entry['linked_issue']}/comments",
                {"per_page": 100},
            )
            if not isinstance(linked_issue_comment_response, list):
                raise RuntimeError(
                    "Unexpected linked issue comment response for "
                    f"{repository}#{entry['linked_issue']}"
                )
            linked_issue_comments = linked_issue_comment_response

    reviews = api.get_json(
        f"/repos/{repository}/pulls/{number}/reviews", {"per_page": 100}
    )
    if not isinstance(reviews, list):
        raise RuntimeError(f"Unexpected reviews response for {repository}#{number}")
    issue_comments = api.get_json(
        f"/repos/{repository}/issues/{number}/comments", {"per_page": 100}
    )
    if not isinstance(issue_comments, list):
        raise RuntimeError(
            f"Unexpected issue comment response for {repository}#{number}"
        )
    review_comments = api.get_json(
        f"/repos/{repository}/pulls/{number}/comments", {"per_page": 100}
    )
    if not isinstance(review_comments, list):
        raise RuntimeError(
            f"Unexpected review comment response for {repository}#{number}"
        )
    attention = summarize_attention(
        issue_comments,
        review_comments,
        reviews,
        username,
        include_change_requests=entry["kind"] == "pull_request",
        linked_issue_comments=linked_issue_comments,
        linked_issue_floor_at=pull_request.get("created_at"),
        attention_acknowledged_at=entry.get("attention_acknowledged_at"),
    )

    own_review_count = 0
    own_review_on_head = False
    first_review_at: str | None = None
    if entry["kind"] == "review":
        own_reviews = [
            review
            for review in reviews
            if review.get("user", {}).get("login") == username
            and review.get("state") != "PENDING"
        ]
        own_review_count = len(own_reviews)
        own_review_on_head = any(
            review.get("commit_id") == head_sha for review in own_reviews
        )
        first_review_at = first_review_submitted_at(
            own_reviews, username, entry["started_at"]
        )

    stage = derive_stage(
        entry,
        pull_request,
        checks,
        workflows,
        linked_issue,
        own_review_count,
        username,
        own_review_on_head,
        attention,
        base_drift,
    )
    return {
        "attention": attention,
        **({"base_drift": base_drift} if base_drift is not None else {}),
        "draft": bool(pull_request.get("draft")),
        "head_sha": head_sha,
        "id": entry["id"],
        "kind": entry["kind"],
        "repository": repository,
        "number": number,
        "title": pull_request["title"],
        "url": pull_request["html_url"],
        "role": entry["role"],
        "tier": entry["tier"],
        "started_at": entry["started_at"],
        "stage": stage,
        "state": pull_request["state"],
        "merged_at": pull_request.get("merged_at"),
        "updated_at": pull_request["updated_at"],
        "checks": checks,
        "workflows": workflows,
        "linked_issue": (
            {
                "number": entry["linked_issue"],
                "state": linked_issue.get("state"),
                "assignees": [
                    assignee.get("login")
                    for assignee in linked_issue.get("assignees", [])
                ],
            }
            if linked_issue
            else None
        ),
        "review_url": entry.get("review_url"),
        "own_review_count": own_review_count,
        "own_review_on_head": own_review_on_head,
        "first_review_submitted_at": first_review_at,
        "cadence_exempt": bool(entry.get("cadence_exempt", False)),
        "next_action": entry["next_action"],
        "exclude_from_landing_rate": bool(
            entry.get("exclude_from_landing_rate", False)
        ),
    }


def search_issues(
    api: GitHubAPI, query: str, *, collect_items: bool = False
) -> tuple[int, list[dict[str, Any]]]:
    items: list[dict[str, Any]] = []
    page = 1
    total = 0
    while True:
        response = api.get_json(
            "/search/issues",
            {"q": query, "per_page": 100, "page": page},
        )
        if not isinstance(response, dict):
            raise RuntimeError("Unexpected GitHub search response")
        total = int(response.get("total_count", 0))
        page_items = response.get("items", [])
        if collect_items:
            items.extend(page_items)
        if not collect_items or len(page_items) < 100 or page >= 10:
            break
        page += 1
    return total, items


def fetch_profile_metrics(
    api: GitHubAPI,
    profile: dict[str, Any],
    contributions: list[dict[str, Any]],
) -> dict[str, Any]:
    username = profile["username"]
    window_start = date.fromisoformat(profile["program_start"])
    window_end = window_start + timedelta(days=profile["window_days"] - 1)
    since = window_start.isoformat()
    until = window_end.isoformat()
    program_range = f"{since}..{until}"
    external = " ".join(f"-user:{owner}" for owner in profile["excluded_owners"])
    prefix = f"is:pr author:{username} {external}"

    authored, _ = search_issues(api, f"{prefix} created:{program_range}")
    merged, _ = search_issues(
        api,
        (f"{prefix} is:merged created:{program_range} merged:{program_range}"),
    )
    open_prs, _ = search_issues(api, f"{prefix} is:open")
    cohort_merged, _ = search_issues(
        api,
        (f"{prefix} is:merged created:{program_range} merged:{program_range}"),
    )
    cohort_closed, _ = search_issues(
        api, f"{prefix} is:closed is:unmerged created:{program_range}"
    )

    excluded_closed = sum(
        1
        for item in contributions
        if item["kind"] == "pull_request"
        and item["exclude_from_landing_rate"]
        and item["state"] == "closed"
        and not item["merged_at"]
        and since <= item["started_at"] <= until
    )
    decided_closed = max(0, cohort_closed - excluded_closed)
    decided = cohort_merged + decided_closed
    landing_rate = round(cohort_merged * 100 / decided) if decided else None

    review_query = (
        f"is:pr reviewed-by:{username} -author:{username} "
        f"updated:{program_range} {external}"
    )
    _, reviewed_candidates = search_issues(api, review_query, collect_items=True)
    reviewed_pull_requests = 0
    threshold_start = f"{since}T00:00:00Z"
    threshold_end = f"{until}T23:59:59Z"
    for item in reviewed_candidates:
        repository = item["repository_url"].removeprefix(f"{API_ROOT}/repos/")
        reviews = api.get_json(
            f"/repos/{repository}/pulls/{item['number']}/reviews",
            {"per_page": 100},
        )
        if isinstance(reviews, list) and any(
            review.get("user", {}).get("login") == username
            and threshold_start <= (review.get("submitted_at") or "") <= threshold_end
            and review.get("state") != "PENDING"
            for review in reviews
        ):
            reviewed_pull_requests += 1

    return {
        "username": username,
        "window_start": since,
        "window_end": until,
        "window_days": profile["window_days"],
        "authored_pull_requests": authored,
        "merged_pull_requests": merged,
        "open_pull_requests": open_prs,
        "external_reviews": reviewed_pull_requests,
        "landing_rate_percent": landing_rate,
        "decided_pull_requests": decided,
        "excluded_administrative_gates": excluded_closed,
        "goals": deepcopy(profile["goals"]),
    }


def summarize_review_cadence(
    contributions: list[dict[str, Any]],
    cadence: dict[str, int],
    now: datetime | None = None,
) -> dict[str, Any]:
    current = now or datetime.now(UTC)
    if current.tzinfo is None or current.utcoffset() is None:
        raise ValueError("review cadence time must include a timezone")
    current = current.astimezone(UTC)

    first_reviews_by_pull_request: dict[tuple[str, int], datetime] = {}
    for item in contributions:
        submitted_at = item.get("first_review_submitted_at")
        if (
            item.get("kind") != "review"
            or item.get("cadence_exempt")
            or not submitted_at
        ):
            continue
        key = (str(item["repository"]).casefold(), int(item["number"]))
        submitted = _parse_timestamp(str(submitted_at))
        previous = first_reviews_by_pull_request.get(key)
        if previous is None or submitted < previous:
            first_reviews_by_pull_request[key] = submitted

    review_times = sorted(first_reviews_by_pull_request.values())
    window = timedelta(hours=cadence["window_hours"])
    spacing = timedelta(hours=cadence["min_spacing_hours"])
    recent = [submitted for submitted in review_times if submitted > current - window]

    eligibility_boundaries: list[datetime] = []
    if review_times:
        eligibility_boundaries.append(review_times[-1] + spacing)
    if len(recent) >= cadence["max_fresh_reviews"]:
        eligibility_boundaries.append(recent[-cadence["max_fresh_reviews"]] + window)

    next_eligible = max(eligibility_boundaries, default=current)
    eligible_now = current >= next_eligible
    return {
        **cadence,
        "eligible_now": eligible_now,
        "next_eligible_at": (
            None if eligible_now else _format_timestamp(next_eligible)
        ),
        "latest_fresh_review_at": (
            _format_timestamp(review_times[-1]) if review_times else None
        ),
        "fresh_reviews_in_window": len(recent),
        "fresh_reviews_considered": len(review_times),
    }


def build_snapshot(
    api: GitHubAPI,
    config: dict[str, Any],
    now: datetime | None = None,
) -> dict[str, Any]:
    username = config["profile"]["username"]
    contributions = [
        fetch_contribution(api, entry, username) for entry in config["contributions"]
    ]
    return {
        "profile": fetch_profile_metrics(api, config["profile"], contributions),
        "review_cadence": summarize_review_cadence(
            contributions,
            resolve_review_cadence(config["profile"]),
            now,
        ),
        "contributions": contributions,
    }


def stabilize_contribution_timestamps(
    current: dict[str, Any],
    previous: dict[str, Any],
) -> None:
    previous_by_id = {
        item["id"]: item
        for item in previous.get("contributions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for item in current.get("contributions", []):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            continue
        old_item = previous_by_id.get(item["id"])
        if not old_item or "updated_at" not in item or "updated_at" not in old_item:
            continue
        material_item = {
            key: value for key, value in item.items() if key != "updated_at"
        }
        old_material_item = {
            key: value for key, value in old_item.items() if key != "updated_at"
        }
        if material_item == old_material_item:
            item["updated_at"] = old_item["updated_at"]


def stabilize_snapshot(
    current: dict[str, Any],
    previous: dict[str, Any] | None,
    now: datetime | None = None,
) -> dict[str, Any]:
    timestamp = (now or datetime.now(UTC)).replace(microsecond=0).isoformat()
    previous = previous or {}
    stable = deepcopy(current)
    stabilize_contribution_timestamps(stable, previous)
    previous_core = {
        key: value for key, value in previous.items() if key != "state_changed_at"
    }
    if stable == previous_core and previous.get("state_changed_at"):
        timestamp = previous["state_changed_at"]
    stable["state_changed_at"] = timestamp
    return stable


def progress_status(current: int, target: int) -> str:
    if current >= target:
        return "Target met"
    return f"{round(current * 100 / target)}%"


def escape_cell(value: Any) -> str:
    """Render untrusted text as inert Markdown table content.

    Pull-request and issue titles come from repositories we do not control.
    Escape HTML first, then encode Markdown and Liquid structural delimiters so
    Jekyll cannot reinterpret upstream text as executable markup.
    """
    text = html.escape(
        str(value).replace("\r", " ").replace("\n", " "),
        quote=True,
    )
    entities = {
        "\\": "&#92;",
        "{": "&#123;",
        "}": "&#125;",
        "[": "&#91;",
        "]": "&#93;",
        "(": "&#40;",
        ")": "&#41;",
        "|": "&#124;",
    }
    return "".join(entities.get(character, character) for character in text)


def render_check_summary(checks: dict[str, Any]) -> str | None:
    """Render successful and merely non-failing checks without conflating them."""
    successful = checks.get("successful", checks["passing"])
    non_failing = checks.get("non_failing", checks["passing"])
    if not non_failing:
        return None

    skipped = checks.get("skipped", 0)
    neutral = checks.get("neutral", 0)
    check_word = "check" if non_failing == 1 else "checks"
    if successful == non_failing:
        return f"{non_failing} {check_word} passed"

    details: list[str] = []
    if successful:
        details.append(f"{successful} passed")
    if skipped:
        details.append(f"{skipped} skipped")
    if neutral:
        details.append(f"{neutral} neutral")
    return f"{non_failing} non-failing {check_word} ({', '.join(details)})"


def render_signals(item: dict[str, Any]) -> str:
    checks = item["checks"]
    workflows = item["workflows"]
    attention = item.get("attention", {})
    base_drift = item.get("base_drift") or {}
    signals: list[str] = []
    if item.get("kind") == "issue":
        response_count = _response_count(attention)
        if response_count:
            signals.append(
                f"{response_count} response{'s' if response_count != 1 else ''}"
            )
        assignees = item.get("assignees", [])
        if assignees:
            signals.append("assigned to " + ", ".join(f"@{name}" for name in assignees))
        else:
            signals.append("unassigned")
        return " · ".join(signals)

    if attention.get("changes_requested_by"):
        count = len(attention["changes_requested_by"])
        signals.append(f"{count} active change request{'s' if count != 1 else ''}")
    response_count = _response_count(attention)
    if response_count:
        signals.append(f"{response_count} response{'s' if response_count != 1 else ''}")
    check_summary = render_check_summary(checks)
    if check_summary:
        signals.append(check_summary)
    if checks["pending"] or workflows["pending"]:
        signals.append(f"{checks['pending'] + workflows['pending']} pending")
    if checks["expected_gates"] or workflows.get("expected_gates"):
        signals.append("expected CI gate")
    if checks["unexpected_failures"] or workflows["failure"]:
        count = len(checks["unexpected_failures"]) + workflows["failure"]
        signals.append(f"{count} failing")
    if workflows["action_required"]:
        signals.append("workflow approval needed")
    if base_drift.get("behind"):
        signals.append(
            "branch update required"
            if base_drift.get("update_required")
            else "base advanced (update optional)"
        )
    return " · ".join(signals) or "No checks reported"


def render_review_cadence(cadence: dict[str, Any]) -> str:
    if cadence["eligible_now"]:
        status = "**eligible under the automated guardrail**"
    else:
        next_eligible = _parse_timestamp(cadence["next_eligible_at"]).strftime(
            "%Y-%m-%d %H:%M UTC"
        )
        status = f"**paused until {next_eligible}**"
    return (
        f"Fresh unsolicited review cadence: {status} "
        f"(rolling {cadence['window_hours']}-hour cap: "
        f"{cadence['max_fresh_reviews']}; minimum spacing: "
        f"{cadence['min_spacing_hours']} hours). "
        "Requested follow-ups remain evidence-driven and exempt."
    )


def render_dashboard(snapshot: dict[str, Any]) -> str:
    profile = snapshot["profile"]
    goals = profile["goals"]
    landing = profile["landing_rate_percent"]
    landing_display = "—" if landing is None else f"{landing}%"
    landing_status = (
        "No decided PRs yet"
        if landing is None
        else progress_status(landing, goals["landing_rate_percent"])
    )
    open_prs = profile["open_pull_requests"]
    open_limit = goals["max_open_pull_requests"]
    open_status = "Within cap" if open_prs <= open_limit else "Over cap"

    lines = [
        "## 90-day scorecard",
        "",
        (
            f"Program window: **{profile['window_start']} through "
            f"{profile['window_end']}** ({profile['window_days']} days). "
            "Outcome metrics include only new work from the program start; "
            "the authored-PR cap spans all active external work."
        ),
        "",
        "| Outcome | Current | Target | Progress |",
        "|---|---:|---:|---|",
        (
            "| Merged external pull requests "
            f"| {profile['merged_pull_requests']} "
            f"| {goals['merged_pull_requests']} "
            f"| {progress_status(profile['merged_pull_requests'], goals['merged_pull_requests'])} |"
        ),
        (
            f"| Landing rate for decided PRs | {landing_display} "
            f"| {goals['landing_rate_percent']}% | {landing_status} |"
        ),
        (
            "| External pull requests reviewed "
            f"| {profile['external_reviews']} "
            f"| {goals['external_reviews']} "
            f"| {progress_status(profile['external_reviews'], goals['external_reviews'])} |"
        ),
        (
            f"| Simultaneous open authored PRs | {open_prs} "
            f"| ≤ {open_limit} | {open_status} |"
        ),
        "",
        (
            f"Authored external PRs opened in this window: "
            f"**{profile['authored_pull_requests']}**. "
            f"Administrative gates excluded from landing-rate decisions: "
            f"**{profile['excluded_administrative_gates']}**."
        ),
        "",
        render_review_cadence(snapshot["review_cadence"]),
        "",
        "## Tracked portfolio",
        "",
        "| Contribution | Role | Stage | Verification signals | Next action |",
        "|---|---|---|---|---|",
    ]

    for item in snapshot["contributions"]:
        target_url = item.get("review_url") or item["url"]
        contribution = (
            f"[{item['repository']}#{item['number']}]({target_url})"
            f"<br>{escape_cell(item['title'])}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    contribution,
                    escape_cell(item["role"]),
                    f"**{escape_cell(item['stage'])}**",
                    escape_cell(render_signals(item)),
                    escape_cell(item["next_action"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            (f"Last public state change recorded: **{snapshot['state_changed_at']}**."),
            "",
            "_The scheduled job still checks daily. It commits only when these public "
            "facts change._",
        ]
    )
    return "\n".join(lines)


def replace_generated_section(readme: str, dashboard: str) -> str:
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one tracker marker pair")
    before, remainder = readme.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return f"{before}{START_MARKER}\n{dashboard.rstrip()}\n{END_MARKER}{after}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate configuration and README markers without network access",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config_path = root / "data" / "contributions.json"
    snapshot_path = root / "data" / "snapshot.json"
    readme_path = root / "README.md"

    config = load_json(config_path)
    validate_config(config)
    readme = readme_path.read_text(encoding="utf-8")
    replace_generated_section(readme, "validation probe")
    if args.validate_only:
        print("Tracker configuration and README markers are valid.")
        return 0

    api = GitHubAPI(os.environ.get("GITHUB_TOKEN"))
    previous = load_json(snapshot_path) if snapshot_path.exists() else None
    snapshot = stabilize_snapshot(build_snapshot(api, config), previous)
    dashboard = render_dashboard(snapshot)
    rendered_readme = replace_generated_section(readme, dashboard)

    snapshot_path.write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    readme_path.write_text(rendered_readme, encoding="utf-8")
    print("Contribution tracker refreshed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
