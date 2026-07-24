# Open Source Contribution Tracker

[![Validate tracker](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml)
[![Daily refresh](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml)

A transparent, evidence-backed dashboard for my public open-source pull
requests, reviews, and issue lanes. The goal is sustained usefulness to
maintainers—not contribution-count inflation.

<!-- TRACKER:START -->
## 90-day scorecard

Program window: **2026-07-23 through 2026-10-20** (90 days). Metrics include only new work from the program start.

| Outcome | Current | Target | Progress |
|---|---:|---:|---|
| Merged external pull requests | 0 | 24 | 0% |
| Landing rate for decided PRs | — | 70% | No decided PRs yet |
| External pull requests reviewed | 1 | 12 | 8% |
| Simultaneous open authored PRs | 1 | ≤ 4 | Within cap |

Authored external PRs opened in this window: **2**. Administrative gates excluded from landing-rate decisions: **1**.

## Tracked portfolio

| Contribution | Role | Stage | Verification signals | Next action |
|---|---|---|---|---|
| [prometheus/alertmanager#5402](https://github.com/prometheus/alertmanager/pull/5402)<br>victorops: use Splunk On-Call branding | author | **Awaiting CI approval** | 1 checks passed · workflow approval needed | Wait for maintainer workflow approval; do not ping prematurely. |
| [PrefectHQ/fastmcp#4625](https://github.com/PrefectHQ/fastmcp/pull/4625)<br>fix: use Python field name for structured task results | author | **Awaiting assignment** | 10 checks passed · 1 expected gate | Wait for issue assignment; the existing pull request will reopen automatically. |
| [prometheus-operator/prometheus-operator#8695](https://github.com/prometheus-operator/prometheus-operator/pull/8695#pullrequestreview-4769609444)<br>alertmanager: preserve top-level event_recorder configuration | reviewer | **Review submitted** | 22 checks passed | Watch the unresolved TLS compatibility finding and respond if the author follows up. |

Last public state change recorded: **2026-07-24T03:09:58+00:00**.

_The scheduled job still checks daily. It commits only when these public facts change._
<!-- TRACKER:END -->

## Operating principles

- Quality before volume: every implementation must be scoped, tested, and
  reviewable.
- Maintainer attention is scarce: no duplicate pull requests, assignment
  nudges, or premature follow-ups.
- Work in progress stays bounded to four authored pull requests, with only one
  active implementation per project.
- External reviews count when they contain a reproduced, actionable finding.
- Automated checks commit only when real public state changes; daily no-op
  refreshes do not manufacture profile activity.

The complete daily loop and intake rules are in
[docs/CONTRIBUTION_PLAYBOOK.md](docs/CONTRIBUTION_PLAYBOOK.md).

## How it works

`data/contributions.json` is the small, human-reviewed portfolio. A scheduled
GitHub Actions workflow reads public GitHub API data, updates
`data/snapshot.json`, and regenerates only the marked dashboard section above.
It uses the repository's short-lived `GITHUB_TOKEN`; no personal access token
or third-party credential is required.

Run it locally:

```bash
GITHUB_TOKEN="$(gh auth token)" python3 scripts/update_tracker.py
python3 -m unittest discover -s tests -v
```

## Add a contribution

Add a public pull request or review entry to `data/contributions.json`, then
run the updater and tests. The schema is deliberately plain JSON so every
tracked claim remains easy to inspect and change.

## License

[MIT](LICENSE)
