# Database Compute Storage Separation

## Thesis Statement
> In cloud native orgs, the move to define everything as compute, network or storage will seperate database systems into compute and storage componenets which will completely change the database industry by 2035

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


1) Adoption & Architecture Signals

1.1 Vendor architecture census (annual panel)
	•	What/why: Track which managed databases expose independently scalable compute/storage and how (shared-nothing w/ remote log, shared-disk, object-backed, NVMe-oF, etc.). Anchors the trend line to 2035.
	•	Fields: vendor, product, engine_type (OLTP/OLAP/HTAP/vector/TS/graph), storage_medium (local NVMe / block / object / hybrid), compute_storage_independent (bool), scale_unit_compute, scale_unit_storage, fabric (ENA/RDMA/Infiniband), cache_layer (buffer cache/remote cache), notes, first_seen_date.
	•	Source/compose: Product docs, architecture whitepapers, conference talks; normalize into a yearly snapshot. When missing, infer from deployment guides and instance/storage SKU coupling.

1.2 Feature release timeline of enabling primitives
	•	What/why: Correlate cloud primitives (high IOPS block, multi-attach, zonal object tiers, RDMA, GPUDirect Storage) with database architecture shifts.
	•	Fields: provider, feature, class (block/object/network), region_coverage_%, launch_date, perf_limits (IOPS/throughput/lat), price_unit.
	•	Source/compose: Cloud provider changelogs; build a time series per region.

1.3 SKU decoupling scorecard
	•	What/why: Measures how decoupled pricing and provisioning are.
	•	Fields: product, compute_priced_independently (y/n), storage_priced_independently (y/n), min_storage_per_vCPU, required_instance_storage (y/n), autoscale_modes (compute/storage/both), billing_granularity (sec/min/hr/GB-hr).
	•	Source/compose: Pricing pages + calculators; encode rules as YAML and render a score 0–5.

⸻

2) Cost/TCO Evidence

2.1 Workload-level cost curves (local vs disaggregated)
	•	What/why: Quantify inflection points where remote storage beats local NVMe on $/QPH or $/TPM.
	•	Fields: workload (TPC-C/H/YCSB/Vector-ANN), read_write_mix, dataset_GB, instance_family, storage_type (local NVMe, block, object+cache), throughput_ops/s, p95_latency_ms, cost_per_hour, cost_per_10^6_ops, cost_per_query.
	•	Source/compose: Run controlled benchmarks; when not possible, simulate using vendor-published perf/price and validated scaling laws.

2.2 Elasticity dividend dataset
	•	What/why: Savings from scaling compute to zero or to match diurnal demand while storage persists.
	•	Fields: tenant_id, time, qps, cpu_%, compute_nodes, storage_GB, autoscale_event (up/down/off), idle_cost/hr, saved_cost/hr.
	•	Source/compose: Real telemetry if available; otherwise synthesize from typical SaaS diurnal curves and provider billing granularity.

2.3 Data egress & duplication ledger
	•	What/why: Separation often pairs with lake/object copies; track whether egress/dup hits TCO.
	•	Fields: pipeline (OLTP→object, OLAP→ML), bytes_moved_GB, region_pairs, egress_cost, dup_storage_cost, compression_ratio, change_rate_%.
	•	Source/compose: ETL job logs or modeled from CDC/streaming rates.

⸻

3) Performance & Latency Tax

3.1 Latency decomposition microbench
	•	What/why: Measure the “separation tax” vs. local media.
	•	Fields: op (get/put/commit/read-amp levels), path (local NVMe, block over TCP, RDMA, object via SDK), p50/p95/p99_us, jitter_us, cpu_sys_%, net_bw_Gbps, cache_hit_%.
	•	Source/compose: Harness using fio/db_bench/YCSB + custom commit-log tests; run on varied fabrics (with/without RDMA).

3.2 Log-structured vs page-oriented sensitivity
	•	What/why: Some engines tolerate remote writes better (append-only). Quantify delta.
	•	Fields: engine_impl (LSM/B-tree/columnar), write_amp, read_amp, compaction_bw, remote_log_latency_us, throughput_ops/s.
	•	Source/compose: Reproduce with open engines (e.g., LSM-style vs B-tree) or simulate with calibrated models.

3.3 Cross-AZ/region penalty table
	•	What/why: Separation can span failure domains; capture tail-latency effects.
	•	Fields: topology (same AZ / multi-AZ / multi-region), rtt_ms, p99_txn_latency_ms, availability_target, consistency_mode (1/QUORUM/ALL), cost_delta_%.
	•	Source/compose: Ping/iperf + db benchmarks; blend with SLA math.

⸻

4) Reliability, Ops & Failure Modes

4.1 Incident taxonomy with root causes
	•	What/why: Do storage-network brownouts dominate? Are repairs faster when compute is stateless?
	•	Fields: incident_id, date, blast_radius (tenant/cluster/region), root_cause (storage, network, compute, control-plane), mttr_hr, rpo/rto, arch_type (coupled/decoupled), mitigation (scale-out/evict/cache-warm).
	•	Source/compose: Public postmortems; your own SRE logs; otherwise build a synthetic catalog from known patterns to support scenario analysis.

4.2 Cache warm/cold behavior traces
	•	What/why: Separation relies on hot caches; quantify warm-up pain after scale-to-zero or failover.
	•	Fields: event (scale-up/failover/restart), cache_size_GB, warm_time_min_to_95%_hit, request_p95_ms_during_warm, miss_penalty_ms.
	•	Source/compose: Record cache metrics from engines with buffer/page caches or remote row caches.

4.3 Snapshot/backup/restore SLOs
	•	What/why: Object-backed snapshots change RPO/RTO economics.
	•	Fields: dataset_TB, snapshot_kind (incremental/full), throughput_GB/min, restore_to_serving_min, S3/listing_penalties_ms, concurrency.
	•	Source/compose: Instrument backup tools or simulate with object store APIs.

⸻

5) Organization, Procurement & Governance

5.1 Spend alignment matrix (FinOps)
	•	What/why: Evidence that teams procure compute & storage independently as policy.
	•	Fields: org_unit, budget_line (compute/storage/network), chargeback_model, tagging_coverage_%, idle_%, reserved_%, spot_%.
	•	Source/compose: Cloud cost exports; if unavailable, construct typical FinOps models and test sensitivity.

5.2 Contract & SKU governance dataset
	•	What/why: Are contracts SKU’d as separate “compute pools” and “storage pools”?
	•	Fields: vendor, contract_term, min_commit_compute_$, min_commit_storage_$, bursting_rights, overage_rate.
	•	Source/compose: Heavily redacted enterprise contracts or analyst notes; otherwise encode public pricing + common enterprise terms to simulate.

⸻

6) Workload Suitability & Boundaries

6.1 Suitability matrix by workload
	•	What/why: Clarify where separation wins/loses (OLTP, OLAP, HTAP, vector ANN, time-series, graph).
	•	Fields: workload_type, latency_budget_ms, write_intensity, read_locality (hot/cold), state_size_GB_per_core, cacheability, acceptable_tax_ms, recommended_arch (coupled/decoupled/hybrid).
	•	Source/compose: Literature + your benchmarks; codify into a rubric.

6.2 Transactional durability under remote commit log
	•	What/why: Validate if 2–5 ms added RTT breaks SLAs.
	•	Fields: txn_type (single-row/multi-partition), consistency, rtt_ms, p99_commit_ms, abort_rate_%, tail_amplification_factor.
	•	Source/compose: Targeted microbench with adjustable artificial RTT.

6.3 Vector/AI augmentation paths
	•	What/why: Many “storage-centric” stacks pair object store parquet/embeddings with ephemeral compute.
	•	Fields: feature_store_location, embedding_store (object/kv), batch_inference_cost/hr, online_inference_p95_ms, rebuild_time_min, drift_%/week.
	•	Source/compose: ML pipelines or synthetic DAGs.

⸻

7) Cross-System Interop (Lake ↔ DB)

7.1 Dataflow DAG inventory
	•	What/why: How often does operational DB offload to object storage and read back via SQL engines?
	•	Fields: source_system, sink_system, refresh_mode (stream/batch), interval_min, lag_p95_min, data_size_GB, cost_per_run, failure_rate_%.
	•	Source/compose: Orchestrator logs (Airflow/DBT); or compose exemplar DAGs and cost them.

7.2 “Hot set on fast media” ratios
	•	What/why: Quantify hybrid patterns: small hot set on local NVMe, cold on object storage.
	•	Fields: dataset_total_GB, hot_set_GB, hot_fraction_%, hit_rate_%, nvme_cost/mo, object_cost/mo, perf_delta_%.
	•	Source/compose: Cache metrics + storage billing; simulate if needed.

⸻

8) Derived Metrics & Indices (ready for figures)
	•	Separation Elasticity (SE): distinct_compute_storage_ratios_used / days_observed
Shows how often teams actually dial compute/storage independently.
	•	Latency Tax (%): (p95_remote - p95_local) / p95_local
Clear, stack-agnostic measure of separation penalty.
	•	Utilization Lift: baseline_cost_at_peak - cost_with_rightsizing normalized by QPS
Captures savings from elastic compute on steady storage.
	•	Failure Domain Isolation Score: weighted sum of multi-AZ, blast_radius, MTTR, presence of stateless_compute
Tests reliability claims of separation.
	•	Data Gravity Index: egress_GB * distance_factor(region_pairs)
Flags hidden costs when compute chases data across zones/regions.

⸻

9) Practitioner Signals (qual → quant)

9.1 Survey/panel of architects
	•	What/why: Validate perceived benefits/risks and where teams are on the curve.
	•	Fields: industry, current_arch (coupled/decoupled/hybrid), drivers (cost, scale, reliability), blockers (latency, tooling, ops), time_to_adopt, SLA_targets, topologies.
	•	Compose: Short survey seeded to DB/SRE leaders; code responses to ordinal scales.

9.2 Postmortem coding study
	•	What/why: Classify 100+ public incidents by whether separation helped or hurt restoration.
	•	Fields: From 4.1 plus did_separation_help (y/n), evidence_excerpt (≤15 words), follow-up_action.
	•	Compose: Annotator guidelines + inter-rater agreement.

⸻

10) Counter-Evidence Datasets (intentionally)
	•	Ultra-low-latency OLTP traces where p99≤2 ms is mandatory and remote storage fails SLA.
	•	High write-amplification workloads (e.g., secondary index storms) where networked writes multiply costs.
	•	Strict data residency cases where compute cannot follow data, forcing expensive egress or co-tenancy.
	•	On-prem edge deployments with no high-bandwidth fabrics—coupled storage outperforms.
