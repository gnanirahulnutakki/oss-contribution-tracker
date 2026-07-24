# Contribution Playbook

This repository is the control plane for a sustained open-source contribution
program. It tracks public evidence and keeps the daily process focused on work
that maintainers are likely to accept.

## 90-day outcomes

The current program begins on July 23, 2026. Activity predating that restart,
including older open pull requests, stays visible on GitHub but is outside this
scorecard.

- 24 merged, independent pull requests
- at least a 70% landing rate for decided pull requests
- 12 substantive reviews of other contributors' pull requests
- top-100 contributor presence in two anchor projects
- no more than four simultaneous authored pull requests

These are directional operating targets, not a reason to split changes
artificially or create low-value activity.

## Portfolio focus

Prefer new and emerging AI open-source projects when they offer clear
maintainer intent, a current unclaimed issue, and a locally verifiable scope.
AI infrastructure, agents, evaluation, inference, observability, and developer
tooling are priority areas, while established cloud-native projects remain
useful anchors for durable maintainer relationships.

Project novelty never weakens the intake gate below. Do not chase activity in
an AI repository solely because it is popular or new.

## Daily loop

1. Refresh every tracked pull request, review thread, issue assignment, and CI
   gate.
2. Address maintainer feedback before beginning new implementation work.
3. If capacity remains, prefer one current issue in an emerging AI project
   with clear maintainer intent, no assignee, no competing pull request, and a
   locally testable scope. Use a cloud-native anchor when no equally strong AI
   lane is available.
4. Reproduce the problem, implement the smallest complete fix, run the
   repository's actual gates, and self-review the diff.
5. Publish one focused pull request with a linked issue, evidence, and required
   disclosures.
6. Record the new lane here and stop when the work-in-progress limit is reached.

## Intake gate

A new implementation lane starts only when all of these are true:

- The issue is open and still relevant on the current default branch.
- No one is assigned or actively claiming the work.
- No open pull request already implements the same outcome.
- Repository contribution and AI-use policies permit the workflow.
- The expected change can be verified locally.
- The project is not already carrying another active implementation from this
  contributor.

If any item fails, the lane is dropped without contacting maintainers.

## Communication policy

- Do not ask for assignment when repository instructions prohibit it.
- Do not open a replacement pull request for an automated assignment gate.
- Do not ping for review immediately after publishing.
- Reply when a maintainer asks a question or requests a change.
- Close the loop with concrete evidence: commit, test, CI run, or merged state.

## What the dashboard means

- **PR open**: implementation is public and awaiting normal review.
- **Awaiting CI approval**: a first-time-contributor workflow needs a
  maintainer to authorize execution; this is not a test failure.
- **Awaiting assignment**: repository automation has parked the pull request
  until the linked issue is assigned.
- **Review submitted**: a substantive review was posted on another
  contributor's pull request.
- **Review update available**: the pull request head changed after the most
  recent review, so the new diff needs a focused re-check before the review is
  considered current.
- **Response available**: a human replied inside one of the contributor's
  review threads or directly mentioned the contributor after their latest
  public review activity.
- **Maintainer response**: a human directly mentioned the contributor on an
  authored pull request after the contributor's latest public activity.
- **Changes requested**: at least one reviewer's latest effective decision is
  still `CHANGES_REQUESTED`; later comment-only reviews do not clear it.
- **Merged**: GitHub reports the pull request as merged.

The landing-rate denominator excludes explicitly identified administrative
gates so they are not confused with maintainers rejecting the implementation.

The automated response queue is intentionally conservative. It ignores bots
and general top-level discussion, and it never posts comments. A later
contributor review or reply clears older response signals; changed heads still
take priority because they require code inspection.
