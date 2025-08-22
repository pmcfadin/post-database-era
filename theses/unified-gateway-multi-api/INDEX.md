# Unified Gateway Multi-API Data Index

This index organizes all data files in the `datasets/` directory according to the 26 research categories outlined in [README.md](README.md).

## Supply-side Evidence (Platform & Feature Coverage)

### 1. Multi-API SKU Catalog
**Schema**: vendor, platform, sku_id, sku_name, apis_supported[sql|kv|doc|graph|search], gateway_default(bool), first_listed_date, links[]

- `multi_api_sku_catalog.csv` - Core SKU catalog data
- `multi_api_sku_catalog_metadata.json` - Metadata for SKU catalog
- `2025-08-20__data__multi-api-sku-catalog__comprehensive__vendor-platform-comparison.csv` - Comprehensive vendor comparison
- `2025-08-20__data__multi-api-sku-catalog__enhanced__vendor-platform-analysis.csv` - Enhanced analysis
- `2025-08-20__analysis__multi-api-sku-insights.json` - Analysis results

### 2. API Coverage & Parity Matrix
**Schema**: vendor, api, feature, status{GA|Preview|NA}, added_date, doc_url

- `api_coverage_parity_matrix.csv` - Core feature parity matrix
- `api_coverage_parity_matrix.meta.yaml` - Metadata
- `2025-08-20__data__api-coverage-parity__multi-vendor__feature-matrix.csv` - Multi-vendor feature matrix
- `2025-08-20__data__api-coverage-parity__multi-vendor__feature-matrix.meta.yaml` - Metadata
- `api_coverage_analysis_results.json` - Analysis results

### 3. GA/Preview Cadence from Release Notes
**Schema**: vendor, api, feature, milestone, date, note_url

- `ga_preview_cadence.csv` - Core GA/preview tracking
- `ga_preview_cadence.meta.yaml` - Metadata
- `2025-08-20__data__ga-preview-cadence__multi-vendor__current-previews.csv` - Current preview status
- `2025-08-20__data__ga-preview-cadence__multi-vendor__current-previews.meta.yaml` - Metadata
- `2025-08-20__data__ga-preview-cadence__multi-vendor__feature-maturity.csv` - Feature maturity tracking
- `2025-08-20__data__ga-preview-cadence__multi-vendor__feature-maturity.meta.yaml` - Metadata
- `2025-08-20__data__ga-preview-cadence__multi-vendor__velocity-metrics.json` - Velocity metrics

### 4. Free-Tier Default Pathways
**Schema**: vendor, plan, entry_guide_url, default_path{gateway|single_api}, steps_to_first_query(int)

- `free_tier_default_pathways.csv` - Core pathways data
- `free_tier_default_pathways.meta.yaml` - Metadata
- `2025-08-20__data__free-tier-pathways__cloud-providers__onboarding-analysis.csv` - Cloud provider analysis
- `2025-08-20__data__free-tier-pathways__cloud-providers__onboarding-analysis.meta.yaml` - Metadata
- `2025-08-20__data__free-tier-pathways__step-breakdown__detailed-onboarding.csv` - Detailed onboarding steps
- `2025-08-20__data__free-tier-pathways__step-breakdown__detailed-onboarding.meta.yaml` - Metadata
- `2025-08-20__data__free-tier-pathways__velocity-analysis__developer-outcomes.csv` - Developer outcomes
- `2025-08-20__data__free-tier-pathways__velocity-analysis__developer-outcomes.meta.yaml` - Metadata

### 5. Marketplace Tile Taxonomy
**Schema**: marketplace, vendor, listing_id, tile_category, apis_on_tile[], first_seen, last_seen

- `marketplace-tile-taxonomy_2025-08-20.csv` - Current marketplace taxonomy
- `2025-08-20__data__marketplace-taxonomy__cloud-providers__tile-positioning.csv` - Cloud provider positioning
- `2025-08-20__data__marketplace-taxonomy__cloud-providers__tile-positioning.meta.yaml` - Metadata
- `2025-08-20__data__marketplace-taxonomy__multi-api-evolution__category-trends.csv` - Category trends
- `2025-08-20__data__marketplace-taxonomy__multi-api-evolution__category-trends.meta.yaml` - Metadata
- `2025-08-20__data__marketplace-taxonomy__vendor-strategies__multi-api-positioning.csv` - Vendor strategies
- `2025-08-20__data__marketplace-taxonomy__vendor-strategies__multi-api-positioning.meta.yaml` - Metadata
- `2025-08-20__data__marketplace-tile-taxonomy__historical__positioning-evolution.csv` - Historical evolution
- `2025-08-20__data__marketplace-tile-taxonomy__historical__positioning-evolution.meta.yaml` - Metadata
- `2025-08-20__data__marketplace-tile-taxonomy__multi-cloud__positioning-analysis.csv` - Multi-cloud analysis
- `2025-08-20__data__marketplace-tile-taxonomy__multi-cloud__positioning-analysis.meta.yaml` - Metadata

### 6. Pricing & Unit Alignment Table
**Schema**: vendor, api, unit_name, free_tier_quota, on_demand_price, notes, link

- `pricing_unit_alignment.csv` - Core pricing alignment data
- `pricing_unit_alignment.meta.yaml` - Metadata

## Demand-side Evidence (Adoption & Usage)

### 7. Case Studies Citing Gateway as Driver
**Schema**: vendor, customer, industry, use_case, gateway_cited(bool), quote(≤15 words), link

- `case_studies_gateway_driver.csv` - Gateway adoption case studies
- `case_studies_gateway_driver.meta.yaml` - Metadata

### 8. SDK/Client Unification Score
**Schema**: vendor, language, client_repo, unified_modes[], monthly_downloads, stars, last_release_date

- `2025-08-20__data__sdk-unification__multi-vendor__client-convergence.csv` - SDK unification analysis
- `2025-08-20__data__sdk-unification__multi-vendor__client-convergence.meta.yaml` - Metadata

### 9. Time-to-First-Query Benchmark
**Schema**: vendor, path{gateway|single}, steps, minutes, tester, date, script_url

- `2025-08-21__data__time-to-first-query__multi-vendor__benchmark-comparison.csv` - Multi-vendor benchmarks
- `2025-08-21__data__time-to-first-query__multi-vendor__benchmark-comparison.meta.yaml` - Metadata
- `2025-08-21__data__time-to-first-query__step-breakdown__detailed-timing.csv` - Detailed timing breakdown
- `2025-08-21__data__time-to-first-query__step-breakdown__detailed-timing.meta.yaml` - Metadata
- `2025-08-21__analysis__time-to-first-query__statistical-summary.json` - Statistical analysis

### 10. Job-Postings Signal
**Schema**: source, employer, title, keywords[], api_mentions[], date

- `2025-08-20__data__job-postings-signal__aggregated__multi-api-demand.csv` - Job market analysis

### 11. Stack Overflow/Forum Tag Mix
**Schema**: platform_tag, api_tag, count, month

- `stackoverflow_forum_tag_mix.csv` - Core forum data
- `stackoverflow_forum_tag_mix.meta.yaml` - Metadata
- `2025-08-20__data__stackoverflow-forum-tag-mix__stackoverflow__tag-snapshot.csv` - Current snapshot
- `2025-08-20__data__stackoverflow-forum-tag-mix__stackoverflow__quarterly-trends.csv` - Quarterly trends

## Economics & Business Signaling

### 12. Earnings Deck Driver Mentions
**Schema**: vendor, quarter, slide_ref, driver_rank, phrasing, link

- `earnings_deck_driver_mentions.csv` - Earnings call analysis
- `earnings_deck_driver_mentions.meta.yaml` - Metadata

### 13. ARR/Revenue Attribution Hints
**Schema**: vendor, segment, metric, value, period, source_link, inference_note

- `2025-08-20__data__arr-revenue-attribution__multi-vendor__gateway-sku-revenue.csv` - Gateway SKU revenue
- `2025-08-20__data__arr-revenue-attribution__multi-vendor__gateway-sku-revenue.meta.yaml` - Metadata
- `2025-08-20__data__arr-revenue-attribution__developer-adoption__platform-growth-metrics.csv` - Growth metrics
- `2025-08-20__data__arr-revenue-attribution__developer-adoption__platform-growth-metrics.meta.yaml` - Metadata

### 14. FinOps Outcomes from Public Posts
**Schema**: company, before_cost, after_cost, delta_pct, notes, link

- `2025-08-20__data__finops-outcomes__public-posts__database-consolidation.csv` - Public cost outcomes
- `2025-08-20__data__finops-outcomes__public-posts__database-consolidation.meta.yaml` - Metadata
- `2025-08-20__data__finops-outcomes__egress-optimization__database-consolidation.csv` - Egress optimization
- `2025-08-20__data__finops-outcomes__egress-optimization__database-consolidation.meta.yaml` - Metadata

## Standards & Ecosystem

### 15. Standards Adoption Tracker
**Schema**: standard, vendor, feature_subset, status{GA|Preview|Roadmap|NA}, date, link

- `standards_adoption_tracker.csv` - Standards adoption tracking
- `standards_adoption_tracker.meta.yaml` - Metadata

### 16. Connector/BI Federation Coverage
**Schema**: tool, vendor, gateway_supported(bool), api_modes[], version, link

- `2025-08-20__data__bi-etl-federation__connector-coverage__gateway-support.csv` - BI/ETL connector support
- `2025-08-20__data__bi-etl-federation__connector-coverage__gateway-support.meta.yaml` - Metadata

### 17. Migration Guides & Shims Registry
**Schema**: vendor, from_api, to_api, guide_url, maintained(bool), last_updated

- `2025-08-20__data__migration-guides__multi-vendor__cross-api-migration.csv` - Cross-API migration guides
- `2025-08-20__data__migration-guides__multi-vendor__cross-api-migration.meta.yaml` - Metadata

## Performance & Reliability

### 18. Typical-Query Penalty Dataset
**Schema**: engine, api, workload_id, native_ms, gateway_ms, delta_pct, env_hash

- `2025-08-20__data__gateway-penalty__multi-platform__query-performance.csv` - Multi-platform performance
- `2025-08-20__data__gateway-penalty__multi-platform__query-performance.meta.yaml` - Metadata
- `2025-08-20__data__gateway-penalty__comprehensive__query-performance.csv` - Comprehensive performance
- `2025-08-20__data__gateway-penalty__comprehensive__query-performance.meta.yaml` - Metadata
- `2025-08-20__data__gateway-penalty__tpc-benchmarks__standardized-workloads.csv` - TPC benchmarks
- `2025-08-20__data__gateway-penalty__tpc-benchmarks__standardized-workloads.meta.yaml` - Metadata
- `2025-08-20__data__gateway-penalty__platform-summary__performance-recommendations.csv` - Performance recommendations
- `2025-08-20__data__gateway-penalty__platform-summary__performance-recommendations.meta.yaml` - Metadata

### 19. Incident/Support Signals
**Schema**: vendor, api, issue_type, count, window, source

- `2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.csv` - API quality patterns
- `2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.meta.yaml` - Metadata
- `2025-08-20__data__incident-support-signals__real-world__api-issues.csv` - Real-world issues
- `2025-08-20__data__incident-support-signals__real-world__api-issues.meta.yaml` - Metadata
- `incident_analysis_results.json` - Analysis results

## Market Prevalence & Trends

### 20. Platform Launches Including Multi-API
**Schema**: platform, launch_date, default_multi_api(bool), description, link

- `platform_launches_multi_api.csv` - Platform launch tracking
- `platform_launches_multi_api.meta.yaml` - Metadata

### 21. "Gateway" Term Tracking
**Schema**: source, date, context, exact_phrase(≤15 words), link

- `2025-08-20__data__gateway-terms__industry-discourse__terminology-tracking.csv` - Gateway terminology tracking
- `2025-08-20__data__gateway-terms__industry-discourse__terminology-tracking.meta.yaml` - Metadata

### 22. Google Trends Bundle
**Schema**: term, region, week, index

- `2025-08-20__data__google-trends__multi-api-gateway__search-volume.csv` - Search volume trends
- `2025-08-20__data__google-trends__multi-api-gateway__search-volume.meta.yaml` - Metadata
- `google_trends_bundle_stats.json` - Bundle statistics
- `google_trends_related_data.json` - Related search data

## Additional Data Files

### Analysis and Support Files
- `analyze_api_coverage.py` - API coverage analysis script
- `analyze_incident_patterns.py` - Incident pattern analysis script
- `gateway_search_template.csv` - Search template for gateway data
- `collection_methodology.md` - Data collection methodology
- `api_coverage_summary_2025-08-20.md` - API coverage summary
- `incident_signals_summary.md` - Incident signals summary
- `marketplace_tile_taxonomy_analysis.md` - Marketplace analysis

### Related Research Areas
- `2025-08-20__data__database-platforms__gateway-apis__multi-protocol-support.csv` - Database platform support
- `2025-08-20__data__database-platforms__gateway-apis__multi-protocol-support.meta.yaml` - Metadata
- `2025-08-20__data__convergence-patterns__multi-vendor__paradigm-matrix.csv` - Convergence patterns
- `2025-08-20__data__convergence-patterns__multi-vendor__paradigm-matrix.meta.yaml` - Metadata
- `2025-08-21__data__developer-friction-points__qualitative__onboarding-barriers.csv` - Developer friction analysis
- `2025-08-21__data__developer-friction-points__qualitative__onboarding-barriers.meta.yaml` - Metadata

## File Naming Convention

Files follow this pattern:
- **Legacy files**: `category_name.csv` with optional `.meta.yaml`
- **New timestamped files**: `YYYY-MM-DD__data|analysis__category__subcategory__description.csv|json`
- **Analysis files**: Include `__analysis__` in the path and typically use `.json` format
- **Metadata files**: Use `.meta.yaml` extension and contain schema, collection notes, and data lineage

## Research Categories Not Yet Populated

The following categories from the README.md have no corresponding data files yet:

### Synthesis Scaffolding (Categories 23-26)
- Source Registry & Tiering
- Claim→Evidence Map  
- Quote Ledger
- Multi-API Gateway Index (MAGI)

These meta-datasets should be created to support rigorous evidence tracking and analysis.