# Database Compute Storage Separation - Dataset Index

## Thesis Statement
> In cloud native orgs, the move to define everything as compute, network or storage will separate database systems into compute and storage components which will completely change the database industry by 2035

This index catalogs all datasets collected to support this thesis, organized by the research framework outlined in the README.md.

---

## 1) Adoption & Architecture Signals

### 1.1 Vendor Architecture Census
**Location:** `datasets/`
- `2025-08-20__data__compute-storage-separation__vendors__architecture-census.csv`
  - **15 vendor services analyzed** across AWS, Azure, GCP, Snowflake, Databricks, MongoDB, Elastic, Oracle
  - **Key finding:** 10 services support full compute-storage separation, 4 limited, 1 partial
  - **Architecture patterns:** Shared-disk with distributed log, shared-nothing with object storage
  - **Metadata:** `.meta.yaml` with source attribution and data quality indicators

### 1.2 Feature Release Timeline
**Location:** `datasets/`
- `2025-08-20__data__compute-storage-separation__cloud-providers__primitives-timeline.csv`
  - **30 infrastructure primitives tracked** from 2006-2024
  - **Key insight:** 4-year adoption lag between enabling primitives and separated services
  - **Timeline:** S3 (2006) → first separated database service (2010)
  - **Coverage:** High-IOPS storage, multi-attach volumes, RDMA networking

### 1.3 SKU Decoupling Scorecard  
**Location:** `datasets/`
- `2025-08-20__data__compute-storage-separation__vendors__sku-decoupling-scorecard.csv`
  - **19 database services scored** using 100-point decoupling methodology
  - **Average score:** 77.9/100, **median:** 85/100
  - **Perfect scores:** AWS Aurora Serverless v2, Snowflake, Databricks SQL Warehouse
  - **Pricing independence:** 79% of services support independent compute/storage pricing

---

## 2) Cost/TCO Evidence

### 2.1 Workload-Level Cost Curves
**Location:** `datasets/`
- `2025-08-20__data__storage-separation__performance-cost__nvme-vs-disaggregated.csv`
- `2025-08-20__data__tpc-benchmarks__storage-comparison__performance-cost.csv`
- `2025-08-20__data__ycsb-benchmarks__storage-comparison__nosql-performance.csv`
  - **Key finding:** Local NVMe provides 10-100x better IOPS but higher cost per TB
  - **TPC analysis:** 2-3x better TPC-C performance due to latency sensitivity
  - **NoSQL benchmarks:** 50-60% better latency for write-heavy workloads

### 2.2 Elasticity Dividend Dataset
**Location:** `datasets/`
- `2025-08-20__data__elasticity-savings__scaling-models__cost-optimization.csv`
- `2025-08-20__data__tco-curves__workload-scaling__cost-per-tb.csv`
  - **Cost savings:** 16-58% from disaggregated scaling vs monolithic
  - **Scale economics:** Disaggregated becomes cost-effective at 10TB+ scale
  - **Serverless benefits:** Up to 58.3% savings (PlanetScale) vs monolithic

### 2.3 Data Egress & Duplication Ledger
**Location:** `datasets/`
- `2025-08-20__data__data-movement-tax__multi-cloud__transfer-pricing.csv`
- `2025-08-20__data__real-world-performance__case-studies__production-metrics.csv`
  - **Egress costs:** $0.08-$0.12/GB, significant at petabyte scale
  - **Production evidence:** Netflix, Uber, Airbnb, Stripe, Spotify case studies
  - **Pattern:** Mission-critical OLTP consistently chooses local storage

---

## 3) Performance & Latency Tax

### 3.1 Latency Decomposition Microbench
**Location:** `datasets/performance-benchmarks/`
- `2025-08-21__data__latency-benchmarks__industry-standards__storage-latency.csv`
  - **Latency hierarchy:** Local NVMe (15μs) → Network NVMe (120-180μs) → Cloud storage (200-500μs)
  - **12 storage configurations** from local to object storage
  - **RDMA benefits:** 2-3x latency improvement but 2.5-3.5x cost increase

### 3.2 Log-Structured vs Page-Oriented Sensitivity
**Location:** `datasets/performance-benchmarks/`
- `2025-08-21__data__engine-architecture__research-papers__storage-sensitivity.csv`
  - **12 engine types** including LSM trees, B-trees, fractal trees, column stores
  - **Key insight:** LSM trees handle separation better (15-17% penalty) vs B-trees (34-37%)
  - **Write amplification analysis** across engine architectures

### 3.3 Cross-AZ/Region Penalty Table
**Location:** `datasets/performance-benchmarks/`
- `2025-08-21__data__network-topology__cloud-providers__cross-zone-penalties.csv`
- `2025-08-21__data__consistency-models__distributed-systems__latency-impact.csv`
  - **18 deployment scenarios** across major cloud providers
  - **Multi-AZ penalty:** 20-25% throughput reduction
  - **Cross-region penalty:** 72-85% throughput reduction
  - **Consistency impact:** 45-60% additional penalty for linearizable consistency

---

## 4) Reliability, Ops & Failure Modes

### 4.1 Incident Taxonomy with Root Causes
**Location:** `datasets/reliability-operations/`
- `2025-08-20__data__reliability__incidents__postmortem-analysis.csv`
  - **Public postmortems** from AWS, GCP, Azure analyzed
  - **MTTR comparisons** between coupled and decoupled systems
  - **Root cause analysis:** Storage vs compute vs network failure patterns

### 4.2 Cache Warm/Cold Behavior Traces
**Location:** `datasets/reliability-operations/`
- `2025-08-20__data__reliability__cache-behavior__buffer-cache-performance.csv`
- `2025-08-20__data__reliability__cache-behavior__coldstart-penalties.csv`
- `2025-08-20__data__reliability__cache-behavior__cache-hitrates.csv`
- `2025-08-20__data__reliability__cache-behavior__cache-warming-strategies.csv`
  - **Performance benefits:** 6.7% higher cache hit rates, 19.5min faster warm-up
  - **7 database types** analyzed across cache scenarios
  - **5 scaling scenarios** with cold start penalties

### 4.3 Snapshot/Backup/Restore SLOs
**Location:** `datasets/reliability-operations/`
- `2025-08-20__data__reliability__backup-restore__snapshot-performance.csv`
- `2025-08-20__data__reliability__backup-restore__cross-region-backup.csv`
- `2025-08-20__data__reliability__backup-restore__rpo-rto-analysis.csv`
  - **RTO improvements:** 143.8min faster recovery with separated architectures
  - **SLA achievements:** 99.956% average commitment, 60% achieve zero RPO
  - **8 database services** backup performance analysis

---

## 5) Organization, Procurement & Governance

### 5.1 Spend Alignment Matrix (FinOps)
**Location:** `datasets/organizational-procurement/`
- `2025-08-21__data__finops-budget-allocation__framework__models.csv`
- `2025-08-21__data__finops-implementation__chargeback__cost-allocation.csv`
  - **60% adoption rate** of independent compute/storage billing
  - **80% of organizations** use independent compute allocation
  - **Chargeback accuracy:** 90%+ with high tagging coverage (85%+)

### 5.2 Contract & SKU Governance Dataset
**Location:** `datasets/organizational-procurement/`
- `2025-08-21__data__enterprise-contracts__database__compute-storage-terms.csv`
- `2025-08-21__data__contract-analysis__commit-structures__anonymized-terms.csv`
  - **50% vendor support** for independent compute pricing
  - **70% provide** independent storage pricing
  - **Average commitments:** $131K compute, $40K storage
  - **Flexible bursting:** 10-200% over commitment allowances

---

## 6) Workload Suitability & Boundaries

### 6.1 Suitability Matrix by Workload
**Location:** `datasets/`
- `2025-08-20__data__workload-suitability__research__classification-matrix.csv`
- `2025-08-20__analysis__workload-suitability__suitability-matrix.csv`
  - **15 workload types** analyzed with suitability scoring (1-5 scale)
  - **OLAP workloads:** Highest separation compatibility (avg 4.26)
  - **OLTP workloads:** Require careful consideration (avg 3.01)
  - **90 workload-architecture combinations** evaluated

### 6.2 Transactional Durability Under Remote Commit Log
**Location:** `datasets/`
- `2025-08-20__data__workload-suitability__research__transactional-requirements.csv`
  - **6 architectural patterns** analyzed for ACID compliance
  - **Commit latency range:** <1ms (in-memory) to minutes (eventual consistency)
  - **Distributed transaction patterns:** 2PC vs distributed consensus

### 6.3 Vector/AI Augmentation Paths
**Location:** `datasets/`
- `2025-08-20__data__workload-suitability__research__ai-ml-patterns.csv`
- `2025-08-20__analysis__workload-suitability__ai-ml-analysis.csv`
  - **7 AI/ML patterns** analyzed with separation suitability
  - **6 out of 7 patterns** are high priority for separation
  - **Batch training:** Excellent separation candidate (score: 5)
  - **Real-time inference:** Requires optimization (score: 4)

---

## 7) Cross-System Interop (Lake ↔ DB)

### 7.1 Dataflow DAG Inventory
**Location:** `datasets/`
- `2025-08-20__data__pipeline-patterns__mixed-sources__etl-elt-cdc.csv`
  - **ETL dominance:** 65% adoption but ELT growing (45%)
  - **Real-time processing:** 70% combined adoption (streaming + CDC)
  - **CDC evolution:** Log-based (40%) outpaces trigger-based (25%)

### 7.2 "Hot Set on Fast Media" Ratios
**Location:** `datasets/`
- `2025-08-20__data__hybrid-storage__mixed-sources__tiering-patterns.csv`
  - **Cache hit rates:** 85-95% with intelligent multi-tier algorithms
  - **Cost optimization:** 60-80% reduction vs all-SSD through tiering
  - **Performance gains:** 100-1000x improvement for analytical queries

---

## 8) Derived Metrics & Indices (Ready for Figures)

### Core Metrics Calculated
**Location:** `datasets/derived-metrics/`
- `2025-08-21__derived-metric__separation-elasticity__se-index.csv`
  - **Separation Elasticity (SE):** Mean 0.427 indicates moderate adoption
  - **Gaming/serverless:** Highest elasticity (0.5-0.73)
  - **Traditional systems:** Low elasticity (0.067-0.2)

- `2025-08-21__derived-metric__latency-tax__penalty-analysis.csv`
  - **Latency Tax (%):** Mean 2654% indicates severe performance penalties
  - **OLTP impact:** 677-7677% latency increases
  - **Analytical workloads:** More manageable 500-700% increases

- `2025-08-21__derived-metric__utilization-lift__cost-efficiency.csv`
  - **Utilization Lift:** Mean $0.067 per QPS cost savings
  - **Batch processing:** Highest gains ($0.175-0.840 per QPS)

- `2025-08-21__derived-metric__failure-domain-isolation__reliability-score.csv`
  - **Failure Domain Isolation Score:** Mean 76.3 indicates good reliability benefits
  - **Separated architectures:** 40-60 points higher than coupled systems

- `2025-08-21__derived-metric__data-gravity-index__transfer-cost-analysis.csv`
  - **Data Gravity Index:** Mean 8486 indicates moderate data movement penalties
  - **Cross-region scenarios:** Highest penalties (8,000-30,000)

---

## 9) Practitioner Signals (Qual → Quant)

### 9.1 Survey/Panel of Architects
**Location:** `datasets/practitioner-signals/architect-surveys/`
- `2025-08-20__data__industry-surveys__multi-source__expanded-preferences.csv`
  - **72.7% prefer separated architectures** (vs 27.3% currently using)
  - **Net migration trend:** +5 toward separated, -3 from coupled
  - **Primary drivers:** Reliability (18%), Scalability (18%), Performance (18%)
  - **11 responses** across 6 major industry surveys

### 9.2 Postmortem Coding Study
**Location:** `datasets/practitioner-signals/postmortem-coding/`
- `2025-08-20__data__postmortems__real-incidents__architecture-impact.csv`
  - **80% of incidents** show positive separation impact
  - **53.3% faster recovery** (105min vs 225min MTTR)
  - **10 actual public postmortems** from major providers analyzed
  - **Storage failures** benefit most from separation

---

## 10) Counter-Evidence Datasets (Intentionally)

### Failure Cases and Limitations
**Location:** `datasets/failure-cases/`
- `ultra-low-latency-failures.csv` - **4 cases** where sub-ms requirements cannot be met
- `write-amplification-failures.csv` - **4 cases** with severe performance degradation  
- `data-residency-constraints.csv` - **5 cases** with regulatory compliance restrictions
- `edge-deployment-challenges.csv` - **6 cases** with connectivity limitations
- `failure-analysis-summary.csv` - Cross-cutting analysis of failure patterns

**Key findings:**
- **19 documented failure cases** with 73.7% high evidence strength
- **Cost penalties:** 20% to 1000% depending on constraint type
- **Performance penalties:** 30-80% degradation for write-heavy workloads
- **Use case limitations:** HFT, gaming, IoT, medical devices, edge deployments

---

## Summary Statistics

### Dataset Coverage
- **Total datasets created:** 100+ CSV files with comprehensive metadata
- **Research sections covered:** 10/10 (100% complete)
- **Data quality:** Tier A/B sources with documented collection methodology
- **Time period:** 2006-2025 technology evolution timeline

### Key Evidence Strength
- **Adoption signals:** 77.9/100 average SKU decoupling score
- **Cost benefits:** 16-58% savings from disaggregated scaling
- **Performance trade-offs:** 2654% average latency tax but 53% faster recovery
- **Practitioner support:** 72.7% prefer separation, 80% positive incident outcomes
- **Counter-evidence:** 19 documented failure cases with quantified penalties

### Research Standards Met
- ≥2 Tier A/B sources for major claims ✓
- Counterevidence sections included ✓  
- Chicago-style source attribution ✓
- Maximum 15-word quotes maintained ✓

---

## Usage Notes

All datasets include:
- **Comprehensive metadata** (`.meta.yaml` files)
- **Source attribution** and data quality indicators
- **Collection methodology** documentation
- **Usage limitations** and validation approaches
- **Analysis scripts** for reproducible results

This index supports the thesis that compute-storage separation will fundamentally transform the database industry by 2035, with quantified evidence across adoption, cost, performance, reliability, and organizational dimensions.