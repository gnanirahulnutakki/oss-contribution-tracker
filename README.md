# Open Source Contribution Tracker

[![Validate tracker](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml)
[![Daily refresh](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml)

A transparent, evidence-backed dashboard for my public open-source pull
requests, reviews, and issue lanes. The goal is sustained usefulness to
maintainers—not contribution-count inflation.

<!-- TRACKER:START -->
## 90-day scorecard

Program window: **2026-07-23 through 2026-10-20** (90 days). Outcome metrics include only new work from the program start; the authored-PR cap spans all active external work.

| Outcome | Current | Target | Progress |
|---|---:|---:|---|
| Merged external pull requests | 0 | 24 | 0% |
| Landing rate for decided PRs | — | 70% | No decided PRs yet |
| External pull requests reviewed | 25 | 12 | Target met |
| Simultaneous open authored PRs | 7 | ≤ 4 | Over cap |

Authored external PRs opened in this window: **5**. Administrative gates excluded from landing-rate decisions: **1**.

Fresh unsolicited review cadence: **paused until 2026-07-28 07:12 UTC** (rolling 24-hour cap: 2; minimum spacing: 4 hours). Requested follow-ups remain evidence-driven and exempt.

## Tracked portfolio

| Contribution | Role | Stage | Verification signals | Next action |
|---|---|---|---|---|
| [prometheus/alertmanager#5402](https://github.com/prometheus/alertmanager/pull/5402)<br>victorops: use Splunk On-Call branding | author | **Awaiting CI approval** | 2 checks passed · workflow approval needed · base advanced (update optional) | Wait for maintainer workflow approval; do not ping prematurely. |
| [prometheus-community/postgres_exporter#1351](https://github.com/prometheus-community/postgres_exporter/pull/1351)<br>fix: preserve precision for large counters | author | **Changes requested** | 1 active change request · 15 checks passed · base advanced (update optional) | The CLI-only change is pushed in 9c8b1d9, its review thread is resolved, and all 15 checks pass; wait for maintainer re-review. |
| [PrefectHQ/fastmcp#4625](https://github.com/PrefectHQ/fastmcp/pull/4625)<br>fix: use Python field name for structured task results | author | **Closed** | 10 checks passed · expected CI gate | Issue #4616 was closed by merged maintainer PR #4657; this administrative pull request remains closed. No follow-up is needed. |
| [open-telemetry/otel-arrow#3572](https://github.com/open-telemetry/otel-arrow/pull/3572)<br>fix(filter): reject unknown config fields | author | **PR open** | 78 checks passed · expected CI gate · base advanced (update optional) | Link and verify the commit email on GitHub, then complete EasyCLA; the PR is assigned, ready, twice approved, and all technical checks pass. |
| [envoyproxy/gateway#9574](https://github.com/envoyproxy/gateway/pull/9574)<br>docs: explain backend protocol selection | author | **Draft** | 28 checks passed · base advanced (update optional) | CI is green; wait for maintainer assignment or direction on #8773, then mark the draft ready if requested. |
| [oam-dev/cluster-gateway#171](https://github.com/oam-dev/cluster-gateway/pull/171)<br>fix(proxy): enforce managed credential precedence | author | **PR open** | 8 checks passed | All eight checks pass and no review thread or maintainer reply is outstanding; wait without pinging. |
| [NousResearch/hermes-agent#10824](https://github.com/NousResearch/hermes-agent/pull/10824)<br>fix(installer): reuse existing newer Python before downloading 3.11 | author | **PR open** | 38 checks passed · base advanced (update optional) | Head ce1cd22 is rebased onto current main, bounds reuse to >=3.11,<3.14, preserves UV_PYTHON repinning, and passes 41 shell-installer plus 13 contributor-mapping tests. The review thread is resolved and all 27 reporting CI checks pass; wait for maintainer re-review without pinging. |
| [NousResearch/hermes-agent#10828](https://github.com/NousResearch/hermes-agent/pull/10828)<br>fix(runtime): auto-upgrade GPT-5 named custom providers to codex_responses | author | **Closed** | No checks reported | Closed after confirming model-only Responses inference conflicts with the current custom-provider compatibility policy; no follow-up is needed. |
| [NousResearch/hermes-agent#10852](https://github.com/NousResearch/hermes-agent/pull/10852)<br>fix(gateway): keep auto vision preprocess concise | author | **PR open** | 38 checks passed · base advanced (update optional) | Head 1f898ab preserves the explicit 500-token cap through custom-provider requests and retry/fallback paths, with 462 focused tests plus 48,637 full-suite passes. The review thread is resolved and all 27 reporting CI checks pass; wait for maintainer re-review without pinging. |
| [prometheus-operator/prometheus-operator#8695](https://github.com/prometheus-operator/prometheus-operator/pull/8695#pullrequestreview-4769609444)<br>alertmanager: preserve top-level event_recorder configuration | reviewer | **Review submitted** | 22 checks passed | Watch the unresolved TLS compatibility finding and respond if the author follows up. |
| [prometheus/client_golang#2062](https://github.com/prometheus/client_golang/pull/2062#pullrequestreview-4769888408)<br>api: return HTTP status on non-JSON API error bodies | reviewer | **Review submitted** | 15 checks passed | Watch the valid-JSON error-envelope finding and re-review if the author updates the pull request. |
| [helm/helm#32339](https://github.com/helm/helm/pull/32339#pullrequestreview-4790630703)<br>fix(scripts): add cache-busting to Helm version checks | reviewer | **Review submitted** | 3 checks passed · workflow approval needed | Approved bc0114c after verifying the requested --header spelling and best-effort CDN wording, all four curl/wget paths, syntax, diff hygiene, and a conflict-free current-main merge; wait for a changed head or concrete maintainer follow-up. |
| [openai/openai-agents-python#3933](https://github.com/openai/openai-agents-python/pull/3933#pullrequestreview-4776733214)<br>fix: enforce realtime text guardrails and synchronize streaming cancellation | reviewer | **Review update available** | 9 checks passed | Head e6b93288 has three unresolved, specific automated findings; do not duplicate them or post a general summary. Re-review only after the author updates the head or asks a concrete question. |
| [google/adk-python#6459](https://github.com/google/adk-python/pull/6459#pullrequestreview-4790316157)<br>fix: route MCP calls to the .mtls.googleapis.com endpoint for Agent Identity | reviewer | **Review submitted** | 23 checks passed · expected CI gate | Force-pushed head 4b115485 is byte-identical in the two pull-request files to verified 2f0043ee; exact-head and current-main synthetic checks each pass 52 focused tests plus pinned style and diff validation. Only the expected Copybara handoff remains; wait for maintainer action or a changed head. |
| [google/adk-python#6460](https://github.com/google/adk-python/pull/6460#pullrequestreview-4776004279)<br>fix(litellm): strip embedded thought_signature from tool call id | reviewer | **Review update available** | 6 checks passed · expected CI gate · 1 failing · workflow approval needed | Head 7c6904ab still has the unresolved empty embedded-signature ID finding; the failing agent-triage run is an unrelated Gemini 503 and CLA remains the expected gate. Do not duplicate the inline finding; re-review only after a substantive author update. |
| [pydantic/pydantic-ai#6706](https://github.com/pydantic/pydantic-ai/pull/6706#pullrequestreview-4770938242)<br>Validate native tool ids per capability layer instead of flattened | reviewer | **Review submitted** | 81 checks passed | Watch the CombinedCapability child-layer validation finding and re-review after the pull request is updated. |
| [microsoft/agent-framework#7292](https://github.com/microsoft/agent-framework/pull/7292#pullrequestreview-4776007573)<br>Python: [Feature]: Support OpenAI instructions in Responses API | reviewer | **Review landed** | 37 checks passed | Merged on head 8a6a52c9 after two maintainer approvals and 37 passing checks; no follow-up required. |
| [microsoft/autogen#7994](https://github.com/microsoft/autogen/pull/7994#pullrequestreview-4776009034)<br>fix(autogen-ext): skip LangChain callback-manager (run_manager) when inferring tool args schema | reviewer | **Review submitted** | 2 checks passed · workflow approval needed | Both callbacks filtering and TypedDict test-typing findings are verified fixed on head c1b1fc24; wait for maintainer review and CI. |
| [crewAIInc/crewAI#6625](https://github.com/crewAIInc/crewAI/pull/6625#pullrequestreview-4771496651)<br>fix(reasoning): use flexible regex to detect READY state to prevent agent deadlocks | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Watch the semantic readiness-marker finding and re-review after the author updates head d2c0b593. |
| [huggingface/smolagents#2565](https://github.com/huggingface/smolagents/pull/2565#pullrequestreview-4779293759)<br>fix: filter TOOL_CALL and TOOL_RESPONSE messages from managed-agent summary | reviewer | **Review submitted** | workflow approval needed | Regression coverage is verified and approved on head e5685e0; wait for maintainer review and merge. |
| [strands-agents/harness-sdk#3448](https://github.com/strands-agents/harness-sdk/pull/3448#pullrequestreview-4782383330)<br>feat(graph): add Python concurrency limit | reviewer | **Review submitted** | 7 checks passed · 3 pending · workflow approval needed | The positive-integer validation fix is verified and approved on head 97c2b6e; wait for maintainer workflow authorization, review, or another head update. |
| [openai/openai-python#3538](https://github.com/openai/openai-python/pull/3538#pullrequestreview-4776232747)<br>fix(streaming): return final response for incomplete and failed events | reviewer | **Review submitted** | workflow approval needed | The incomplete/failed structured-output fix is verified on head e896c03a; wait for maintainer review or another head update. |
| [langchain-ai/deepagents#5026](https://github.com/langchain-ai/deepagents/pull/5026#pullrequestreview-4772078666)<br>fix(sdk): make `BackendProtocol.glob` recursive for bare patterns | reviewer | **Review submitted** | 87 checks passed · 3 failing | Watch the unbounded sandbox brace-expansion finding and re-review after expansion is capped with regression coverage. |
| [sgl-project/sglang#32344](https://github.com/sgl-project/sglang/pull/32344#pullrequestreview-4776140668)<br>[Bugfix] Emit cached token metric before first cache hit | reviewer | **Review submitted** | 85 checks passed · expected CI gate | Watch the PromQL label-set mismatch finding on head 94b638a4; re-review after the metric schema or query and regression coverage are corrected. |
| [browser-use/browser-use#5300](https://github.com/browser-use/browser-use/pull/5300#pullrequestreview-4776211914)<br>Call the model with minimal state after capture timeout | reviewer | **Review landed** | 96 checks passed | Watch for author or maintainer follow-up and re-review only if the head changes or a concrete timeout-safety question is raised. |
| [modelcontextprotocol/typescript-sdk#2544](https://github.com/modelcontextprotocol/typescript-sdk/pull/2544#pullrequestreview-4776312162)<br>Fix tests timing out during interactive OAuth flow (#2510) | reviewer | **Review submitted** | 16 checks passed | Watch the unresolved REDIRECT lifecycle finding on head a740d28c; re-review after the triggering request stays pending through finishAuth and retry with regression coverage. |
| [confident-ai/deepeval#2950](https://github.com/confident-ai/deepeval/pull/2950#pullrequestreview-4779294175)<br>fix(openai): apply prompt-caching discount to GPTModel cost calculation | reviewer | **Review submitted** | 12 checks passed · expected CI gate · 2 failing | The mocked-usage regression is fixed on a7a4a718; GPT-5.4 cached pricing remains unresolved, so re-review after pricing data and a default-model regression are added. |
| [traceloop/openllmetry#4375](https://github.com/traceloop/openllmetry/pull/4375#pullrequestreview-4776934105)<br>fix(cohere): avoid double-ending async error spans | reviewer | **Review submitted** | 3 checks passed · workflow approval needed | Watch the duplicate exception-event finding on head 9c303fd1; re-review after one layer owns exception recording and the regression asserts exact cardinality. |
| [Arize-ai/openinference#3429](https://github.com/Arize-ai/openinference/pull/3429#pullrequestreview-4787290072)<br>fix(anthropic): preserve APIPromise helpers | reviewer | **Review submitted** | 21 checks passed | The consumed asResponse body finding is verified fixed and approved on head d4827bfb; all 16 package tests, type-check, build, lint, and format passed, and all 21 GitHub checks completed without failure. Wait for maintainer action or a changed head. |
| [AgentOps-AI/agentops#1428](https://github.com/AgentOps-AI/agentops/pull/1428#pullrequestreview-4780556283)<br>fix(langchain): capture structured output tool calls | reviewer | **Review submitted** | 1 checks passed · workflow approval needed | Structured-output capture is reproduced and approved on head 85f6896; wait for maintainer review, CI authorization, or a new head. |
| [agno-agi/agno#9174](https://github.com/agno-agi/agno/pull/9174#pullrequestreview-4781165073)<br>refactor: resolve the pydantic version once instead of per tool | reviewer | **Review submitted** | 10 checks passed | The cache optimization is independently verified and approved on head 140bd1d; watch the non-blocking concurrent cold-start wording and formatter cleanup, then re-review only after a new head or concrete reply. |
| [omnigent-ai/omnigent#3304](https://github.com/omnigent-ai/omnigent/pull/3304#pullrequestreview-4783071226)<br>fix(accounts): enforce the last-admin invariant atomically on delete | reviewer | **Review submitted** | 60 checks passed · expected CI gate | The last-admin invariant is independently validated and approved on head bb2ca4c across SQLite, PostgreSQL 16, and MySQL 8.0; wait for author or maintainer follow-up and re-review only after a new head or concrete reply. |
| [opensquilla/opensquilla#815](https://github.com/opensquilla/opensquilla/pull/815#pullrequestreview-4787283091)<br>fix(engine): evict cache-break monitor state for terminal sessions | reviewer | **Review submitted** | workflow approval needed | The false cache-break diagnostic is verified fixed and approved on head af315af: the original reproducer now reports baseline_initialized without a break, 2,210 exact-head tests passed, and a current-main synthetic merge passed all 18 focused regressions plus Ruff and mypy. Wait for maintainer action or a changed head. |
| [agentscope-ai/agentscope#1874](https://github.com/agentscope-ai/agentscope/pull/1874#pullrequestreview-4792240922)<br>fix(embedding): omit default OpenAI dimensions | reviewer | **Review submitted** | 6 checks passed | Two P2 findings are open on head ce2832e: preserve explicit pass_dimensions=False when Parameters uses defaults, and retain genuine multi-type anyOf schemas. Re-review only after an author update or concrete reply. |
| [oam-dev/cluster-gateway#170](https://github.com/oam-dev/cluster-gateway/issues/170)<br>Security: managed credential must override inbound Authorization on proxy requests | author | **Issue open** | unassigned | The linked implementation PR is green; wait for maintainer review without a status ping. |
| [CaviraOSS/OpenMemory#186](https://github.com/CaviraOSS/OpenMemory/issues/186)<br>`delete_all` removes DB rows but not the in-process hsg query cache — deleted memories remain retrievable for the process lifetime | author | **Assigned elsewhere** | assigned to @nullure | The issue is assigned to @nullure and has no unanswered maintainer reply; wait for implementation or a concrete question. |
| [plastic-labs/honcho#790](https://github.com/plastic-labs/honcho/issues/790)<br>Deleted workspace's search results keep being served from the redis cache until TTL; recreating the same workspace id resurrects them | author | **Issue open** | unassigned | No maintainer reply or assignment has landed; preserve the report and do not ping. |
| [shaneholloman/mcp-knowledge-graph#22](https://github.com/shaneholloman/mcp-knowledge-graph/issues/22)<br>Memories silently written to a global shared store when cwd lacks project markers — cross-project contamination by default; `--memory-path` ignored | author | **Issue open** | unassigned | No maintainer reply or assignment has landed; preserve the report and do not ping. |
| [akuity/kargo#6685](https://github.com/akuity/kargo/issues/6685)<br>Webhooks server (kubernetes-webhooks-server) is missing probe support that all other servers have | assignee | **Assigned** | assigned to @gnanirahulnutakki | Assigned implementation is valid, but hold publication while the global authored-PR cap is exceeded; recheck for competing work before resuming. |
| [kagent-dev/kagent#2303](https://github.com/kagent-dev/kagent/issues/2303)<br>A2A: report turn-total token usage on the terminal status update | participant | **Issue open** | unassigned | No maintainer reply, assignment, or competing implementation decision has landed; wait without pinging. |
| [PrefectHQ/fastmcp#2879](https://github.com/PrefectHQ/fastmcp/issues/2879)<br>Background job does not produce valid CreateTaskResult | participant | **Issue open** | unassigned | No author or maintainer reply followed the prior technical comment; retain as a watch-only legacy lane. |
| [argoproj/argo-cd#21059](https://github.com/argoproj/argo-cd/issues/21059)<br>CLI: add possibility to diff the desired state instead of the live state | participant | **Issue open** | unassigned | No author or maintainer reply followed the prior comment; retain as a watch-only legacy lane. |
| [argoproj/argo-cd#12273](https://github.com/argoproj/argo-cd/issues/12273)<br>Rework Credentials template url layout in Settings: Repositories | participant | **Issue open** | unassigned | No author or maintainer reply followed the prior comment; retain as a watch-only legacy lane. |

Last public state change recorded: **2026-07-28T02:28:48+00:00**.

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

The refresh records exact heads, draft state, base-branch drift, and whether
that drift requires action; detects active change requests on authored pull
requests; and surfaces only direct human mentions, replies to the contributor's
own review threads, or trusted linked-issue responses after the contribution
began. Base drift is bucketed instead of counted commit by commit, and optional
drift is kept distinct from repository-enforced branch updates to avoid
needless CI churn.
Active legacy pull requests and issue discussions remain visible even when they
predate the scorecard window. All open external authored pull requests count
against the simultaneous-work cap; only outcome metrics stay window-bounded.
The tracker also derives the next fresh-review eligibility boundary from
first-submission timestamps while leaving explicitly requested follow-ups
exempt. Bot-only pull-request timestamp churn is stabilized so it cannot create
synthetic tracker commits. The tracker never posts upstream comments.

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
