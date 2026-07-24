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
| External pull requests reviewed | 20 | 12 | Target met |
| Simultaneous open authored PRs | 4 | ≤ 4 | Within cap |

Authored external PRs opened in this window: **5**. Administrative gates excluded from landing-rate decisions: **1**.

Fresh unsolicited review cadence: **paused until 2026-07-25 21:40 UTC** (rolling 24-hour cap: 2; minimum spacing: 4 hours). Requested follow-ups remain evidence-driven and exempt.

## Tracked portfolio

| Contribution | Role | Stage | Verification signals | Next action |
|---|---|---|---|---|
| [prometheus/alertmanager#5402](https://github.com/prometheus/alertmanager/pull/5402)<br>victorops: use Splunk On-Call branding | author | **Awaiting CI approval** | 2 checks passed · workflow approval needed | Wait for maintainer workflow approval; do not ping prematurely. |
| [prometheus-community/postgres_exporter#1351](https://github.com/prometheus-community/postgres_exporter/pull/1351)<br>fix: preserve precision for large counters | author | **Awaiting CI approval** | 1 checks passed · workflow approval needed | Wait for maintainer approval of first-time contributor workflows; do not ping prematurely. |
| [PrefectHQ/fastmcp#4625](https://github.com/PrefectHQ/fastmcp/pull/4625)<br>fix: use Python field name for structured task results | author | **Awaiting assignment** | 10 checks passed · expected CI gate | Wait for issue assignment; the existing pull request will reopen automatically. |
| [open-telemetry/otel-arrow#3572](https://github.com/open-telemetry/otel-arrow/pull/3572)<br>fix(filter): reject unknown config fields | author | **Awaiting CI approval** | 77 checks passed · expected CI gate · workflow approval needed | Link and verify the commit email on GitHub, then complete EasyCLA; the PR is assigned, ready, twice approved, and all technical checks pass. |
| [envoyproxy/gateway#9574](https://github.com/envoyproxy/gateway/pull/9574)<br>docs: explain backend protocol selection | author | **Draft** | 28 checks passed | CI is green; wait for maintainer assignment or direction on #8773, then mark the draft ready if requested. |
| [prometheus-operator/prometheus-operator#8695](https://github.com/prometheus-operator/prometheus-operator/pull/8695#pullrequestreview-4769609444)<br>alertmanager: preserve top-level event_recorder configuration | reviewer | **Review submitted** | 22 checks passed | Watch the unresolved TLS compatibility finding and respond if the author follows up. |
| [prometheus/client_golang#2062](https://github.com/prometheus/client_golang/pull/2062#pullrequestreview-4769888408)<br>api: return HTTP status on non-JSON API error bodies | reviewer | **Review submitted** | 15 checks passed | Watch the valid-JSON error-envelope finding and re-review if the author updates the pull request. |
| [helm/helm#32339](https://github.com/helm/helm/pull/32339#pullrequestreview-4770049007)<br>fix(scripts): add cache-busting to get-helm-3 version check | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Watch the cache-header and Helm 4 parity threads; re-review after the author updates the pull request. |
| [openai/openai-agents-python#3933](https://github.com/openai/openai-agents-python/pull/3933#pullrequestreview-4776733214)<br>fix: enforce realtime text guardrails and synchronize streaming cancellation | reviewer | **Review update available** | 9 checks passed | Head e6b93288 has three unresolved, specific automated findings; do not duplicate them or post a general summary. Re-review only after the author updates the head or asks a concrete question. |
| [google/adk-python#6459](https://github.com/google/adk-python/pull/6459#pullrequestreview-4771066656)<br>fix: route MCP calls to the .mtls.googleapis.com endpoint for Agent Identity | reviewer | **Review submitted** | 8 checks passed · workflow approval needed | Watch for maintainer feedback or another head update; the mTLS policy matrix and formatter follow-up are verified on 2f0043ee. |
| [google/adk-python#6460](https://github.com/google/adk-python/pull/6460#pullrequestreview-4776004279)<br>fix(litellm): strip embedded thought_signature from tool call id | reviewer | **Review submitted** | 7 checks passed · expected CI gate · workflow approval needed | Watch the empty embedded-signature ID finding and formatter follow-up on head 15bbca82; re-review only after another author update. |
| [pydantic/pydantic-ai#6706](https://github.com/pydantic/pydantic-ai/pull/6706#pullrequestreview-4770938242)<br>Validate native tool ids per capability layer instead of flattened | reviewer | **Review submitted** | 81 checks passed | Watch the CombinedCapability child-layer validation finding and re-review after the pull request is updated. |
| [microsoft/agent-framework#7292](https://github.com/microsoft/agent-framework/pull/7292#pullrequestreview-4776007573)<br>Python: [Feature]: Support OpenAI instructions in Responses API | reviewer | **Review submitted** | 2 checks passed · workflow approval needed | The OpenAIChatOptions typing finding is verified fixed on head 8a6a52c9; wait for maintainer scope direction and CI. |
| [microsoft/autogen#7994](https://github.com/microsoft/autogen/pull/7994#pullrequestreview-4776009034)<br>fix(autogen-ext): skip LangChain callback-manager (run_manager) when inferring tool args schema | reviewer | **Review submitted** | 2 checks passed · workflow approval needed | Both callbacks filtering and TypedDict test-typing findings are verified fixed on head c1b1fc24; wait for maintainer review and CI. |
| [crewAIInc/crewAI#6625](https://github.com/crewAIInc/crewAI/pull/6625#pullrequestreview-4771496651)<br>fix(reasoning): use flexible regex to detect READY state to prevent agent deadlocks | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Watch the semantic readiness-marker finding and re-review after the author updates head d2c0b593. |
| [huggingface/smolagents#2565](https://github.com/huggingface/smolagents/pull/2565#pullrequestreview-4776010815)<br>fix: filter TOOL_CALL and TOOL_RESPONSE messages from managed-agent summary | reviewer | **Review submitted** | workflow approval needed | The unrelated commit is removed; watch the missing TOOL_CALL and TOOL_RESPONSE regression-test finding and re-review after an author update. |
| [strands-agents/harness-sdk#3448](https://github.com/strands-agents/harness-sdk/pull/3448#pullrequestreview-4771826938)<br>feat(graph): add Python concurrency limit | reviewer | **Review submitted** | 10 checks passed · 3 pending · workflow approval needed | Watch the positive-integer validation finding and re-review after the builder and direct Graph constructor are hardened. |
| [openai/openai-python#3538](https://github.com/openai/openai-python/pull/3538#pullrequestreview-4776232747)<br>fix(streaming): return final response for incomplete and failed events | reviewer | **Review submitted** | workflow approval needed | The incomplete/failed structured-output fix is verified on head e896c03a; wait for maintainer review or another head update. |
| [langchain-ai/deepagents#5026](https://github.com/langchain-ai/deepagents/pull/5026#pullrequestreview-4772078666)<br>fix(sdk): make `BackendProtocol.glob` recursive for bare patterns | reviewer | **Review submitted** | 87 checks passed · 3 failing | Watch the unbounded sandbox brace-expansion finding and re-review after expansion is capped with regression coverage. |
| [sgl-project/sglang#32344](https://github.com/sgl-project/sglang/pull/32344#pullrequestreview-4776140668)<br>[Bugfix] Emit cached token metric before first cache hit | reviewer | **Review submitted** | 85 checks passed · expected CI gate | Watch the PromQL label-set mismatch finding on head 94b638a4; re-review after the metric schema or query and regression coverage are corrected. |
| [browser-use/browser-use#5300](https://github.com/browser-use/browser-use/pull/5300#pullrequestreview-4776211914)<br>Call the model with minimal state after capture timeout | reviewer | **Review submitted** | 95 checks passed | Watch for author or maintainer follow-up and re-review only if the head changes or a concrete timeout-safety question is raised. |
| [modelcontextprotocol/typescript-sdk#2544](https://github.com/modelcontextprotocol/typescript-sdk/pull/2544#pullrequestreview-4776312162)<br>Fix tests timing out during interactive OAuth flow (#2510) | reviewer | **Review submitted** | 16 checks passed | Watch the unresolved REDIRECT lifecycle finding on head a740d28c; re-review after the triggering request stays pending through finishAuth and retry with regression coverage. |
| [confident-ai/deepeval#2950](https://github.com/confident-ai/deepeval/pull/2950#pullrequestreview-4776624336)<br>fix(openai): apply prompt-caching discount to GPTModel cost calculation | reviewer | **Review submitted** | 11 checks passed · expected CI gate · 4 failing | Watch the default GPT-5 cache-pricing and existing-completion regression findings on head a14a307c; re-review after the author updates the prices and full affected test suite. |
| [traceloop/openllmetry#4375](https://github.com/traceloop/openllmetry/pull/4375#pullrequestreview-4776934105)<br>fix(cohere): avoid double-ending async error spans | reviewer | **Review submitted** | 3 checks passed · workflow approval needed | Watch the duplicate exception-event finding on head 9c303fd1; re-review after one layer owns exception recording and the regression asserts exact cardinality. |
| [Arize-ai/openinference#3429](https://github.com/Arize-ai/openinference/pull/3429#pullrequestreview-4777149779)<br>fix(anthropic): preserve APIPromise helpers | reviewer | **Review submitted** | 20 checks passed | Watch the consumed asResponse body finding on head 8554f3db; re-review after failure observation no longer triggers eager parsing and raw-response regression coverage is added. |

Last public state change recorded: **2026-07-24T23:32:38+00:00**.

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
- Fresh unsolicited reviews are limited to one per automated cycle and two per
  rolling 24 hours, with at least four hours between them.
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

The refresh records exact heads and draft state, detects active change requests
on authored pull requests, and surfaces only direct human mentions, replies to
the contributor's own review threads, or trusted linked-issue responses after
the contribution began. It also derives the next fresh-review eligibility
boundary from first-submission timestamps while leaving explicitly requested
follow-ups exempt. Bot-only pull-request timestamp churn is stabilized so it
cannot create synthetic tracker commits. The tracker never posts upstream
comments.

## Reuse this tracker

This repository is designed to work as a GitHub template. Configuration lives
in `data/contributions.json`; the update engine and workflows do not depend on
the original repository owner.

Follow the [setup guide](docs/SETUP.md) to configure a reporting window, add
reviewed contributions, enable the scheduled refresh, and verify that unchanged
public state produces no synthetic commit.

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
