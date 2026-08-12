# Open Source Contribution Tracker

[![Validate tracker](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/ci.yml)
[![Daily refresh](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/update.yml)
[![Pages deployment](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/pages.yml/badge.svg)](https://github.com/gnanirahulnutakki/oss-contribution-tracker/actions/workflows/pages.yml)

A transparent, evidence-backed dashboard for my public open-source pull
requests, reviews, and issue lanes. The goal is sustained usefulness to
maintainers—not contribution-count inflation.

[View the live dashboard](https://gnanirahulnutakki.github.io/oss-contribution-tracker/)
or inspect every claim in this repository.

<!-- TRACKER:START -->
## 90-day scorecard

Program window: **2026-07-23 through 2026-10-20** (90 days). Outcome metrics include only new work from the program start; the authored-PR cap spans all active external work.

| Outcome | Current | Target | Progress |
|---|---:|---:|---|
| Merged external pull requests | 0 | 24 | 0% |
| Landing rate for decided PRs | — | 70% | No decided PRs yet |
| External pull requests reviewed | 27 | 12 | Target met |
| Simultaneous open authored PRs | 6 | ≤ 4 | Over cap |

Authored external PRs opened in this window: **5**. Administrative gates excluded from landing-rate decisions: **1**.

Fresh unsolicited review cadence: **eligible under the automated guardrail** (rolling 24-hour cap: 2; minimum spacing: 4 hours). Requested follow-ups remain evidence-driven and exempt.

## Tracked portfolio

| Contribution | Role | Stage | Verification signals | Next action |
|---|---|---|---|---|
| [prometheus/alertmanager#5402](https://github.com/prometheus/alertmanager/pull/5402)<br>victorops: use Splunk On-Call branding | author | **Awaiting CI approval** | 2 checks passed · workflow approval needed · base advanced &#40;update optional&#41; | Wait for maintainer workflow approval; do not ping prematurely. |
| [prometheus-community/postgres_exporter#1351](https://github.com/prometheus-community/postgres_exporter/pull/1351)<br>fix: preserve precision for large counters | author | **Changes requested** | 1 active change request · 1 check passed · workflow approval needed | Maintainer feedback on 9c8b1d9 required coverage in the active collector package. Rebased head 52cae0f now routes every Int64-backed collector counter through the shared precision policy, preserves the opt-out across normal and probe paths, and passes race tests, lint, Go 1.26 CI-equivalent gates, and live PostgreSQL 13.22/18.1 Docker scrapes. Wait for hosted CI and maintainer re-review without posting a status comment. |
| [PrefectHQ/fastmcp#4625](https://github.com/PrefectHQ/fastmcp/pull/4625)<br>fix: use Python field name for structured task results | author | **Closed** | 10 non-failing checks &#40;9 passed, 1 skipped&#41; · expected CI gate | Issue #4616 was closed by merged maintainer PR #4657; this administrative pull request remains closed. No follow-up is needed. |
| [open-telemetry/otel-arrow#3572](https://github.com/open-telemetry/otel-arrow/pull/3572)<br>fix&#40;filter&#41;: reject unknown config fields | author | **PR open** | 78 non-failing checks &#40;73 passed, 5 skipped&#41; · expected CI gate · base advanced &#40;update optional&#41; | Link and verify gnani.nutakki@gmail.com on GitHub, then complete EasyCLA; the PR is ready and twice approved with 73 passing and 5 skipped technical checks, but currently has no assignee. Do not post another routing comment before the legal gate is green. |
| [envoyproxy/gateway#9574](https://github.com/envoyproxy/gateway/pull/9574)<br>docs: explain backend protocol selection | author | **PR open** | 28 non-failing checks &#40;14 passed, 11 skipped, 3 neutral&#41; · base advanced &#40;update optional&#41; | Ready on unchanged head 12202063 after all 28 checks completed non-failing and Codex found no major issues. GitHub denied the fork author&#x27;s Copilot review request for lack of repository permission; wait for human review or a concrete request without pinging. |
| [oam-dev/cluster-gateway#171](https://github.com/oam-dev/cluster-gateway/pull/171)<br>fix&#40;proxy&#41;: enforce managed credential precedence | author | **PR open** | 8 checks passed | All eight checks pass and no review thread or maintainer reply is outstanding; wait without pinging. |
| [NousResearch/hermes-agent#10824](https://github.com/NousResearch/hermes-agent/pull/10824)<br>fix&#40;installer&#41;: reuse existing newer Python before downloading 3.11 | author | **PR open** | 38 non-failing checks &#40;27 passed, 10 skipped, 1 neutral&#41; · base advanced &#40;update optional&#41; | Head ce1cd22 is rebased onto current main, bounds reuse to &gt;=3.11,&lt;3.14, preserves UV_PYTHON repinning, and passes 41 shell-installer plus 13 contributor-mapping tests. The review thread is resolved and all 27 reporting CI checks pass; wait for maintainer re-review without pinging. |
| [NousResearch/hermes-agent#10828](https://github.com/NousResearch/hermes-agent/pull/10828)<br>fix&#40;runtime&#41;: auto-upgrade GPT-5 named custom providers to codex_responses | author | **Closed** | No checks reported | Closed after confirming model-only Responses inference conflicts with the current custom-provider compatibility policy; no follow-up is needed. |
| [NousResearch/hermes-agent#10852](https://github.com/NousResearch/hermes-agent/pull/10852)<br>fix&#40;gateway&#41;: keep auto vision preprocess concise | author | **Closed** | 38 non-failing checks &#40;26 passed, 11 skipped, 1 neutral&#41; | PR #10852 closed unmerged after collaborator @kshitijk4poor salvaged the concise-prompt change through merged PR #81269. Default-branch commit e6b16885 preserves Gnani&#x27;s authorship and all required Python, lint, attribution, supply-chain, and amd64/arm64 Docker checks passed. The maintainer intentionally omitted the token-cap plumbing to match project policy; the appreciative explanation asks no question, so no reply or follow-up is needed. |
| [prometheus-operator/prometheus-operator#8695](https://github.com/prometheus-operator/prometheus-operator/pull/8695#pullrequestreview-4769609444)<br>alertmanager: preserve top-level event_recorder configuration | reviewer | **Review submitted** | 22 non-failing checks &#40;21 passed, 1 skipped&#41; | Watch the unresolved TLS compatibility finding and respond if the author follows up. |
| [prometheus/client_golang#2062](https://github.com/prometheus/client_golang/pull/2062#pullrequestreview-4769888408)<br>api: return HTTP status on non-JSON API error bodies | reviewer | **Review submitted** | 15 non-failing checks &#40;14 passed, 1 skipped&#41; | Watch the valid-JSON error-envelope finding and re-review if the author updates the pull request. |
| [helm/helm#32339](https://github.com/helm/helm/pull/32339#pullrequestreview-4790630703)<br>fix&#40;scripts&#41;: add cache-busting to Helm version checks | reviewer | **Review landed** | 7 checks passed | Merged on exact reviewed head bc0114c at 2026-07-28T21:30:38Z after seven passing checks. A maintainer noted a possible dev-v3 backport but did not request action from this reviewer; do not reply or open follow-up work while over cap. |
| [openai/openai-agents-python#3933](https://github.com/openai/openai-agents-python/pull/3933#pullrequestreview-4776733214)<br>fix: enforce realtime text guardrails and synchronize streaming cancellation | reviewer | **Review complete** | 10 non-failing checks &#40;9 passed, 1 skipped&#41; | Closed unmerged on 2026-08-02. The maintainer&#x27;s request to stop posting general comments and identify only specific points is acknowledged; no reply or follow-up is warranted. |
| [google/adk-python#6459](https://github.com/google/adk-python/pull/6459#pullrequestreview-4790316157)<br>fix: route MCP calls to the .mtls.googleapis.com endpoint for Agent Identity | reviewer | **Review complete** | 23 non-failing checks &#40;19 passed, 4 skipped&#41; · expected CI gate | Closed unmerged after a maintainer confirmed the endpoint rewrite already occurs in _get_connection_uri&#40;&#41;. The explanation is specific and requires no reviewer reply or replacement pull request. |
| [google/adk-python#6460](https://github.com/google/adk-python/pull/6460#pullrequestreview-4776004279)<br>fix&#40;litellm&#41;: strip embedded thought_signature from tool call id | reviewer | **Review update available** | 6 non-failing checks &#40;2 passed, 4 skipped&#41; · expected CI gate · 1 failing · workflow approval needed | Head 7c6904ab still has the unresolved empty embedded-signature ID finding; the failing agent-triage run is an unrelated Gemini 503 and CLA remains the expected gate. Do not duplicate the inline finding; re-review only after a substantive author update. |
| [pydantic/pydantic-ai#6706](https://github.com/pydantic/pydantic-ai/pull/6706#pullrequestreview-4770938242)<br>Validate native tool IDs per capability layer | reviewer | **Review update available** | 65 non-failing checks &#40;48 passed, 16 skipped, 1 neutral&#41; | Exact head a51fa5e7 still rejects conflicting native tools returned by a factory inside CombinedCapability even though the same tools override as separate run-level entries. Seven focused and 417 full agent tests pass, but the validation-boundary contract remains unresolved; GitHub returned &#x27;User is blocked&#x27; when the proof-backed follow-up was submitted, so do not retry through another channel unless access changes or a maintainer contacts us. |
| [microsoft/agent-framework#7292](https://github.com/microsoft/agent-framework/pull/7292#pullrequestreview-4776007573)<br>Python: &#91;Feature&#93;: Support OpenAI instructions in Responses API | reviewer | **Review landed** | 37 non-failing checks &#40;23 passed, 14 skipped&#41; | Merged on head 8a6a52c9 after two maintainer approvals and 37 non-failing checks &#40;23 passed, 14 skipped&#41;; no follow-up required. |
| [microsoft/autogen#7994](https://github.com/microsoft/autogen/pull/7994#pullrequestreview-4801249949)<br>fix&#40;autogen-ext&#41;: skip LangChain callback-manager &#40;run_manager&#41; when inferring tool args schema | reviewer | **Review submitted** | 2 checks passed · workflow approval needed | Answered the author&#x27;s concrete re-review question at issuecomment-5173162647: head 7b5e64de is unchanged from the independently tested and approved commit, so the existing approval still applies. Wait for maintainer workflow approval or a substantive new head. |
| [crewAIInc/crewAI#6625](https://github.com/crewAIInc/crewAI/pull/6625#pullrequestreview-4771496651)<br>fix&#40;reasoning&#41;: use flexible regex to detect READY state to prevent agent deadlocks | reviewer | **Review submitted** | 1 check passed · workflow approval needed | Watch the semantic readiness-marker finding and re-review after the author updates head d2c0b593. |
| [huggingface/smolagents#2565](https://github.com/huggingface/smolagents/pull/2565#pullrequestreview-4849687654)<br>fix: filter TOOL_CALL and TOOL_RESPONSE messages from managed-agent summary | reviewer | **Review submitted** | workflow approval needed | Approved exact head 2d0a0317 after the author removed ActionStep serialization from managed summaries: raw tool arguments, observations, and images are never accessed, an adversarial raising-object probe passed, all eight focused regressions pass, and make quality is clean. Hosted workflows still await repository authorization; wait for maintainer action or another substantive head. |
| [strands-agents/harness-sdk#3448](https://github.com/strands-agents/harness-sdk/pull/3448#pullrequestreview-4782383330)<br>feat&#40;graph&#41;: add Python concurrency limit | reviewer | **Review update available** | 7 non-failing checks &#40;6 passed, 1 skipped&#41; · 3 pending · workflow approval needed | Re-reviewed the substantive delta through head 0cdaaee7 with no code or documentation finding: 100 graph tests pass, the new queue-timeout test passed 100 repetitions, all execution-timeout combinations passed 100 repetitions, and Ruff/mypy are clean. Exact-head hosted jobs still await manual authorization, so keep the prior approval stale and re-approve only after the Windows matrix is green. |
| [openai/openai-python#3538](https://github.com/openai/openai-python/pull/3538#pullrequestreview-4776232747)<br>fix&#40;streaming&#41;: return final response for incomplete and failed events | reviewer | **Review submitted** | workflow approval needed | The incomplete/failed structured-output fix is verified on head e896c03a; wait for maintainer review or another head update. |
| [langchain-ai/deepagents#5026](https://github.com/langchain-ai/deepagents/pull/5026#pullrequestreview-4849693821)<br>fix&#40;sdk&#41;: make `BackendProtocol.glob` recursive for bare patterns | reviewer | **Review update available** | 80 non-failing checks &#40;53 passed, 27 skipped&#41; · 4 failing | Head f12a2ed only merges current main into the branch; no author response or substantive fix followed, and the existing &#123;&#123;a,b&#125;&#125;.py backend disagreement plus Windows path-normalization failure remain. The prior proof-backed COMMENT review still applies, so do not re-review until a substantive fix or concrete author question arrives. |
| [sgl-project/sglang#32344](https://github.com/sgl-project/sglang/pull/32344#pullrequestreview-4776140668)<br>&#91;Bugfix&#93; Emit cached token metric before first cache hit | reviewer | **Review submitted** | 85 non-failing checks &#40;6 passed, 79 skipped&#41; · expected CI gate | Watch the PromQL label-set mismatch finding on head 94b638a4; re-review after the metric schema or query and regression coverage are corrected. |
| [browser-use/browser-use#5300](https://github.com/browser-use/browser-use/pull/5300#pullrequestreview-4776211914)<br>Call the model with minimal state after capture timeout | reviewer | **Review landed** | 96 non-failing checks &#40;94 passed, 2 skipped&#41; | Watch for author or maintainer follow-up and re-review only if the head changes or a concrete timeout-safety question is raised. |
| [modelcontextprotocol/typescript-sdk#2544](https://github.com/modelcontextprotocol/typescript-sdk/pull/2544#pullrequestreview-4776312162)<br>Fix tests timing out during interactive OAuth flow &#40;#2510&#41; | reviewer | **Review submitted** | 10 non-failing checks &#40;9 passed, 1 skipped&#41; · 7 failing | Re-reviewed exact head 4dbb8a03. The successful REDIRECT path works and 81 focused tests pass, but an error-shaped OAuth callback rejects finishAuth while leaving the triggering request pending until close&#40;&#41;; five required checks are also branch-caused. GitHub denied a formal changes-requested review without explicit access, so a proof-backed COMMENT review was submitted and the original P1 thread remains unresolved. Re-review only after failure-path settlement and CI fixes. |
| [confident-ai/deepeval#2950](https://github.com/confident-ai/deepeval/pull/2950#discussion_r3708697090)<br>fix&#40;openai&#41;: apply prompt-caching discount to GPTModel cost calculation | reviewer | **Review submitted** | 12 checks passed · expected CI gate · 2 failing | Re-tested exact head a2758d42 and replied in the existing unresolved thread. Standard cached rates are fixed, but fully cached 300K-token GPT-5.4 input returns $0.075 instead of the documented $0.15 because the &gt;272K long-context multiplier is absent; the same reproduces on current main and 52 affected tests pass without a boundary regression. Wait for a substantive fix; lint is current-main drift and Vercel needs team authorization. |
| [traceloop/openllmetry#4375](https://github.com/traceloop/openllmetry/pull/4375#pullrequestreview-4776934105)<br>fix&#40;cohere&#41;: avoid double-ending async error spans | reviewer | **Review submitted** | 3 checks passed · workflow approval needed | Watch the duplicate exception-event finding on head 9c303fd1; re-review after one layer owns exception recording and the regression asserts exact cardinality. |
| [Arize-ai/openinference#3429](https://github.com/Arize-ai/openinference/pull/3429#pullrequestreview-4787290072)<br>fix&#40;anthropic&#41;: preserve APIPromise helpers | reviewer | **Review landed** | 23 non-failing checks &#40;14 passed, 9 skipped&#41; | Merged on 2026-08-06 at default-branch commit 7ea68f72 after the consumed asResponse body finding was fixed and re-approved with all hosted checks non-failing. No reply or follow-up is needed. |
| [AgentOps-AI/agentops#1428](https://github.com/AgentOps-AI/agentops/pull/1428#pullrequestreview-4780556283)<br>fix&#40;langchain&#41;: capture structured output tool calls | reviewer | **Review submitted** | 1 check passed · workflow approval needed | Structured-output capture is reproduced and approved on head 85f6896; wait for maintainer review, CI authorization, or a new head. |
| [agno-agi/agno#9174](https://github.com/agno-agi/agno/pull/9174#pullrequestreview-4781165073)<br>refactor: cache the pydantic version across tool wrappers | reviewer | **Review complete** | 7 non-failing checks &#40;5 passed, 2 skipped&#41; · 7 failing | Closed as superseded after #9210 landed the same cache on main. The author acknowledged the independent validation and asked no question; no reply or re-review is warranted. |
| [omnigent-ai/omnigent#3304](https://github.com/omnigent-ai/omnigent/pull/3304#pullrequestreview-4783071226)<br>fix&#40;accounts&#41;: enforce the last-admin invariant atomically on delete | reviewer | **Review landed** | 68 non-failing checks &#40;60 passed, 8 skipped&#41; | Merged on exact reviewed head bb2ca4c at 2026-07-29T00:07:09Z after maintainer approval and 68 non-failing checks &#40;60 passed, 8 skipped&#41;. The approval thanked the contributor but asked no question; no reply is warranted. |
| [opensquilla/opensquilla#815](https://github.com/opensquilla/opensquilla/pull/815#pullrequestreview-4849838477)<br>fix&#40;engine&#41;: evict cache-break monitor state for terminal sessions | reviewer | **Review landed** | 27 non-failing checks &#40;22 passed, 5 skipped&#41; | Merged on 2026-08-06 at default-branch commit 0acd578e after the cache-break fix was re-approved with 19 focused tests, Ruff, mypy, and all hosted checks non-failing. No reply or follow-up is needed. |
| [agentscope-ai/agentscope#1874](https://github.com/agentscope-ai/agentscope/pull/1874#pullrequestreview-4792240922)<br>fix&#40;embedding&#41;: omit default OpenAI dimensions | reviewer | **Review submitted** | 6 checks passed | Approved exact head de155d7e after both P2 findings were fixed: explicit pass_dimensions precedence is preserved and genuine multi-type anyOf schemas remain intact. Twelve focused tests, the 33-test provider slice, all file-scoped hooks, and all six hosted checks pass. Wait for maintainer action or another substantive head. |
| [tma1-ai/tma1#73](https://github.com/tma1-ai/tma1/pull/73#pullrequestreview-4801192177)<br>chore&#40;deps&#41;: Bump sharp and astro in /site | reviewer | **Review submitted** | 1 check passed | Exact head afa47ab builds on Node 22.12.0 and preserves the three localized page contracts, but the lockfile still installs sharp 0.34.5 and leaves GHSA-f88m-g3jw-g9cj present. One file-level finding is open; wait for a head update or concrete reply without duplicating it. |
| [kserve/kserve#5917](https://github.com/kserve/kserve/pull/5917#pullrequestreview-4849628354)<br>fix: select compatible LocalModelNodeGroup instead of blindly picking &#91;0&#93; | reviewer | **Review submitted** | 5 checks passed · workflow approval needed | Re-reviewed exact head 4c1d4529 after the RBAC and generated-manifest update: controller-gen, Helm, Kustomize, all 12 quick-install outputs, 21 validators, race tests, compile/vet, chart lint, and diff checks pass. GitHub denied a formal approval because the account lacks explicit repository access, so a proof-backed COMMENT review was submitted; wait for maintainers to authorize the remaining action_required workflows. |
| [oam-dev/cluster-gateway#170](https://github.com/oam-dev/cluster-gateway/issues/170)<br>Security: managed credential must override inbound Authorization on proxy requests | author | **Issue open** | unassigned | The linked implementation PR is green; wait for maintainer review without a status ping. |
| [CaviraOSS/OpenMemory#186](https://github.com/CaviraOSS/OpenMemory/issues/186)<br>`delete_all` removes DB rows but not the in-process hsg query cache — deleted memories remain retrievable for the process lifetime | author | **Assigned elsewhere** | assigned to @nullure | Resolved upstream by merged competing PR #190, which added cache clearing directly. The issue remains open and assigned elsewhere, but no implementation or reply is owed from this contributor. |
| [plastic-labs/honcho#790](https://github.com/plastic-labs/honcho/issues/790)<br>Deleted workspace&#x27;s search results keep being served from the redis cache until TTL; recreating the same workspace id resurrects them | author | **Issue open** | unassigned | No maintainer reply or assignment has landed; preserve the report and do not ping. |
| [shaneholloman/mcp-knowledge-graph#22](https://github.com/shaneholloman/mcp-knowledge-graph/issues/22)<br>Memories silently written to a global shared store when cwd lacks project markers — cross-project contamination by default; `--memory-path` ignored | author | **Issue open** | unassigned | No maintainer reply or assignment has landed; preserve the report and do not ping. |
| [akuity/kargo#6685](https://github.com/akuity/kargo/issues/6685)<br>Webhooks server &#40;kubernetes-webhooks-server&#41; is missing probe support that all other servers have | assignee | **Assigned** | assigned to @gnanirahulnutakki | A private, uncommitted implementation is fully qualified on base a8df2f95; current main d30e014 changes only an unrelated design document. In addition to full race tests, Go lint, 151 chart tests, chart lint, generated docs, and strict manifest validation, the exact built image sha256:eaab195d887f reached Ready in disposable kind v1.34: /healthz reported ping, /readyz reported webhook-server, both returned HTTP 200, restart count stayed zero, logs had no TLS-probe noise, read-only Freight/Stage cache RBAC was sufficient, and all 11 rolling-restart samples retained a ready Service endpoint. The cluster, TLS material, and image were removed. Keep it unpublished at 6/4; recheck live assignment, competing work, main, and capacity before committing. |
| [kagent-dev/kagent#2303](https://github.com/kagent-dev/kagent/issues/2303)<br>A2A: report turn-total token usage on the terminal status update | participant | **Issue open** | unassigned | Issue author @QuentinBisson opened the exact implementation as draft PR #2332 on 2026-07-25; do not implement, claim, review, or comment. Remove this lane from the candidate queue unless a maintainer makes a concrete request. |
| [PrefectHQ/fastmcp#2879](https://github.com/PrefectHQ/fastmcp/issues/2879)<br>Background job does not produce valid CreateTaskResult | participant | **Issue open** | unassigned | No author or maintainer reply followed the prior technical comment; retain as a watch-only legacy lane. |
| [argoproj/argo-cd#21059](https://github.com/argoproj/argo-cd/issues/21059)<br>CLI: add possibility to diff the desired state instead of the live state | participant | **Issue open** | unassigned | Maintainer PR #27469 implements this lane. Its current head has older approvals and green completed checks but is now dirty and review-required; preserve the prior report, do not compete, and do not comment unless a maintainer asks a concrete question. |
| [argoproj/argo-cd#12273](https://github.com/argoproj/argo-cd/issues/12273)<br>Rework Credentials template url layout in Settings: Repositories | participant | **Issue open** | unassigned | Our implementation PR #27415 was self-closed and later competing attempts also closed. Keep this as watch-only legacy context; do not revive it without fresh maintainer intent and current reproduction. |
| [NousResearch/hermes-agent#10695](https://github.com/NousResearch/hermes-agent/issues/10695)<br>Python dependency CVEs: aiohttp, cryptography, curl-cffi need minimum version bumps | participant | **Issue closed** | unassigned | Closed after alternative PR #26830 merged. The maintainer explicitly credited this contributor&#x27;s audit; no reply or replacement work is needed. |
| [meshery/meshery#18739](https://github.com/meshery/meshery/issues/18739)<br>&#91;UI&#93; Replace direct MUI imports in dashboard surfaces | assignee | **Issue closed** | assigned to @leecalcote, @gnanirahulnutakki | Closed after maintainer PR #19306 merged and credited this contributor&#x27;s initial PR #18770. No reply or competing implementation is needed. |
| [akuity/kargo#6021](https://github.com/akuity/kargo/issues/6021)<br>feat: add gitea label support | participant | **Issue closed** | assigned to @fuskovic | Closed after maintainer PR #6262 merged; this contributor&#x27;s earlier PR #6101 was self-closed. No follow-up is needed. |
| [kitops-ml/kitops#1138](https://github.com/kitops-ml/kitops/issues/1138)<br>Set org.opencontainers.image.created annotation on ModelKit manifests | participant | **Issue closed** | unassigned | Closed after competing PR #1139 merged on 2026-05-11; this contributor&#x27;s PR #1164 must remain closed and no reply is needed. |
| [MemoriLabs/Memori#590](https://github.com/MemoriLabs/Memori/issues/590)<br>Self-hosted &#40;BYODB&#41; usage: `capture_agent_turn&#40;&#41;` POSTs to the cloud API, and `Memori&#40;conn=...&#41;` never provisions the schema — both undocumented | author | **Issue closed** | unassigned | Closed after the current-version clarification. The later DevRel Discord invitation contains no technical question, so no public reply or issue revival is warranted. |
| [basicmachines-co/basic-memory#944](https://github.com/basicmachines-co/basic-memory/issues/944)<br>CLI `write-note` &#40;and other `tool` subcommands&#41; crash with `&#x27;function&#x27; object has no attribute &#x27;fn&#x27;` — no resolvable fastmcp version satisfies the 0.16.2 CLI bridge | author | **Issue closed** | unassigned | Closed after the maintainer confirmed the behavior is fixed in current releases. Maintainer-authored issue #1181 later cross-referenced #944 only as an older resolved FastMCP 2.x/3.x pin issue that does not overlap the FastMCP 4 beta port; the non-actionable reference is acknowledged and requires no reply or revival. |
| [kagent-dev/kagent#1037](https://github.com/kagent-dev/kagent/issues/1037)<br>feat: add support for Docker images and kmcp projects for local dev | participant | **Issue closed** | unassigned | Closed by the stale bot on 2026-06-23 without a maintainer response. Do not revive the old claim without current reproduction and renewed maintainer intent. |
| [letta-ai/letta#3364](https://github.com/letta-ai/letta/issues/3364)<br>BYOK OpenAI-compatible provider: handle is generated under `openai-proxy/...` but validated against the provider name → 400, or unhandled `AssertionError` → opaque 500 | author | **Issue closed** | unassigned | Automatically closed and locked for missing the repository&#x27;s required human-verification and AI-policy template. Do not reopen or repost without a fresh reproduction and full policy compliance. |

Last public state change recorded: **2026-08-12T00:01:07+00:00**.

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
synthetic tracker commits. Human-reviewed, non-actionable response signals can
be acknowledged per contribution without suppressing later activity. The
tracker never posts upstream comments.

For snapshot compatibility, `checks.passing` keeps its original meaning:
successful, skipped, and neutral checks. Consumers that need exact evidence
should use `checks.successful` for successful checks and `checks.non_failing`
for the explicit aggregate.

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
