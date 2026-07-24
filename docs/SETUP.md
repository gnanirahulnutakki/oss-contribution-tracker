# Set up your contribution tracker

This repository can be used as a template for an evidence-backed public
open-source portfolio. It reads public GitHub state, renders a scorecard in the
README, and commits only material changes.

## 1. Create your repository

Use GitHub's **Use this template** action, then create a public repository under
your account. Public visibility lets profile visitors and maintainers inspect
the same evidence shown in the dashboard.

## 2. Configure the program

Edit `data/contributions.json`:

- `profile.username`: your GitHub login.
- `profile.program_start`: the first day included in metrics, as `YYYY-MM-DD`.
- `profile.window_days`: the fixed reporting-window length.
- `profile.review_cadence`: the rolling window, maximum fresh reviews in that
  window, and minimum spacing used by the machine-readable advisory.
- `profile.excluded_owners`: your login plus organizations whose repositories
  should not count as external contributions.
- `profile.goals`: targets for merged pull requests, landing rate, external
  reviews, and simultaneous open authored pull requests.

Keep the program window fixed. Moving its start date after work begins makes
historical comparisons misleading.

## 3. Add reviewed contributions

Each entry under `contributions` identifies one public pull request or review:

```json
{
  "id": "example-project-123",
  "kind": "pull_request",
  "repository": "example/project",
  "number": 123,
  "role": "author",
  "tier": "anchor",
  "started_at": "2026-01-15",
  "linked_issue": 99,
  "next_action": "Wait for maintainer review; do not ping prematurely."
}
```

Use `kind: "review"` and add `review_url` for an external code review. Optional
fields support known CI gates, assignment-gated work, and items that should not
affect the landing-rate denominator. Keep `next_action` specific enough that a
future refresh cannot justify a generic status ping.

Set `cadence_exempt: true` only when a review entry represents a direct
maintainer-requested review rather than fresh unsolicited outreach. The tracker
uses the first non-pending review after `started_at` for each distinct pull
request, so later re-reviews do not consume another cadence slot.

## 4. Validate locally

Python 3.13 or newer is recommended. The runtime uses only the standard library.

```bash
python3 scripts/update_tracker.py --validate-only
python3 -m unittest discover -s tests -v
GITHUB_TOKEN="$(gh auth token)" python3 scripts/update_tracker.py
```

The token is read from the environment and must not be committed. Local
authentication improves API rate limits; the scheduled workflow uses GitHub's
short-lived repository token.

## 5. Enable scheduled refreshes

In **Settings → Actions → General**, allow workflows to read and write repository
contents. The workflow in `.github/workflows/update.yml` requests narrow read
permissions for public contribution state and write permission only for the
generated tracker commit.

Update the schedule and IANA timezone in that workflow if the default daily
time is not suitable. Run it once through **Actions → Daily refresh → Run
workflow**, then confirm:

1. The workflow succeeds.
2. `README.md` and `data/snapshot.json` change only when public facts change.
3. A second run against unchanged GitHub state creates no commit.

## 6. Make the evidence visible

Link the repository from your GitHub profile README or website field. Keep
claims in the profile concise and use this tracker for live counts, CI results,
maintainer responses, and next actions.

## Operating guardrails

- Prefer merged, tested outcomes over activity volume.
- Keep authored work in progress bounded.
- Do not claim unassigned issues or duplicate active pull requests.
- Respond only to concrete maintainer questions or actionable review feedback.
- Bound fresh unsolicited reviews by both cycle and time; this template uses
  one per cycle, two per rolling 24 hours, and at least four hours between them.
- Never let the tracker post upstream comments automatically.
