# Unified Gateway Multi-API Convergence

## Thesis Statement
> Managed platforms will expose SQL, KV, Doc, Graph, Search via a unified gateway, driven by developer velocity and cost, measurable by growth in multi-API SKUs by 2030

## Directory Structure
- `research/` - Deep research reports and PDFs
- `notes/` - Working notes and synthesis documents
- `lit-scans/` - Literature scans and recency checks
- `opinion/` - Essays and white papers
- `figures/` - Charts, diagrams, and visualizations
- `datasets/` - Data tables and CSVs
- `drafts/` - Work in progress documents
- `inbox/` - Intake drop zone for new materials

## Evidence Standards
- Major claims require ≥2 Tier A/B sources
- All artifacts must include counterevidence sections
- Chicago-style citations required
- Maximum 15-word quotes from sources

## Important Data to Find

1) Multi-API SKU Catalog (Findable)
	•	Why: Show who actually sells a single multi-API SKU vs API-specific SKUs.
	•	Schema: vendor, platform, sku_id, sku_name, apis_supported[sql|kv|doc|graph|search], gateway_default(bool), first_listed_date, links[]
	•	Collect: Vendor product pages/marketplaces (AWS/GCP/Azure + vendor sites), Wayback for history.
	•	Use: Primary evidence for your thesis; time series of SKU convergence.

2) API Coverage & Parity Matrix (Findable)
	•	Why: Verify breadth/parity across CRUD, indexing, paging, transactions, consistency.
	•	Schema: vendor, api, feature, status{GA|Preview|NA}, added_date, doc_url
	•	Collect: Docs + release notes.
	•	Use: Compute % parity per platform; highlight feature gaps.

3) GA/Preview Cadence from Release Notes (Findable)
	•	Why: Track “preview→GA” velocity across APIs.
	•	Schema: vendor, api, feature, milestone, date, note_url
	•	Collect: Changelogs/RNs.
	•	Use: Lead/lag indicator for 2030 readiness.

4) Free-Tier Default Pathways (Findable)
	•	Why: Do quickstarts funnel users through the gateway?
	•	Schema: vendor, plan, entry_guide_url, default_path{gateway|single_api}, steps_to_first_query(int)
	•	Collect: Quickstarts, tutorials.
	•	Use: Developer-velocity proof point.

5) Marketplace Tile Taxonomy (Findable)
	•	Why: Are multi-API SKUs first-class tiles vs niche add-ons?
	•	Schema: marketplace, vendor, listing_id, tile_category, apis_on_tile[], first_seen, last_seen
	•	Collect: AWS/GCP/Azure marketplaces (screenshots + CSV).
	•	Use: External validation of productization.

6) Pricing & Unit Alignment Table (Findable/Composable)
	•	Why: Are RU/CU/DU (or equivalents) aligned across APIs?
	•	Schema: vendor, api, unit_name, free_tier_quota, on_demand_price, notes, link
	•	Collect: Pricing pages; compose normalized “per-1000 ops” columns.
	•	Use: Comparable price curves across APIs.

Demand-side (adoption & usage)

7) Case Studies Citing Gateway as Driver (Findable)
	•	Why: Show gateway as purchase/expansion trigger.
	•	Schema: vendor, customer, industry, use_case, gateway_cited(bool), quote(≤15 words), link
	•	Collect: Customer stories, conference talks.
	•	Use: Qual evidence; export short quotes that meet your limit.

8) SDK/Client Unification Score (Findable/Composable)
	•	Why: Do SDKs expose a unified client with API modes?
	•	Schema: vendor, language, client_repo, unified_modes[], monthly_downloads, stars, last_release_date
	•	Collect: GitHub + package registries; compose a “unification_score(0–5)”.
	•	Use: Developer UX convergence.

9) Time-to-First-Query Benchmark (Composable)
	•	Why: Quantify velocity: gateway vs single API.
	•	Schema: vendor, path{gateway|single}, steps, minutes, tester, date, script_url
	•	Collect: Run your own timed quickstart scripts.
	•	Use: “≥30% faster” style claims.

10) Job-Postings Signal (Findable/Composable)
	•	Why: Market demand for multi-API skills.
	•	Schema: source, employer, title, keywords[], api_mentions[], date
	•	Collect: Job boards; simple keyword filters.
	•	Use: Trend lines for skill demand.

11) Stack Overflow/Forum Tag Mix (Findable/Composable)
	•	Why: Are questions shifting to gateway concepts?
	•	Schema: platform_tag, api_tag, count, month
	•	Collect: SO data dumps/APIs, vendor forums.
	•	Use: Developer attention proxy.

Economics & business signaling

12) Earnings Deck Driver Mentions (Findable)
	•	Why: Are multi-API SKUs top-3 drivers?
	•	Schema: vendor, quarter, slide_ref, driver_rank, phrasing, link
	•	Collect: Investor decks/transcripts.
	•	Use: Business-level validation of SKU strategy.

13) ARR/Revenue Attribution Hints (Findable/Composable)
	•	Why: Tie revenue to SKU where possible.
	•	Schema: vendor, segment, metric, value, period, source_link, inference_note
	•	Collect: Public filings; compose cautious attributions with flags.
	•	Use: Conservative revenue ties to gateway.

14) FinOps Outcomes from Public Posts (Findable)
	•	Why: TCO/egress/storage duplication deltas after consolidation.
	•	Schema: company, before_cost, after_cost, delta_pct, notes, link
	•	Collect: Engineering blogs, talks.
	•	Use: Cost proof points (with counterevidence).

Standards & ecosystem

15) Standards Adoption Tracker (Findable)
	•	Why: SQL:2023, ISO GQL, JSONPath adoption timelines.
	•	Schema: standard, vendor, feature_subset, status{GA|Preview|Roadmap|NA}, date, link
	•	Collect: Standards docs + vendor mappings.
	•	Use: Syntax homogenization evidence.

16) Connector/BI Federation Coverage (Findable)
	•	Why: Are BI/ETL tools targeting the gateway?
	•	Schema: tool, vendor, gateway_supported(bool), api_modes[], version, link
	•	Collect: Tool docs.
	•	Use: Ecosystem readiness.

17) Migration Guides & Shims Registry (Findable)
	•	Why: Cross-API migration maturity.
	•	Schema: vendor, from_api, to_api, guide_url, maintained(bool), last_updated
	•	Collect: Docs repos.
	•	Use: 2030 feasibility indicator.

Performance & reliability

18) Typical-Query Penalty Dataset (Composable)
	•	Why: Is abstraction ≤10% slower on common queries?
	•	Schema: engine, api, workload_id, native_ms, gateway_ms, delta_pct, env_hash
	•	Collect: Your harness on TPC-ish micro-benchmarks.
	•	Use: Counter to “gateway is always slow” claims.

19) Incident/Support Signals (Findable)
	•	Why: Quality across APIs.
	•	Schema: vendor, api, issue_type, count, window, source
	•	Collect: Public trackers/changelogs.
	•	Use: Stability deltas by API.

Market prevalence & trends

20) Platform Launches Including Multi-API (Findable)
	•	Why: New launches defaulting to multi-API vs add-on.
	•	Schema: platform, launch_date, default_multi_api(bool), description, link
	•	Collect: Press releases/blogs.
	•	Use: Prevalence over time.

21) “Gateway” Term Tracking (Findable/Composable)
	•	Why: Analyst/vendor usage of the term.
	•	Schema: source, date, context, exact_phrase(≤15 words), link
	•	Collect: Analyst notes, vendor blogs, conference agendas.
	•	Use: Vocabulary normalization.

22) Google Trends Bundle (Findable)
	•	Why: Relative attention: “multi-API”, “unified gateway”, “Stargate”, etc.
	•	Schema: term, region, week, index
	•	Collect: Trends export.
	•	Use: Interest momentum.

Synthesis scaffolding (meta-datasets you’ll maintain)

23) Source Registry & Tiering (Composable)
	•	Why: Enforce your evidence standards.
	•	Schema: source_id, title, url, tier{A|B|C}, bias_notes, last_checked
	•	Use: Auto-filter major claims to ≥2 Tier A/B.

24) Claim→Evidence Map (Composable)
	•	Why: Trace each claim to supporting & counterevidence.
	•	Schema: claim_id, claim_text, support_sources[], counter_sources[], status{provisionally_true|contested}
	•	Use: Keeps counterevidence honest.

25) Quote Ledger (Composable)
	•	Why: Respect 15-word max quotes.
	•	Schema: quote_id, text(≤15 words), source_id, page, topic
	•	Use: Reuse short, compliant quotes.

26) Multi-API Gateway Index (MAGI) (Composable)
	•	Why: One score to compare platforms.
	•	Schema: vendor, subscore_api_parity(0–25), sku_unification(0–25), velocity(0–20), ecosystem(0–15), pricing_alignment(0–15), MAGI_total
	•	Use: Rank and trend; include rubric doc in /notes/.
