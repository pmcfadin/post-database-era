# Research Questions Outline — Unified Multi‑API Gateway (SQL, KV, Doc, Graph, Search)

## Sub‑theme 1: Unified gateway prevalence
- What % of top managed DB platforms ship a unified multi‑API gateway (2025→2030)?
- What share of new platform launches include multi‑API by default vs add‑on?
- What % of customers enable the gateway vs single‑API SKUs per vendor?
- How many public case studies cite the gateway as the primary purchase driver?
- What % revenue/ARR is tied to multi‑API SKUs per vendor over time?
- Do analyst reports track “multi‑API gateway” as a distinct capability by 2030?

## Sub‑theme 2: API coverage & parity (SQL/KV/Doc/Graph/Search)
- Do vendors offer all five APIs behind one endpoint/product name by 2030?
- Are feature parity gaps <10% across APIs for CRUD, indexing, and paging?
- Do cross‑API consistency guarantees match docs (read/write semantics)?
- How often are features GA in one API but preview/missing in others?
- Are migration guides/API shims maintained for all five APIs?
- Do SDKs expose a unified client with pluggable API modes?

## Sub‑theme 3: Developer velocity impact
- Does gateway adoption reduce time‑to‑first‑query for new apps by ≥30%?
- Are cycle times from schema→prototype→prod shorter with the gateway?
- Do teams report fewer vendor‑specific blockers in postmortems?
- What % of repos use gateway SDKs vs engine‑specific clients?
- Do platform teams see lower backlog for cross‑API feature requests?
- Do gateway‑based projects show higher release cadence vs controls?

## Sub‑theme 4: Cost/TCO outcomes
- Is infra+ops TCO lower by ≥15% with a multi‑API SKU vs separate engines?
- Do license/pricing models favor gateway bundles over single‑API plans?
- Are data egress/storage duplication costs lower with unified storage?
- Do support tickets/incidents per 1k nodes drop after gateway adoption?
- Is spend predictability (variance) better with multi‑API SKUs?
- Do FinOps dashboards show reduced idle/over‑provisioned assets?

## Sub‑theme 5: SKU adoption & productization
- Do vendors list a single multi‑API SKU vs many API‑specific SKUs by 2030?
- Are multi‑API SKUs among the top 3 revenue drivers in earnings decks?
- Do free tiers default to the gateway rather than single‑API modes?
- Are usage‑based prices aligned across APIs (e.g., RU, CU, DU) consistently?
- Do marketplaces categorize multi‑API as first‑class product tiles?
- Are migrations to multi‑API SKUs growing YoY across customer cohorts?

## Sub‑theme 6: Performance & reliability trade‑offs
- Is gateway overhead ≤10% latency vs native engines on common workloads?
- Are P90/P99 SLOs met consistently across all APIs under mixed load?
- Do cross‑API transactions/reads avoid hotspots and maintain fairness?
- Are failure modes localized (API‑level) without cascading outages?
- Are perf regressions rarer with shared query planning/caching layers?
- Do users disable the gateway for perf‑critical paths? How often/why?

## Sub‑theme 7: Tooling, ecosystem, and interoperability
- Do major ORMs/BI/ETL tools natively support the gateway endpoint?
- Are connectors/drivers consolidated to one DSN with API selection?
- Do IaC modules (Terraform/Pulumi) model multi‑API resources uniformly?
- Are observability schemas (OTel) standardized across APIs via gateway?
- Do data catalogs/governance tools resolve entities across APIs?
- Are query UIs supporting all APIs in one console session?

## Sub‑theme 8: Governance, security, and compliance
- Can policies (RBAC/ABAC) target API scopes uniformly across services?
- Are audit logs consistent and joinable across all APIs?
- Do DPIA/compliance reviews pass without API‑specific exceptions?
- Are encryption/PII masking policies enforced identically for all APIs?
- Do secrets/keys rotate once for the gateway vs per‑API credentials?
- Are breach postmortems simpler with a single policy/control plane?

## Sub‑theme 9: Organizational & operational complexity
- Do platform teams report fewer runbooks and SOPs after gateway rollout?
- Are on‑call rotations consolidated with lower MTTR for API issues?
- Do golden paths/templates reduce API choice paralysis for dev teams?
- Are training hours per engineer lower for multi‑API vs many engines?
- Do service limits/quotas manageably scale across APIs without toil?
- Are ownership boundaries clearer between platform and app teams?

## Sub‑theme 10: Market incentives & vendor strategy
- Do vendors use bundling/discounts to steer to multi‑API SKUs?
- Are acquisitions/roadmaps consolidating APIs behind one brand?
- Do competitive win‑loss notes cite “velocity + cost” for gateway wins?
- Are specialized single‑API products being sunset or folded in?
- Do partner ecosystems build first on gateway rather than engines?
- Are RFPs specifying “multi‑API via one endpoint” as a must‑have?

## Sub‑theme 11: Counter‑evidence & boundary conditions
- Which workloads still require specialist engines despite the gateway?
- Do regulated sectors reject gateways due to compliance/perf needs?
- Are cross‑cloud/edge deployments harder with a centralized gateway?
- Do data model mismatches cause hidden complexity for teams?
- Are total costs higher when APIs force lowest‑common‑denominator use?
- Do vendor lock‑in risks rise when the gateway layer is proprietary?
