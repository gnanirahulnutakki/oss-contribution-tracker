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
| External pull requests reviewed | 12 | 12 | Target met |
| Simultaneous open authored PRs | 4 | ≤ 4 | Within cap |

Authored external PRs opened in this window: **5**. Administrative gates excluded from landing-rate decisions: **1**.

## Tracked portfolio

| Contribution | Role | Stage | Verification signals | Next action |
|---|---|---|---|---|
| [prometheus/alertmanager#5402](https://github.com/prometheus/alertmanager/pull/5402)<br>victorops: use Splunk On-Call branding | author | **Awaiting CI approval** | 2 checks passed · workflow approval needed | Wait for maintainer workflow approval; do not ping prematurely. |
| [prometheus-community/postgres_exporter#1351](https://github.com/prometheus-community/postgres_exporter/pull/1351)<br>fix: preserve precision for large counters | author | **Awaiting CI approval** | 1 checks passed · workflow approval needed | Wait for maintainer approval of first-time contributor workflows; do not ping prematurely. |
| [PrefectHQ/fastmcp#4625](https://github.com/PrefectHQ/fastmcp/pull/4625)<br>fix: use Python field name for structured task results | author | **Awaiting assignment** | 10 checks passed · 1 expected gate | Wait for issue assignment; the existing pull request will reopen automatically. |
| [open-telemetry/otel-arrow#3572](https://github.com/open-telemetry/otel-arrow/pull/3572)<br>fix(filter): reject unknown config fields | author | **Awaiting CI approval** | 3 checks passed · 1 expected gate · workflow approval needed | Link and verify the commit email on GitHub, then complete EasyCLA; wait for issue assignment and maintainer workflow approval before marking the draft ready. |
| [envoyproxy/gateway#9574](https://github.com/envoyproxy/gateway/pull/9574)<br>docs: explain backend protocol selection | author | **Draft** | 28 checks passed | CI is green; wait for maintainer assignment or direction on #8773, then mark the draft ready if requested. |
| [prometheus-operator/prometheus-operator#8695](https://github.com/prometheus-operator/prometheus-operator/pull/8695#pullrequestreview-4769609444)<br>alertmanager: preserve top-level event_recorder configuration | reviewer | **Review submitted** | 22 checks passed | Watch the unresolved TLS compatibility finding and respond if the author follows up. |
| [prometheus/client_golang#2062](https://github.com/prometheus/client_golang/pull/2062#pullrequestreview-4769888408)<br>api: return HTTP status on non-JSON API error bodies | reviewer | **Review submitted** | 15 checks passed | Watch the valid-JSON error-envelope finding and re-review if the author updates the pull request. |
| [helm/helm#32339](https://github.com/helm/helm/pull/32339#pullrequestreview-4770049007)<br>fix(scripts): add cache-busting to get-helm-3 version check | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Watch the cache-header and Helm 4 parity threads; re-review after the author updates the pull request. |
| [openai/openai-agents-python#3933](https://github.com/openai/openai-agents-python/pull/3933#discussion_r3643680270)<br>fix: enforce realtime text guardrails and synchronize streaming cancellation | reviewer | **Review submitted** | 9 checks passed | Watch the confirmed public-result agent-state finding on the current head; re-review after the ordinary and resumed handoff paths are updated. |
| [google/adk-python#6459](https://github.com/google/adk-python/pull/6459#pullrequestreview-4771066656)<br>fix: route MCP calls to the .mtls.googleapis.com endpoint for Agent Identity | reviewer | **Review submitted** | 8 checks passed · workflow approval needed | Watch for maintainer feedback or another head update; the mTLS policy matrix and formatter follow-up are verified on 2f0043ee. |
| [google/adk-python#6460](https://github.com/google/adk-python/pull/6460#pullrequestreview-4770729500)<br>fix(litellm): strip embedded thought_signature from tool call id | reviewer | **Review submitted** | 7 checks passed · 1 expected gate · workflow approval needed | Watch the malformed embedded-signature ID finding and re-review after the author updates the pull request. |
| [pydantic/pydantic-ai#6706](https://github.com/pydantic/pydantic-ai/pull/6706#pullrequestreview-4770938242)<br>Validate native tool ids per capability layer instead of flattened | reviewer | **Review submitted** | 81 checks passed | Watch the CombinedCapability child-layer validation finding and re-review after the pull request is updated. |
| [microsoft/agent-framework#7292](https://github.com/microsoft/agent-framework/pull/7292#pullrequestreview-4771214920)<br>Python: [Feature]: Support OpenAI instructions in Responses API | reviewer | **Review submitted** | 40 checks passed · 2 expected gate · 1 failing | Watch the validated OpenAIChatOptions test-typing fix and re-review after the author updates head 01ef5bf. |
| [microsoft/autogen#7994](https://github.com/microsoft/autogen/pull/7994#pullrequestreview-4771362474)<br>fix(autogen-ext): skip LangChain callback-manager (run_manager) when inferring tool args schema | reviewer | **Review submitted** | 2 checks passed · workflow approval needed | Watch the reserved callbacks filtering and TypedDict test-typing findings; re-review after the author updates the pull request. |
| [crewAIInc/crewAI#6625](https://github.com/crewAIInc/crewAI/pull/6625#pullrequestreview-4771496651)<br>fix(reasoning): use flexible regex to detect READY state to prevent agent deadlocks | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Watch the semantic readiness-marker finding and re-review after the author updates head d2c0b593. |
| [huggingface/smolagents#2565](https://github.com/huggingface/smolagents/pull/2565#pullrequestreview-4771627268)<br>fix: filter TOOL_CALL and TOOL_RESPONSE messages from managed-agent summary | reviewer | **Review submitted** | workflow approval needed | Watch for the author to remove the unrelated #2564 executor commit, then re-review the isolated managed-agent summary fix. |
| [strands-agents/harness-sdk#3448](https://github.com/strands-agents/harness-sdk/pull/3448#pullrequestreview-4771826938)<br>feat(graph): add Python concurrency limit | reviewer | **Review submitted** | 10 checks passed · 3 pending · workflow approval needed | Watch the positive-integer validation finding and re-review after the builder and direct Graph constructor are hardened. |

Last public state change recorded: **2026-07-24T09:08:38+00:00**.

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
