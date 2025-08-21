# Object Storage Lake Tables TCO Displacement

## Thesis Statement
> In cloud-first orgs, object storage + table formats will displace DB-native storage because decoupled compute cuts TCO, resulting in >50% of analytics queries running directly on lake tables by 2030

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

Adoption & Prevalence
	1.	Query share by substrate (DW-native vs lake tables)

	•	What: Percent of analytics queries hitting DB-native storage vs external/lake tables.
	•	Why: Direct test of “>50% by 2030.”
	•	Sources: Cloud billing & query logs (BQ, Snowflake, Databricks SQL, Athena, Trino/Presto), engine metadata.
	•	Columns: ts, account_id, engine, table_type{native|external|iceberg|delta|hudi}, query_count

	2.	Lake table format penetration

	•	What: Iceberg/Delta/Hudi share across orgs/datasets.
	•	Why: Proxy for lake table maturity.
	•	Sources: Table catalogs (Glue, Unity, HMS), repo telemetry, vendor reports.
	•	Columns: org_id, catalog, format, dataset_count, total_tb

	3.	Engine coverage for lake tables

	•	What: Which SQL/query engines read/write each format.
	•	Why: Ecosystem breadth lowers switching cost.
	•	Sources: Docs, release notes, connectors matrix.
	•	Columns: engine, format, read_support, write_support, version_added

	4.	Managed “lakehouse SKU” availability

	•	What: Presence of first-class SKUs for lake tables by vendor/cloud/region.
	•	Why: Productization indicator.
	•	Sources: Vendor pricing pages, product catalogs.
	•	Columns: vendor, product, cloud, region, lakehouse_sku{0/1}, ga_date

Cost & TCO (Direct)
	5.	Storage cost curve by substrate

	•	What: $/TB-month for S3/GCS/ADLS vs DW-native storage tiers.
	•	Why: Core TCO driver.
	•	Sources: Cloud pricing pages, historical price archives.
	•	Columns: cloud, region, substrate{object|dw-native}, redundancy, price_per_tb_month, effective_date

	6.	Compute cost per TB scanned

	•	What: Normalized $/TB scanned by engine and workload class.
	•	Why: Compares decoupled compute to warehouse pricing.
	•	Sources: Billing exports, query stats.
	•	Columns: engine, workload{etl|bi|adhoc}, tb_scanned, compute_cost_usd, usd_per_tb

	7.	Table maintenance cost

	•	What: Monthly spend for compaction, clustering, vacuum, optimize jobs.
	•	Why: Hidden cost in lake stacks.
	•	Sources: Job schedulers (Airflow/Databricks Jobs), billing.
	•	Columns: org_id, format, job_type, runs, compute_hours, cost_usd, data_tb_touched

	8.	Data movement tax (egress/ingest)

	•	What: $ from cross-AZ/cloud movement, external table reads.
	•	Why: TCO leakage for decoupled architectures.
	•	Sources: Cloud bills, network telemetry.
	•	Columns: cloud, movement_type, gb_moved, cost_usd, source_region, dest_region

	9.	Catalog & governance service cost

	•	What: Spend for catalogs, lineage, policy engines.
	•	Why: Overhead vs “all-in warehouse.”
	•	Sources: SaaS invoices, cloud bills.
	•	Columns: service, pricing_model, monthly_active_objects, cost_usd

	10.	People cost for ops

	•	What: FTE time per TB or per 100 tables (oncall, maintenance, upgrades).
	•	Why: Opex component of TCO.
	•	Sources: Time tracking, interviews, tickets.
	•	Columns: org_id, stack_type{lake|dw}, fte_hours_month, tables, tb, incidents

Performance, Efficiency & Utilization
	11.	Latency/throughput distributions by workload

	•	What: P50/P95/P99 latency and concurrency for BI/ETL/Ad-hoc.
	•	Why: Where lake tables shine/falter.
	•	Sources: Engine query history (Trino, Spark SQL, Snowflake, BQ).
	•	Columns: engine, workload, p50_ms, p95_ms, p99_ms, qps_peak

	12.	Compute utilization & idle

	•	What: % idle time and autoscale efficiency (clusters vs serverless).
	•	Why: Decoupled compute savings come from elasticity.
	•	Sources: Cluster metrics, autoscaler logs.
	•	Columns: engine, mode{cluster|serverless}, cpu_util_avg, idle_pct, scale_events_day

	13.	Read amplification & skipping effectiveness

	•	What: Bytes scanned vs bytes returned; data skipping/index hit rate.
	•	Why: Iceberg/Delta optimizations’ real gains.
	•	Sources: Query profiles, file footers/stats.
	•	Columns: format, partitioning, bytes_scanned, bytes_returned, skipping_rate

	14.	Compaction ROI

	•	What: Latency/scan cost deltas before/after optimize/compaction.
	•	Why: Payback period for maintenance jobs.
	•	Sources: Job logs + query metrics.
	•	Columns: dataset_id, before_latency_ms, after_latency_ms, job_cost_usd, savings_usd_month

Reliability, Security & Governance
	15.	Incident & recovery metrics

	•	What: Incidents related to metadata corruption, stale snapshots, accidental deletes; MTTR.
	•	Why: Risk side of TCO.
	•	Sources: Postmortems, incident trackers.
	•	Columns: org_id, stack_type, incident_type, mttr_minutes, data_loss_gb

	16.	Rollback & time travel usage

	•	What: Frequency and success rate of snapshot/rollback.
	•	Why: Operational safety value of lake tables.
	•	Sources: Catalog logs, engine audit.
	•	Columns: format, rollbacks_month, median_rollback_time_s, success_rate

	17.	Policy parity index

	•	What: Coverage of row/column-level security, masking, audit, lineage.
	•	Why: Governance completeness vs warehouses.
	•	Sources: Config scans, policy engines.
	•	Columns: stack_type, control, supported{0/1}, enforced{0/1}

	18.	Schema evolution cadence

	•	What: Add/drop/rename column events and downstream breakage.
	•	Why: Flexibility (benefit) vs fragility (cost).
	•	Sources: Catalog history, pipeline failures.
	•	Columns: dataset_id, evolution_event, downstream_failures, recovery_time_minutes

Migration & Data Gravity
	19.	Migration funnel

	•	What: Count/size/duration of migrations from DW-native to lake tables (and vice-versa).
	•	Why: Net flow direction and friction.
	•	Sources: PMO trackers, change tickets, vendor PS logs.
	•	Columns: source_stack, target_stack, tb_migrated, duration_days, blockers_count

	20.	System-of-record placement

	•	What: Where golden datasets live (object store vs DW-native).
	•	Why: Power center of analytics.
	•	Sources: Data product catalogs, ownership tags.
	•	Columns: domain, dataset, sor{lake|dw}, tb, consumers_count

	21.	Pipeline landing patterns

	•	What: % pipelines landing raw in object storage first vs DW first.
	•	Why: Upstream architectural bias.
	•	Sources: Orchestrator DAGs, storage events.
	•	Columns: pipeline_id, first_landing{object|dw}, tb_month, engines_downstream

Ecosystem Maturity & Standards
	22.	BI/Tooling compatibility matrix

	•	What: Direct query/write support for Iceberg/Delta/Hudi across BI & ELT tools.
	•	Why: Friction to org-wide adoption.
	•	Sources: Tool docs, connector catalogs.
	•	Columns: tool, capability{read|write|pushdown}, format, status{ga|preview}

	23.	Spec/version adoption

	•	What: Iceberg spec features (row-level deletes, spec v2/v3), Delta protocol versions in the wild.
	•	Why: Feature parity needed to replace DW-native.
	•	Sources: Table metadata, commit logs.
	•	Columns: dataset_id, format, spec_version, features{list}, last_upgraded_at

	24.	Open file/format features in use

	•	What: Parquet encodings, stats, bloom filters, object store consistency settings.
	•	Why: Performance & correctness envelope.
	•	Sources: File footers, storage config.
	•	Columns: dataset_id, parquet_feature, enabled{0/1}

Counterevidence & Boundary Cases
	25.	Small/interactive workload head-to-head

	•	What: Cost & latency for small BI dashboards (native DW vs lake tables).
	•	Why: Where warehouses often win.
	•	Sources: Repro benchmarks, prod traces.
	•	Columns: workload_id, engine, median_latency_ms, p95_ms, cost_usd_session

	26.	Governed multi-region scenarios

	•	What: Cost and complexity of strong governance + multi-region replication.
	•	Why: Potential TCO reversal points.
	•	Sources: Replication bills, policy engines.
	•	Columns: regions, stack_type, gb_replicated, policy_objects, monthly_cost_usd

	27.	Workload mix sensitivity

	•	What: TCO vs % interactive BI vs batch ETL vs ML.
	•	Why: Reveal thresholds where lake wins/loses.
	•	Sources: Portfolio analysis + modeled runs.
	•	Columns: org_id, mix_bi_pct, mix_etl_pct, mix_ml_pct, tco_usd_month

Derived Metrics You Can Compute
	•	Lake Share of Queries:
lake_share = queries_on_{iceberg|delta|hudi} / total_queries
	•	All-in Cost per TB Scanned:
(compute_cost + maintenance_cost + catalog_cost + egress_cost) / tb_scanned
	•	Elasticity Dividend:
1 – (idle_time_serverless / idle_time_clusters)
	•	Maintenance Payback (days):
optimize_job_cost / (post_optimize_daily_savings)
	•	Policy Parity Score (0–1):
controls_supported_and_enforced / controls_required

Practical Tips
	•	Normalization: Record region, redundancy, and storage class to avoid apples-to-oranges.
	•	Cohorts: Track cohorts by org size, industry, and workload mix for fair comparisons.
	•	Time windows: Keep monthly snapshots to show trends toward 2030.
	•	Replicability: Save raw billing & query logs (sanitized) alongside derived tables in datasets/.
