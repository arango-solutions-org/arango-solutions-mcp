# SOTA MCP Competitive Scorecard

**Product:** ArangoDB MCP Server<br>
**Assessment date:** August 6, 2026 (full assessment); revised September 29, October 5 and October 21, 2026<br>
**Repository baseline:** `main` at `363a7cb` (the MCP SDK 2.x migration, [#28](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/28), and the CodeQL triage, [#30](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/30), merged October 21), no release tag. The history was rewritten on October 5 to purge a leaked credential, so commit ids quoted from before then belong to the rewritten history<br>
**Product version:** 2.0.0 (`pyproject.toml:3`, `src/arangodb_mcp/config.py:76`); next release is v3.0.0

**Revision — October 21, 2026 (P0 closed): 82/100 — B+ (was 81).** The three P0 items that were
still open earlier on October 21 are now complete. Each was verified externally, from the GitHub API
or from CI on `main`.

- `[V]` **CodeQL: 0 open alerts on `main`.** All 12 alerts ever raised are resolved.
  - 7 are fixed. In [#30](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/30), the
    confirmation-token parameter digest became an HMAC keyed with the confirmation secret (token
    version 2), the redacted log lines got a SHA-256 correlation prefix, and the test port probe binds
    to loopback.
  - 5 are dismissed with recorded reasons. Four clear-text-logging alerts have a data flow that starts
    at a test fixture named `secret`. The fifth is CodeQL's password-storage heuristic firing on the
    keyed HMAC.
- `[V]` **`main` is protected,** confirmed by reading the protection back from the API.
  - 10 required checks: every CI and Security job.
  - Branches must be up to date and changes must come through pull requests, enforced for admins.
  - Force pushes and deletion are disallowed.
  - [Issue #6](https://github.com/arango-solutions-org/arango-solutions-mcp/issues/6) is closed. No
    approving review is required, a maintainer decision while there is a single active maintainer.
- `[V]` **Dependabot security alerts and security updates are enabled,** with 0 open alerts.
- `[V]` **The pipeline is green:** CI 6/6 and Security 4/4 on `main` at `363a7cb`.

Ecosystem and release maturity returns from **4 to 5**, its August level, because every adverse item
behind the September 29 drop is now resolved with external evidence. It goes no higher: there is still
no release, and adoption is 3 stars and 0 forks. PRD requirements REL-001 and REL-002 move from
PARTIAL to CURRENT. Still `[U]`: revocation of the leaked key by its owner, and GitHub's purge of the
old pull-request refs.

**Revision — October 21, 2026: 81/100 — B+ (unchanged).** The pipeline went from red to fully
green, and three newly published dependency advisories were each fixed within a day. The score holds
because the "green **and enforce**" P0 item is only half done. All of the following is verified on
GitHub runners unless marked otherwise.

- `[V]` **`main` is fully green for the first time since August 8.** CI is 6/6 jobs and Security
  4/4, as of `8e4d1fb`. The Lint job had stopped at `ruff check` on vendored `.cursor/hooks/` files,
  which **skipped six later gates on every run**: format, doc consistency, the quality gates, mypy,
  the lockfile check and the wheel smoke test. Excluding the vendored hooks from ruff
  ([#26](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/26)) means all six now run.
- `[V]` **Dependency advisories, fixed as they appeared:**
  - `mcp` 1.30.0 for GHSA-84m7-p3x7-pcfv (unbounded Streamable HTTP sessions), in #26.
  - certifi 2026.10.19 for GHSA-6q48-6c7w-9gw2 (critical: a trusted root with compromised
    intermediates), in [#27](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/27).
    A local audit caught this before CI's scanners carried the advisory. All of the server's HTTPS
    trust (OIDC/JWKS, embeddings, ArangoDB) depends on that bundle.
  - PyJWT 2.15.1 and urllib3 2.8.0 earlier, on October 5.
- `[V]` **A release-blocking defect was found and fixed.** `release.yml` re-verified the published
  wheel against 81 tools while the catalog has 83, so the first tagged release would have failed.
  `verify_docs.py` now checks every hardcoded copy of the count (#26).
- `[V]` **Runtime and supply chain:**
  - The image runs Python 3.14, and CI now tests 3.10, 3.11 and 3.14.
  - Both Trivy exceptions are retired; the 3.14 base no longer ships setuptools, and a scan without
    the ignore file finds nothing.
  - Major-version Dependabot updates now arrive as separate PRs instead of blocking grouped ones.
  - These landed in [#24](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/24) and
    this revision's PR.
- `[V]` **MCP Python SDK 2.x**, merged October 21 (#28).
  - Protocol 2026-07-28 is supported natively, including its stateless core: there is no
    `initialize`, and clients use `server/discover`. The 1.x bridge is gone.
  - Verified with a stdio client handshake, the live OIDC harness and a kind install/upgrade.
  - The migration also fixed a latent cache defect: `tools/list` was marked `public`, meaning
    shareable across authorization contexts, while under OIDC each caller's list is filtered by its
    token scopes. It is now `private`.

**Still open, so the P0 item stays incomplete:**
- `[V]` 7 CodeQL alerts (6 high) are open and untriaged, up from 5.
  - The four clear-text-logging alerts are the opt-in `LOG_AQL_QUERIES` debug path; the profiling
    tools added two of those call sites.
  - One weak-hashing alert is a SHA-1 log-correlation ID.
  - The other is the SHA-256 parameter digest in confirmation tokens, which could be HMAC-keyed.
  - The medium alert is a test-only socket bind.
  - None is dismissed with a reason.
- `[V]` `main` is unprotected
  ([issue #6](https://github.com/arango-solutions-org/arango-solutions-mcp/issues/6)), and Dependabot
  security alerts are disabled.
- `[V]` There is no release, and adoption is 3 stars and 0 forks.
- `[U]` For the leaked key: GitHub has not yet purged the old pull-request refs, and its owner has not
  confirmed revocation.

**Revision — October 5, 2026: 81/100 — B+ (unchanged).** The external results the September 29
revision scored against have partly recovered, all verified on GitHub runners against `998153d`:

- `[V]` **Secret scanning passes for the first time on this branch.** `.env` was removed from the
  entire Git history of both repositories. No branch on either remote contains the key, and a
  fresh clone finds zero copies. The one remaining finding was a made-up test password, now
  recorded with a reason in `.gitleaksignore` (`.github/workflows/security.yml:32`).
- `[V]` **The dependency audit and container scan pass again.** Newly published advisories (13
  in PyJWT 2.13.0, one CRITICAL, in the authentication-bypass and token-forgery classes; 3 in
  urllib3 2.7.0) were fixed the day they surfaced by upgrading to PyJWT 2.15.1 and urllib3 2.8.0.
  The declared PyJWT floor is now `^2.15.1` (`pyproject.toml:28`), and pip-audit went from 16
  findings to 0. PyJWT backs OIDC token validation, so the live OIDC integration (signed JWTs from
  a reference IdP) was re-run and passes locally and in CI.
- `[V]` **The whole Security workflow is green** (secret scan, dependency audit, container scan,
  CodeQL analysis), as are both test jobs (487 passed; 82.40%/82.21% coverage), Helm/kind, and
  the Phase 4 OIDC/telemetry integration.

**Why the score does not move yet.** The P0 gap is "green **and enforce** the external pipeline".
Lint still fails, on four `SIM105` findings in `.cursor/hooks/` (dev tooling, not product code).
Five CodeQL alerts are still open and untriaged, `main` is still unprotected, and Dependabot
security alerts are still off. Restoring the maturity point needs the whole P0 row, not part of
it. Two further items sit outside the repository: GitHub Support must purge 12 read-only
pull-request refs that still reach the old history, and the key's owner has not yet confirmed
revocation.

**Revision — September 29, 2026: 81/100 — B+ (was 82).** This revision re-audited the code and,
for the first time, captured the **external** CI and security results that the August assessment
left `[U]`. Code gains since August — a 3.12.x AQL manual update, two clean-room query-profiling
tools (catalog 81 → 83), a Helm `startupProbe`, and a trivyignore refresh — are recorded but do not
move any category score. The external results **are** scored, because the rubric credits gains only
on external evidence but applies adverse external evidence immediately:

- `[V]` The branch's CI has **not passed in full on any push since August 8**. Lint fails on four
  `SIM105` findings in `.cursor/hooks/` shared-memory tooling (not product code). The Docker-backed
  test jobs pass externally (486 of 487 on the latest push, at 82.40%/82.21% coverage on Python
  3.10/3.11). The one failure was a regression introduced at `a2bd938`, fixed on September 29.
- `[V]` Full-history secret scanning failed on a third-party API key committed in the initial
  import's `.env`, and on a test-fixture false positive. *(Remediated October 5, 2026:* `.env`
  was removed from the entire Git history, so the key is no longer in any branch. The false
  positive is recorded with a reason in `.gitleaksignore`, and the secret scan now passes in
  CI. Revocation by the key's owner and GitHub's purge of old pull-request refs are still
  pending.)
- `[V]` CodeQL analysis runs, but **5 alerts remain open and untriaged**: 3× high
  `py/clear-text-logging-sensitive-data` and 1× high `py/weak-sensitive-data-hashing` in the AQL
  log-redaction path, and 1× medium `py/bind-socket-all-network-interfaces` in `tests/conftest.py`.
- `[V]` `main` has no branch protection. Dependabot *security* alerts are disabled for the
  repository. Three Dependabot update PRs (#8, #16, #18) are open and unmerged.
- `[V]` There is still no release, while Neo4j (v1.6.0), MongoDB (v2.1.2), DBHub (v1.4.0), and
  Neptune (PyPI 1.1.1) have all shipped releases since August.

Ecosystem and release maturity therefore moves from **5 to 4**. Every other category is unchanged.
The ranking is unchanged (#2, one point above DBHub). The fastest recovery is operational rather
than engineering: green the whole pipeline, triage CodeQL, revoke and resolve the leaked
credential, protect `main`, merge PR #7, and cut v3.0.0. *(October 5: the history purge and
false-positive record are done; confirming key revocation remains.)*

**Revision — August 14, 2026:** The Phases 1–5 worktree this scorecard assessed was **committed**
(`3256f93`, Aug 7) and pushed to `origin/phase1/platform-spine`, with a breaking-changes changelog
(`5bd06b1`, Aug 8); latest activity is Aug 8, 2026. Version remains `2.0.0`, but `CHANGELOG.md`
records **two breaking client-facing changes** (the `main.py` → `arangodb-mcp` launch entrypoint,
and the `readonly` default profile that gates the `memory` toolset), so the next release is a major
**v3.0.0**. The **82/B+** score is unchanged: the external gates it depends on — merge to `main`,
published signed PyPI/GHCR artifacts, a 30-day green operational window, and the independent MAT-003
regrade — remain unmet (no release tag exists). This revision corrects temporal/state framing only;
category scores and evidence are otherwise as of the August 6 assessment.

## Executive verdict

**Overall: 82/100 — B+** (October 21 revision, after the P0 item closed; 81 from September 29 to October 21; 82 at the August 6 assessment)

This server is the **functional-breadth leader** in the comparison: its 83 verified tools cover
documents, graphs, AQL (including measured query profiling and proven-equivalence query
comparison), search, vectors, transactions, cluster administration, backups, users, permissions,
embeddings, and shared memory (`src/arangodb_mcp/server.py:18-66`, `tests/test_mcp_e2e.py:59-63`).
No peer in this scorecard matches that native multi-model and administrative surface.

It exceeds Neo4j's 77-point benchmark through a compact readonly default, catalog-driven policy,
parser-backed AQL safety, human confirmations, current stateless protocol behavior, MCP resources
and prompts, and blocking quality gates. Phases 4 and 5 now add local OIDC authority intersection,
request-scoped credentials, Prometheus/OpenTelemetry/audit controls, package and immutable-image
gates, a release workflow, and a supported Helm deployment. Those improvements do not justify a
self-awarded score increase. The largest remaining deficits are:

1. the legacy shared-token compatibility mode still maps to one configured database identity;
2. no PyPI wheel, GHCR digest, SBOM, signature, or provenance attestation is externally published;
3. required CI/branch-protection and interoperability evidence remains incomplete;
4. governance files are committed on the branch but not yet merged to `main` or in a public release;
5. MAT-003 still requires an independent regrade after at least 30 days of green operational,
   release, interoperability, and external-use evidence;
6. *(September 29)* the external pipeline is red: CI has not fully passed since August 8, secret
   scanning flagged a committed credential (purged from history October 5, external confirmation
   pending), and 5 CodeQL alerts (4 high) are open and untriaged.

The defensible market position is:

> **The broadest ArangoDB-native MCP control plane, with strong locally verified identity,
> observability, package, and Helm foundations, while published distribution, independently
> observed operations, and release/adoption maturity still trail the production leaders.**

### Change since the August 14 revision

- `[V]` Two new developer-tier AQL tools, `profile-aql-query` and `compare-aql-queries`
  (`src/arangodb_mcp/mcp_tools/aql_tools.py:165`, `src/arangodb_mcp/mcp_tools/aql_tools.py:211`),
  take the catalog from 81 to 83 (`src/arangodb_mcp/catalog/tools.yaml:18-19`, `PRD.md:135-145`).
  Profiling returns measured time, memory, plan, indexes, optimizer rules, and scan statistics.
  Comparison proves that candidate queries return the same result **multiset** (order-independent
  canonical per-row SHA-256 digests) before ranking them by speed, and warns loudly on divergence
  (`src/arangodb_mcp/agents/aql_execution_agent.py:35-83`,
  `src/arangodb_mcp/agents/aql_execution_agent.py:436-493`).
- `[V]` Both tools execute queries, so they reuse the parser-backed classifier and reject any
  non-read query with `aql_policy_denied` before execution. They are gated `operation: write`, so
  they appear only in `developer`+ profiles, in line with `execute-aql-query`. The readonly
  default is still 17 tools and 8,293 estimated tokens. Seven tests cover this, including
  row-order equivalence, divergence, and mutation refusal (`tests/test_agents.py:523-670`).
- `[V]` The capability was inspired by a sibling ArangoDB team's server. It was implemented
  clean-room from a behavioral spec by an implementer with no access to that source, and a first
  derivative attempt was discarded before commit (commit `145f140` records the provenance).
- `[V]` The served AQL reference now covers 3.12.x syntax: inline `FILTER` in array expansion,
  `UPSERT` filter matching, `readOwnWrites`, destructuring, and new functions (`dcdb917`).
- `[V]` The Helm chart gains an optional `startupProbe` on `/readyz` with a 90-second default
  budget. It is schema-validated and passes lint, kubeconform, and kind smoke in CI
  (`deploy/helm/arangodb-mcp/templates/deployment.yaml:187-193`,
  `deploy/helm/arangodb-mcp/values.yaml:166`).
- `[V]` A startup database connect can no longer block the MCP protocol handshake (`67b4e18`).
- `[V]` Trivy suppressions were re-audited. The setuptools false positive was re-verified and
  extended. The stale msgpack suppression was removed, and the external container scan still
  passes without it. The security contract test now pins the policy structurally instead of
  pinning an already-expired date (`tests/test_security_contract.py:50-75`).
- `[V]` **External CI captured.** Tests, Helm/kind, the Phase 4 OIDC/telemetry integration,
  CodeQL analysis, and the container scan pass on GitHub runners. Lint, secret scanning, and
  (before the September 29 fix) the tests and dependency audit fail. Five CodeQL alerts are open.
  `main` is unprotected and no release exists (see the September 29 revision note).

### Change since the prior baseline

- `[V]` Contributor PR [#2](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/2)
  corrected a multi-writer data-integrity defect: `save-pattern(force=true)` now preserves the
  caller's "genuinely distinct" ruling instead of implicitly superseding a near-duplicate
  (`src/arangodb_mcp/mcp_tools/pattern_memory_tools.py:131-145`, `src/arangodb_mcp/mcp_tools/pattern_memory_tools.py:172-183`).
- `[V]` Two regression tests pin both sides of the invariant: forced saves do not supersede, while
  ordinary near-duplicates still do (`tests/test_pattern_memory_tools.py:295-325`).
- `[V]` PRD item P-2 now distinguishes implicit superseding from explicit replacement
  (`PRD.md:270`).
- `[V]` At the prior `99a53c2` baseline, the two Docker-backed CI test jobs passed on Python 3.10
  and 3.11, but the lint job failed on a pre-existing Ruff import-order violation
  ([CI run](https://github.com/arango-solutions-org/arango-solutions-mcp/actions/runs/31053199522)).
- `[V]` Phase 0 established 44 stable, owned, evidence-gated v3 requirements in the PRD and
  replaced the blanket implementation claim with requirement-level states (`PRD.md:39-55`,
  `PRD.md:367-473`).
- `[V]` The Compose path now requires independent MCP/database secrets, enables vector indexes,
  provides working dependency and container health checks, and initializes the database connector
  for HTTP service startup (`docker-compose.yml:1-40`, `Dockerfile:20-28`,
  `src/arangodb_mcp/main.py:130-144`).
- `[V]` A clean live smoke test reached healthy ArangoDB and MCP containers, returned HTTP 200 from
  `/healthz`, rejected an unauthenticated MCP request with 401, and created a vector index.
- `[V]` The latest completed local suite is green at 480 tests and 82.64% measured coverage; Ruff,
  formatting, Mypy, and the enforced 79% coverage floor also pass.
- `[V]` Dependabot covers Python, Actions, and Docker dependencies. CodeQL, exception-free
  dependency audit, full-history secret scanning, and built-image vulnerability gates are
  configured; the unused vulnerable `fastmcp` package was removed.
- `[V]` A new CI gate derives the registered tool count, test-function count, configuration
  variables, and source inventories from executable code and rejects stale README, PRD, or
  scorecard claims (`scripts/verify_docs.py:19-109`, `.github/workflows/ci.yml:43-44`).
- `[V]` A pinned ArangoDB Starter deployment was exercised locally with three agents, DBServers,
  and coordinators; the corrected cluster tier passed 4 tests with one Community-edition skip.
  The same deployment is now scheduled nightly (`tests/test_cluster.py:17-63`,
  `.github/workflows/cluster-nightly.yml:1-113`).
- `[V]` A canonical policy catalog (81 tools at the August baseline; 83 now) drives readonly/developer/operator/admin profiles,
  graph/search additions, and fail-closed denylists (`src/arangodb_mcp/catalog/tools.yaml:1-108`,
  `src/arangodb_mcp/policy/profiles.py:10-89`).
- `[V]` The default surface is 17 readonly tools and remains below the 9,000-token contract ceiling
  (`tests/test_tool_policy.py:115-142`, `tests/test_tool_policy.py:199-207`).
- `[V]` Parser-backed AQL classification, non-disableable runtime/output/bulk/concurrency ceilings,
  and one-use bound confirmation tokens are enforced before dispatch
  (`src/arangodb_mcp/policy/aql_classifier.py:10-84`, `src/arangodb_mcp/policy/limits.py:36-160`,
  `src/arangodb_mcp/policy/confirmation.py:30-230`).
- `[V]` Resources, prompts, a versioned v3 result envelope, stateless 2026-07-28 interoperability,
  and Host/Origin controls are covered by executable contracts (`src/arangodb_mcp/mcp_content.py:22-164`,
  `src/arangodb_mcp/contracts/v3_result.py:8-100`, `tests/test_protocol_interop.py:64-139`).
- `[V]` CI now includes deterministic tool-selection, destructive-refusal, retrieval-quality, and
  latency gates. The local baseline is 90% selection, 100% refusal, MRR@10 1.0, and recall@5 1.0
  (`evals/run_quality_gates.py:40-170`, `.github/workflows/ci.yml:43-50`).
- `[V]` Phase 4 locally verifies OIDC discovery/JWKS, a signed-JWT MCP request, Prometheus scraping,
  and correlated OTLP spans (`scripts/run_phase4_integration.py:159-296`).
- `[V]` Phase 5 moves the application into the installable `arangodb_mcp` package, verifies an
  isolated wheel and immutable non-root wheel-based image, configures trusted release publication,
  and passes strict Helm/kubeconform plus live kind install/upgrade/probe/authentication
  (`pyproject.toml:10-18`, `scripts/verify_wheel.py:61-121`,
  `scripts/verify_helm.sh:13-54`, `scripts/run_helm_kind_smoke.sh:47-180`).
- `[V]` Security, contribution, ownership, support, threat-model, and deprecation documents are
  committed on the `phase1/platform-spine` branch (`SECURITY.md:1-80`, `CONTRIBUTING.md:1-51`, `.github/CODEOWNERS:1-8`,
  `SUPPORT.md:1-29`, `docs/threat-model.md:1-104`, `docs/deprecation-policy.md:1-35`).

At the August assessment the evidence-backed total was **82/B+**, eleven points above the Phase 0
baseline. It fell to **81/B+** on September 29, when adverse external evidence was captured, and returned
to **82/B+** on October 21, once every item behind that drop was resolved and externally verified. That is five
points above Neo4j's 77. Phase 4/5 implementation is recorded without changing category scores:
publishing and governance still lack their EXTERNAL gates, and MAT-003 requires an independent
post-30-day evidence review rather than a maintainer self-awarding an A.

## Method

### Evidence labels

- `[V]` Verified in source, tests, CI configuration, vendor documentation, or release metadata.
- `[I]` Reasoned inference from verified evidence.
- `[U]` Unknown from available public evidence.

The local repository received a static source audit (re-audited September 29, 2026, when external
GitHub CI and security results were also captured). Competitors were assessed from public vendor
documentation, repositories, package registries, and release metadata. The latest suite passes 487
tests; external CI measured 82.40%/82.21% coverage (82.64% locally at the August baseline). Local live evidence includes the multi-server cluster,
Compose, Phase 4 OIDC/telemetry harness, and Phase 5 kind Helm install/upgrade harness. Published
artifact integrity, sustained production reliability, governance visibility, and adoption were not
independently measured.

### Weighted rubric

| Category | Weight | SOTA bar |
|---|---:|---|
| Database capability | 20 | Broad, composable data operations with domain-native discovery and analysis |
| Agent ergonomics | 15 | Small default surface, progressive disclosure, bounded output, consistent schemas |
| Security and guardrails | 15 | Read-only profiles, scoped identity, query classification, confirmations, safe HTTP |
| Reliability and verification | 15 | Unit/integration/E2E tests, enforced coverage, live-engine and agent-quality gates |
| Operations and observability | 15 | Health, metrics, traces, structured logs, auditability, resilience |
| Deployment and integration | 10 | Current transports, easy install, container/package distribution, cloud readiness |
| Ecosystem and release maturity | 10 | Active releases, provenance, security automation, adoption, governance |
| **Total** | **100** | A composite target; no compared product demonstrates every item |

Grades: **A** 90–100, **A-** 85–89, **B+** 80–84, **B** 75–79, **B-** 70–74,
**C+** 65–69, **C** 60–64, **D** below 60.

This is a competitive-position score, not a universal product-quality ranking. Focused products
such as Qdrant intentionally trade breadth for simplicity.

## Competitive ranking

| Rank | Server | Capability /20 | Ergonomics /15 | Security /15 | Reliability /15 | Operations /15 | Deployment /10 | Maturity /10 | Total | Grade | Evidence confidence |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | MongoDB MCP | 18 | 11 | 12 | 14 | 14 | 9 | 10 | **88** | **A-** | Medium-high |
| 2 | **ArangoDB MCP Server** | **19** | **14** | **13** | **14** | **8** | **9** | **5** | **82** | **B+** | High static/test / high external (CI, security, branch protection verified) |
| 3 | Bytebase DBHub | 10 | 15 | 13 | 13 | 10 | 10 | 9 | **80** | **B+** | Medium-high |
| 4 | Neo4j MCP | 10 | 14 | 13 | 13 | 9 | 9 | 9 | **77** | **B** | Medium-high |
| 5 | Qdrant MCP | 6 | 15 | 9 | 10 | 4 | 7 | 8 | **59** | **D** | Medium |
| 6 | Amazon Neptune MCP | 9 | 12 | 10 | 10 | 4 | 6 | 7 | **58** | **D** | Medium |

The best observed category scores combine to **95/100**, but they are distributed across multiple
products. ArangoDB's 13-point gap to that composite benchmark is concentrated in identity,
operations, distribution, and ecosystem maturity rather than database or agent-safety capability.
Competitor scores are held at the August 6 assessment. Their public metrics are refreshed below,
but their categories were not re-audited in this revision.

## ArangoDB category grades

### 1. Database capability — 19/20 (A)

**Why it leads**

- `[V]` The framework contract test requires exactly 83 registered tools
  (`tests/test_mcp_e2e.py:59-63`).
- `[V]` *(September 29)* Measured AQL profiling and proven-equivalence comparison let an agent
  verify that an "optimized" rewrite returns the same data, and measure that it is faster, before
  recommending it (`src/arangodb_mcp/agents/aql_execution_agent.py:312-493`). This strengthens
  the 19 but does not close either "not 20" gap below.
- `[V]` The server covers document CRUD, database and collection management, graph management and
  traversal, AQL validation/explain/execute, indexes, vector and hybrid search, views, analyzers,
  cluster administration, transactions, backups, users, and permissions (`src/arangodb_mcp/server.py:18-61`).
- `[V]` Embedding and shared-memory tools add hybrid retrieval, provenance, reuse outcomes, and
  drift capture (`src/arangodb_mcp/server.py:63-66`, `PRD.md:263-275`).
- `[V]` Shared-memory consolidation now preserves an explicit `force=true` ruling while retaining
  default implicit and caller-selected explicit replacement behavior
  (`src/arangodb_mcp/mcp_tools/pattern_memory_tools.py:142-145`,
  `src/arangodb_mcp/mcp_tools/pattern_memory_tools.py:663-687`).
- `[V]` Dedicated graph and vector tools reduce the need to synthesize raw AQL
  (`src/arangodb_mcp/server.py:29-43`).

**Why it is not 20**

- `[V]` The pattern-memory subsystem deliberately keeps substantial business logic in the tool
  layer, a known architecture divergence (`PRD.md:275`).
- `[V]` Resources and prompts expose schema/manual/workflow context, but there is no domain-native
  progressive schema search equivalent to the strongest discovery implementations.

### 2. Agent ergonomics — 14/15 (A)

**Strengths**

- `[V]` Server instructions prescribe a manual → validate → explain → execute AQL workflow
  (`src/arangodb_mcp/server.py:11-16`).
- `[V]` The server publishes a capability map and database best practices to clients
  (`src/arangodb_mcp/server.py:18-79`).
- `[V]` Tool naming and registration are mechanically checked
  (`tests/test_mcp_e2e.py:59-67`).
- `[V]` Query budgets and dedicated traversal/search tools help keep calls bounded
  (`src/arangodb_mcp/config.py:101-105`, `src/arangodb_mcp/server.py:71-79`).
- `[V]` The default profile exposes exactly 17 readonly tools, while explicit profiles and
  graph/search toolsets expand the surface by deployment intent (`src/arangodb_mcp/policy/profiles.py:10-89`,
  `tests/test_tool_policy.py:115-142`).
- `[V]` All dispatches use one v3 success/error envelope with machine-readable limit metadata
  (`src/arangodb_mcp/contracts/v3_result.py:8-100`, `src/arangodb_mcp/policy/tool_manager.py:91-253`).
- `[V]` Manuals, schema, active profile, and status are MCP resources, with safe AQL, graph, and
  search workflow prompts (`src/arangodb_mcp/mcp_content.py:22-164`).

**Gaps**

- `[V]` The compact default still exposes 17 schemas and 8,293 estimated tokens; it does not offer
  DBHub-style dynamic two-tool discovery (`tests/test_tool_policy.py:199-207`).
- `[I]` The mandatory five-step AQL workflow improves correctness but can waste calls and tokens
  for known-safe queries.
- `[V]` The pattern-memory subsystem retains a documented business-logic exception in the tool
  layer (`PRD.md:297`).

### 3. Security and guardrails — 13/15 (A-)

**Strengths**

- `[V]` Non-loopback HTTP refuses to start without a bearer token (`src/arangodb_mcp/main.py:228-236`).
- `[V]` Token comparison is constant-time (`src/arangodb_mcp/auth_middleware.py:63`).
- `[V]` Database and MCP credentials use `SecretStr`; AQL is redacted from logs by default
  (`src/arangodb_mcp/config.py:34-40`, `src/arangodb_mcp/config.py:106-112`).
- `[V]` Server-side JavaScript transactions are disabled by default
  (`src/arangodb_mcp/config.py:96-100`).
- `[V]` `_system` deletion and primary-index deletion have explicit mechanical guards
  (`src/arangodb_mcp/mcp_tools/database_tools.py:136-137`,
  `src/arangodb_mcp/agents/index_management_agent.py:105-106`).
- `[V]` Version 3 defaults to a readonly profile; writes/admin tools require explicit enablement,
  and tool/category denylists fail closed (`src/arangodb_mcp/config.py:146-161`, `src/arangodb_mcp/policy/profiles.py:31-89`).
- `[V]` AQL policy uses the authoritative parser AST and rejects mutation or ambiguity in readonly
  mode (`src/arangodb_mcp/policy/aql_classifier.py:10-84`, `src/arangodb_mcp/agents/aql_execution_agent.py:64-91`).
- `[V]` Irreversible catalog entries require actor/action/parameter/expiry-bound one-use tokens
  minted outside MCP (`src/arangodb_mcp/policy/confirmation.py:30-230`, `scripts/mint_confirmation.py:1-57`).
- `[V]` Runtime, rows, bytes, bulk input, and concurrency have non-disableable server maxima
  (`src/arangodb_mcp/policy/limits.py:36-160`, `src/arangodb_mcp/policy/tool_manager.py:129-253`).
- `[V]` Host and Origin validation runs before authentication on HTTP transports
  (`src/arangodb_mcp/asgi/app_factory.py:20-55`, `src/arangodb_mcp/middleware/transport_security.py:11-30`).
- `[V]` Production OIDC validates discovery/JWKS, signatures, issuer, audience, time bounds, actor,
  scopes, and database claims, then intersects them with profiles, catalog policy, and
  request-scoped server-side credentials (`src/arangodb_mcp/oidc.py:39-365`,
  `src/arangodb_mcp/policy/credentials.py:21-121`,
  `src/arangodb_mcp/policy/tool_manager.py:161-170,434-471`).

**Gaps**

- `[V]` The temporary legacy bearer mode remains a shared identity backed by one configured
  ArangoDB account; production deployments must select OIDC for per-request authority.
- `[V]` The default database is `_system`, expanding the blast radius of a privileged
  configuration (`src/arangodb_mcp/config.py:37`).
- `[U]` No independent production identity-provider interoperability or sustained authorization
  telemetry has been published.

### 4. Reliability and verification — 14/15 (A)

**Strengths**

- `[V]` The repository contains 438 test functions across mock, framework-contract, integration,
  and cluster tiers; the latest parametrized suite executes 487 tests and explicitly enforces
  83-tool registration (`tests/test_mcp_e2e.py:59-74`).
- `[V]` CI runs Ruff, formatting, mypy, and Docker-backed tests on Python 3.10 and 3.11 with
  ArangoDB 3.12 (`.github/workflows/ci.yml:10-90`).
- `[V]` The force/supersede regression is tested in both directions, and PR #2's Docker-backed
  Python 3.10 and 3.11 jobs passed (`tests/test_pattern_memory_tools.py:295-325`).
- `[V]` Blocking driver work is dispatched off the event loop
  (`src/arangodb_mcp/agents/agent_base.py:100-105`, `PRD.md:305-312`).
- `[V]` Startup uses retry/backoff and a lifespan-managed connection
  (`src/arangodb_mcp/config.py:114-123`, `PRD.md:295-303`).
- `[V]` The full suite passes 487 tests (82.40%/82.21% external coverage on Python 3.10/3.11;
  82.64% at the August baseline), and CI enforces a 79% floor
  (`pyproject.toml:94-96`, `.github/workflows/ci.yml:82-97`).
- `[V]` Repository-wide Ruff check/format and the CI-equivalent Mypy command pass locally.
- `[V]` The multi-server cluster tier passes against a live three-machine starter deployment and is
  scheduled nightly with pinned container digests (`tests/test_cluster.py:17-63`,
  `.github/workflows/cluster-nightly.yml:1-113`).
- `[V]` Blocking deterministic gates cover tool selection, destructive refusal, retrieval MRR and
  recall, and latency percentiles (`evals/run_quality_gates.py:40-170`).
- `[V]` Strict/auto/legacy Streamable HTTP and SSE/stdio composition have interoperability
  contracts (`tests/test_protocol_interop.py:64-139`, `tests/test_app_factory.py:59-75`).

- `[V]` *(September 29)* External runs now confirm the Docker-backed suite on GitHub runners:
  487 executed tests (438 functions) at 82.40% (Python 3.10) and 82.21% (Python 3.11) coverage,
  plus Helm/kind smoke and the Phase 4 OIDC/telemetry integration.

**Gaps**

- `[V]` *(September 29)* The CI workflow as a whole has not passed on any branch push since
  August 8. Lint fails on four `SIM105` findings in `.cursor/hooks/`, and a test regression at
  `a2bd938` was fixed on September 29. Required branch checks still need repository-admin
  configuration, and `main` is unprotected (`PRD.md:442-445`).
- `[V]` The deterministic latency gate is not a multi-client saturation/load benchmark.
- `[I]` The score holds at 14 because the red jobs are tooling and hygiene failures, not
  product-test failures. It is at risk if the workflow stays red, because branch protection
  cannot require checks that never pass.

### 5. Operations and observability — 8/15 (B-)

**Strengths**

- `[V]` HTTP deployments expose distinct `/livez` and dependency-aware `/readyz` probes; the
  deprecated `/healthz` alias retains readiness semantics (`src/arangodb_mcp/asgi/health.py:13-93`).
  *(September 29)* The Helm chart also gates liveness on a `/readyz` `startupProbe`, so slow cold
  starts are not liveness-killed (`deploy/helm/arangodb-mcp/templates/deployment.yaml:187-193`).
- `[V]` Logging supports text or field-whitelisted JSON output
  (`src/arangodb_mcp/main.py:20-60`, `src/arangodb_mcp/config.py:75-82`).
- `[V]` Startup diagnostics, AQL redaction, standardized errors, and connection retries are
  implemented (`src/arangodb_mcp/main.py:210-215`, `src/arangodb_mcp/config.py:106-123`).
- `[V]` HTTP requests receive propagated `X-Request-ID` correlation context
  (`src/arangodb_mcp/middleware/request_context.py:20-46`, `src/arangodb_mcp/asgi/app_factory.py:47-48`).
- `[V]` SLO semantics and probe failure behavior are documented and executable
  (`docs/slo.md:7-62`, `tests/test_health_endpoint.py:89-164`).
- `[V]` Dispatch enforces global per-tool concurrency ceilings
  (`src/arangodb_mcp/policy/limits.py:121-160`, `src/arangodb_mcp/policy/tool_manager.py:155-253`).
- `[V]` Prometheus metrics, OpenTelemetry request/tool/database/embedding spans, one redacted audit
  event per write/admin attempt, and per-actor/global/class/tool limits are implemented
  (`src/arangodb_mcp/observability/metrics.py:15-163`,
  `src/arangodb_mcp/observability/telemetry.py:22-75`,
  `src/arangodb_mcp/observability/audit.py:14-60`,
  `src/arangodb_mcp/policy/limits.py:176-350`).
- `[V]` The containerized Phase 4 harness observed a successful MCP metric and correlated
  request/tool/database spans (`scripts/run_phase4_integration.py:159-296`).

**Gaps**

- `[U]` No independent production telemetry window, dashboard/alert evidence, or multi-replica
  saturation benchmark has been published.
- `[V]` The initial SLO remains an objective; it has not accumulated a 30-day production window
  required for MAT-003 (`docs/slo.md:42-62`).

MongoDB is the benchmark here: public evidence shows separate health/metrics endpoints, tool
duration and count metrics, structured logging, telemetry, and agent evaluations.

### 6. Deployment and integration — 9/10 (A-)

**Strengths**

- `[V]` stdio, SSE, and Streamable HTTP are implemented (`src/arangodb_mcp/config.py:83-87`,
  `src/arangodb_mcp/main.py:177-180`, `src/arangodb_mcp/main.py:220-246`).
- `[V]` Dockerfile and Docker Compose deployment paths are included (`README.md:138-184`).
- `[V]` The server fails closed if configured auth cannot be wrapped around the FastMCP ASGI app
  (`src/arangodb_mcp/main.py:160-169`).
- `[V]` Compose requires `MCP_AUTH_TOKEN`, enables ArangoDB vector indexing, supports configurable
  host ports, and waits for an authenticated ArangoDB health probe
  (`docker-compose.yml:4-39`).
- `[V]` The MCP image has a database-backed health check, and standalone HTTP startup explicitly
  owns the ArangoDB connector lifecycle (`Dockerfile:25-26`, `src/arangodb_mcp/main.py:130-144`).
- `[V]` Static deployment contracts and a clean live Compose smoke test verify the documented
  secret, health, and vector behavior (`tests/test_deployment_contract.py:12-38`).
- `[V]` The runtime image is a multi-stage Alpine build running as an unprivileged user
  (`Dockerfile:1-52`, `tests/test_deployment_contract.py:65-82`).
- `[V]` Streamable HTTP defaults to stateless JSON responses with strict/legacy/auto compatibility,
  2026-07-28 routing metadata, cache hints, and Host/Origin checks (`src/arangodb_mcp/server.py:88-106`,
  `src/arangodb_mcp/middleware/protocol.py:24-236`).
- `[V]` The `src/` package declares the `arangodb-mcp` console entry point and packaged catalog and
  manuals; an isolated wheel-only install verifies imports, data, tools, prompts/resources, and CLI
  (`pyproject.toml:10-18`, `scripts/verify_wheel.py:61-121`).
- `[V]` The runtime image installs the wheel, removes package installers, makes the environment
  read-only, and runs as a non-root user (`Dockerfile:12-29,46-51`).
- `[V]` The supported Helm chart documents secrets, probes, resources, hardening, digest pinning,
  and upgrades; strict lint/kubeconform and live kind install/upgrade/probe/authentication pass
  locally (`deploy/helm/arangodb-mcp/README.md:1-113`,
  `scripts/verify_helm.sh:13-54`, `scripts/run_helm_kind_smoke.sh:47-180`).

**Gaps**

- `[U]` No PyPI package or GHCR digest is externally published, so install/start from published
  immutable artifacts remains unverified.
- `[V]` The chart deploys only the MCP server; operators still provide ArangoDB, ingress/TLS,
  external secrets, network policy, and multi-cluster operations.

### 7. Ecosystem and release maturity — 5/10 (D) *(4/10 from September 29 to October 21)*

**Restored on October 21:** every item listed under "Why it dropped" below is resolved and externally
verified (see the October 21 P0 revision at the top). What still keeps this category at 5 is the lack
of any release and the minimal adoption.

**Why it dropped.** The August assessment gave 5 on configured automation, with the first
external results still `[U]`. Those results are now `[V]`, and they are adverse:

- `[V]` Full-history secret scanning failed on a committed third-party API key plus a
  test-fixture false positive. Configured secret scanning is only worth credit if it passes.
  *(October 5: the key was purged from all history and the false positive recorded; the secret
  scan now passes in CI. Credit for this category also needs the rest of the P0 row below.)*
- `[V]` Five CodeQL alerts (4 high, 1 medium) have been open and untriaged since at least
  August. Three are clear-text logging and one is weak hashing, all in the opt-in AQL log path;
  one is a test-only socket bind. Some may be accepted risks, but none is dismissed with a
  justification.
- `[V]` There is no release or tag, and PR #7 has been open about seven weeks with `UNSTABLE`
  checks. Meanwhile Neo4j, MongoDB, DBHub, and Neptune each shipped releases.
- `[V]` `main` has no branch protection, Dependabot security alerts are disabled, and three
  Dependabot update PRs are unmerged.
- `[V]` Public adoption is 3 stars and 0 forks.

**Strengths**

- `[V]` Apache-2.0 licensing and a repeatable CI workflow are present (`LICENSE:1`,
  `.github/workflows/ci.yml:1-90`).
- `[V]` The repository has current implementation activity through September 29, 2026.
- `[V]` A non-owner collaborator submitted a focused correctness fix that was reviewed and merged
  through PR [#2](https://github.com/arango-solutions-org/arango-solutions-mcp/pull/2).
- `[V]` Dependabot covers Python, GitHub Actions, and Docker; CodeQL and pip-audit workflows run on
  pull requests, `main`, and a weekly schedule (`.github/dependabot.yml:1-24`,
  `.github/workflows/security.yml:1-84`).
- `[V]` The release workflow configures PyPI trusted publishing, GHCR digest publication, Python and
  container SBOM/provenance attestations, keyless cosign signing, digest scanning, verification,
  Helm packaging, and GitHub release creation (`.github/workflows/release.yml:113-347`).
- `[V]` Local governance files define private vulnerability reporting, contribution flow,
  ownership, support targets, threat boundaries, and deprecation/upgrade policy
  (`SECURITY.md:1-80`, `CONTRIBUTING.md:1-51`, `.github/CODEOWNERS:1-8`,
  `SUPPORT.md:1-29`, `docs/threat-model.md:1-104`, `docs/deprecation-policy.md:1-35`).

**Gaps**

- `[U]` No release execution proves trusted publication, SBOMs, signatures, provenance, or
  verification against externally published artifacts.
- `[U]` Governance files are committed and pushed on the `phase1/platform-spine` branch but are not
  yet on `main` or in a release, so they cannot yet be credited as public response/contribution paths.
- `[V]` Public adoption evidence remains limited to an initial collaborator contribution, while
  the compared peers have measurable stars, downloads, releases, or vendor distribution.
- `[V]` Tool/test inventories, configuration variables, and immutable release-history references
  are now checked mechanically in CI (`scripts/verify_docs.py:19-109`,
  `.github/workflows/ci.yml:43-44`).

## Head-to-head assessment

### Versus MongoDB MCP

ArangoDB wins on unified graph + document + search/vector + cluster/backup coverage. MongoDB wins
decisively on managed-platform integration, configurable tool restrictions, confirmations,
metrics, agent evaluations, security automation, distribution, and release provenance. MongoDB
is the principal **production-readiness benchmark**.

### Versus Bytebase DBHub

ArangoDB provides far more administration, graph, and vector functionality. DBHub's two-tool
default, progressive schema search, stateless MCP 2026-07-28 support, read-only enforcement,
static-token HTTP controls, traces, and one-command distribution make it the principal
**agent-ergonomics benchmark**.

### Versus Neo4j MCP

ArangoDB leads 82 to 77 through much greater multi-model/administrative breadth, a compact
readonly default, parser-backed query policy, irreversible-action confirmation, resources/prompts,
and deterministic quality gates. Neo4j retains the simpler four-tool graph surface, mature package
distribution, and per-request remote credentials, so it remains the principal **graph simplicity
and request-identity benchmark**.

### Versus Amazon Neptune MCP

ArangoDB wins on transports, breadth, local deployment, graph operations, and code-level
guardrails. Neptune's AWS credential chain, IAM, and VPC integration are stronger for AWS-native
identity and network controls. Neptune is the **cloud identity benchmark**, not the feature
leader.

### Versus Qdrant MCP

ArangoDB includes a substantially broader vector, hybrid-search, database, graph, and memory
surface. Qdrant's two-tool interface and read-only mode are easier for an agent to reason about.
Qdrant is the **focused semantic-memory ergonomics benchmark**.

## SOTA gap register

| Priority | Gap | Competitive evidence | Current evidence | Score impact |
|---:|---|---|---|---:|
| Closed | Compact discovery and tool profiles | DBHub: 2 default tools; Qdrant: 2 tools | 17-tool readonly default plus explicit profiles/toolsets (`src/arangodb_mcp/policy/profiles.py:10-89`) | Credited |
| Closed | Read-only, denylist, query policy, and confirmation | MongoDB/DBHub/Neo4j provide mechanical restrictions | Catalog policy, parser classification, hard limits, and one-use confirmation (`src/arangodb_mcp/policy/tool_manager.py:38-253`) | Credited |
| Closed | MCP 2026-07-28 interoperability | DBHub documents current stateless compatibility | Strict/auto/legacy stateless contracts and live probe (`tests/test_protocol_interop.py:64-139`) | Credited |
| Closed locally | OAuth/per-request identity and scopes | Neo4j uses per-request DB identity; Toolbox sets broader SOTA | OIDC authority intersection and request credentials implemented; independent production evidence pending (`src/arangodb_mcp/policy/tool_manager.py:434-471`) | Regrade pending |
| Closed locally | Metrics, traces, and audit events | MongoDB exposes Prometheus; DBHub exposes request traces | Prometheus, OTLP, audit, and limit telemetry implemented and locally exercised (`scripts/run_phase4_integration.py:159-296`) | Regrade pending |
| Closed | Green and enforce the external pipeline | Peers publish green releases from protected branches | **Closed Oct 21:** CI 6/6 and Security 4/4 green; 0 open CodeQL alerts (7 fixed, 5 dismissed with reasons); `main` protected by 10 required checks, enforced for admins; Dependabot security alerts on | Credited (+1; maturity 4 → 5) |
| P1 | Release automation and provenance | MongoDB, Neo4j, DBHub publish packages/images/releases | Workflow implemented; no published artifacts or attestations (`.github/workflows/release.yml:113-347`) | +4 |
| P1 | External verification enforcement | MongoDB has published accuracy/evaluation and security pipelines | Local gates pass; first external security/interop runs and branch protection remain open | +1 |
| Closed | Resources/prompts and schema-first discovery | Neptune exposes resources; peers have compact discovery | Four resource capabilities and three guided prompts (`src/arangodb_mcp/mcp_content.py:22-164`) | Credited |
| P2 | Adoption and governance | Competitors have releases, users, and contribution paths | Governance exists locally but is not public; 30-day adoption gate remains open | +2 |

Phases 1–3 added **+11** after re-audit. The September 29 capture of adverse external evidence
removed **−1** (maturity). Phase 4/5 improvements await the independent post-30-day
MAT-003 review. Remaining score impacts are directional estimates and are not additive without that
evidence-backed regrade.

## Recommended roadmap

### Phase 0 — Repair credibility and defaults

1. **Completed:** Docker Compose starts with explicit secret injection, vector indexing, and
   database-backed health checks.
2. **Completed:** Reconciled tool/test counts, architecture inventories, configuration variables,
   and release-history claims; CI now rejects documentation drift.
3. **Completed:** lint/format/type-check are green locally; coverage enforcement, Dependabot,
   CodeQL, dependency audit, and a real pinned nightly cluster tier are configured and locally
   verified.

### Phase 1 — Make breadth safe and usable

1. **Completed:** readonly/developer/operator/admin profiles and graph/search toolsets.
2. **Completed:** compact 17-tool readonly default with a bounded schema footprint.
3. **Completed:** parser-backed AQL classification and hard runtime/row/byte/bulk/concurrency
   ceilings.
4. **Completed:** actor/action/parameter/expiry-bound one-use confirmation for irreversible tools.
5. **Completed:** one structured v3 success/error envelope with dated legacy compatibility.

### Phase 2 — Meet the production MCP bar

1. **Completed locally:** stateless MCP 2026-07-28 routing, cache, Host/Origin, and compatibility.
2. **Completed locally:** OAuth 2.1/OIDC resource-server validation, protected-resource metadata,
   per-request identity, scopes, database policy, and request-scoped credentials.
3. **Completed locally:** OpenTelemetry traces and Prometheus metrics for tool, AQL, dependency,
   and limiter behavior.
4. **Completed locally:** one structured, redacted audit event for every mutation/privileged
   attempt.

### Phase 3 — Prove and distribute quality

1. **Workflow implemented; publication pending:** publish versioned Python and container artifacts
   with signed provenance, SBOMs, changelogs, and automated vulnerability scans.
2. **Completed for the deterministic baseline:** MCP interoperability, tool selection,
   destructive refusal, retrieval MRR/recall, latency, and output ceilings are blocking gates.
3. Publish reproducible latency/concurrency benchmarks and the locally implemented governance
   policies.
4. **Completed locally:** supported Helm chart with static validation and live kind
   install/upgrade/probe/authentication acceptance.

## What would move this server to A-range

The current **82/B+** result needs eight additional points for A-range. The P0 point was restored on
October 21; the remaining path is the release, operations and adoption evidence below.

- raising security from 13 to 15 with OIDC scopes, authority intersection, and request-scoped
  least-privilege credentials;
- raising operations from 8 to at least 12 with metrics, traces, complete audit events, propagated
  correlation, and per-actor load controls;
- raising deployment and maturity from 14 combined to at least 16 through published signed
  artifacts, Helm, governance, and independently observable use.

Phase 4/5 implementation may support a future **90–92/A** result, but the score remains **82/B+**
until external interoperability, security, release, operational, governance, and use evidence
passes and an independent MAT-003 regrade occurs after at least 30 days.

## Competitor evidence

### Neo4j MCP

- Official project, 297 GitHub stars (278 in August); v1.6.0 released September 10, 2026.
- Four tools: schema, read/write Cypher, and GDS procedure discovery.
- stdio and stateless HTTP; per-request Basic/Bearer auth; mature package and release channels.
- Sources: [repository](https://github.com/neo4j/mcp),
  [documentation](https://neo4j.com/docs/mcp/current/),
  [authentication](https://neo4j.com/docs/mcp/current/authentication/),
  [releases](https://github.com/neo4j/mcp/releases).

### MongoDB MCP

- Official project, 1,137 GitHub stars (1,091 in August); v2.1.2 released September 23, 2026.
- Broad database and Atlas surface with read-only/tool-category controls, limits, metrics, and
  extensive evaluations.
- Sources: [repository](https://github.com/mongodb-js/mongodb-mcp-server),
  [documentation](https://www.mongodb.com/docs/mcp-server/),
  [releases](https://github.com/mongodb-js/mongodb-mcp-server/releases),
  [Docker image](https://hub.docker.com/r/mongodb/mongodb-mcp-server).

### Amazon Neptune MCP

- AWS Labs-maintained; PyPI package 1.1.1 (1.0.20 in August); monorepo release September 22, 2026.
- Four tools plus status/schema resources; stdio; IAM/AWS credential chain.
- Sources: [repository](https://github.com/awslabs/mcp/tree/main/src/amazon-neptune-mcp-server),
  [documentation](https://awslabs.github.io/mcp/servers/amazon-neptune-mcp-server),
  [PyPI](https://pypi.org/project/awslabs.amazon-neptune-mcp-server/).

### Qdrant MCP

- Official project, 1,540 GitHub stars (1,488 in August); still v0.8.1 (December 10, 2025).
- Two focused store/find tools; stdio, SSE, and Streamable HTTP; Qdrant API key and read-only mode.
- Sources: [repository](https://github.com/qdrant/mcp-server-qdrant),
  [release](https://github.com/qdrant/mcp-server-qdrant/releases/tag/v0.8.1),
  [PyPI](https://pypi.org/project/mcp-server-qdrant/).

### Bytebase DBHub

- Bytebase-backed, 3,585 GitHub stars (3,289 in August); v1.4.0 released September 28, 2026.
  Weekly npm downloads were about 41,769 in August and were not re-measured.
- Two-tool default, current stateless HTTP, read-only enforcement, request traces, and broad
  package/container distribution.
- Sources: [repository](https://github.com/bytebase/dbhub),
  [documentation](https://dbhub.ai/),
  [transport and auth](https://dbhub.ai/config/command-line),
  [releases](https://github.com/bytebase/dbhub/releases).

### SOTA protocol reference

- MCP 2026-07-28 establishes the current stateless core, required Streamable HTTP routing headers,
  MRTR interactions, an extensions framework, and authorization hardening.
- Sources: [release overview](https://blog.modelcontextprotocol.io/posts/2026-07-28/),
  [Streamable HTTP specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http).

## Evidence limitations

- Competitor features were not installed or independently penetration-tested.
- Public stars/downloads indicate adoption, not production quality.
- No peer publishes directly comparable production usage, support SLA, independent security
  audit, standardized interoperability result, or latency/token benchmark.
- `[V]` Latest completed local coverage is 82.64%; production throughput, failure rate, and adoption remain
  unverified.
- `[V]` *(September 29)* External CI and security runs are now captured. The test, Helm, OIDC,
  CodeQL-analysis, and container-scan jobs pass; lint and secret scanning fail. Competitor
  categories were not re-audited in this revision, only their public metrics.
- Scores should be recalculated after material protocol, security, release, or tool-surface
  changes.
