# Compute-Storage Separation Cost and TCO Data Collection Summary

## Overview
This collection provides comprehensive cost and performance data for analyzing the TCO implications of compute-storage separation in database architectures. The data spans three key focus areas:

1. **Workload Cost Curves** - Performance and cost comparisons between local NVMe vs disaggregated storage
2. **Elasticity Savings** - Cost optimization through independent compute-storage scaling
3. **Data Movement Costs** - Transfer pricing and egress costs in disaggregated architectures

## Key Datasets Collected

### 1. Storage Architecture Performance Comparison
**File:** `2025-08-20__data__storage-separation__performance-cost__nvme-vs-disaggregated.csv`
- **Records:** 10 storage configurations
- **Key Metrics:** IOPS, latency, throughput, cost per TB/hour
- **Key Finding:** Local NVMe provides 10-100x better IOPS but higher cost per TB

### 2. Elasticity Savings Analysis
**File:** `2025-08-20__data__elasticity-savings__scaling-models__cost-optimization.csv`
- **Records:** 8 scaling scenarios
- **Key Metrics:** Monthly costs, utilization rates, cost savings
- **Key Finding:** Disaggregated scaling provides 16-58% cost savings vs monolithic

### 3. TCO Workload Scaling Curves
**File:** `2025-08-20__data__tco-curves__workload-scaling__cost-per-tb.csv`
- **Records:** 7 workload sizes (0.5TB to 1PB)
- **Key Metrics:** Cost per TB, operational costs, total TCO
- **Key Finding:** Scale economies favor disaggregated storage at 10TB+

### 4. TPC Benchmark Performance
**File:** `2025-08-20__data__tpc-benchmarks__storage-comparison__performance-cost.csv`
- **Records:** 7 benchmark configurations
- **Key Metrics:** TPC-C/TPC-H performance, cost per operation
- **Key Finding:** Local NVMe provides 2-3x better TPC-C performance due to latency sensitivity

### 5. YCSB NoSQL Benchmarks
**File:** `2025-08-20__data__ycsb-benchmarks__storage-comparison__nosql-performance.csv`
- **Records:** 6 NoSQL configurations
- **Key Metrics:** Operations/sec, latency, cost per million operations
- **Key Finding:** 50-60% better latency for write-heavy workloads on local storage

### 6. Real-World Production Case Studies
**File:** `2025-08-20__data__real-world-performance__case-studies__production-metrics.csv`
- **Records:** 8 production deployments (Netflix, Uber, Airbnb, etc.)
- **Key Metrics:** QPS, latency, availability, monthly costs
- **Key Finding:** Mission-critical OLTP consistently chooses local storage for predictable latency

### 7. Data Movement Tax Analysis
**File:** `2025-08-20__data__data-movement-tax__multi-cloud__transfer-pricing.csv`
- **Records:** 27 transfer pricing scenarios
- **Key Metrics:** Cost per GB, egress pricing across cloud providers
- **Key Finding:** Internet egress costs $0.08-$0.12/GB, significant at petabyte scale

### 8. Compute Cost Analysis
**Files:** Enhanced compute cost data from existing collection
- **Records:** 29 total compute cost records across multiple engines
- **Key Metrics:** Cost per TB scanned, pricing models
- **Key Finding:** Open source engines average $1.13/TB vs $4.59/TB for cloud managed

## Summary of Key Insights

### Storage Performance vs Cost
| Storage Type | IOPS/TB | P99 Latency (ms) | Cost/TB/Hour | Best For |
|--------------|---------|------------------|--------------|----------|
| Local NVMe | 500K | 0.1-3.0 | $156-$312 | Latency-sensitive OLTP |
| EBS gp3 | 16K | 1.2-1.5 | $248 | Balanced workloads |
| Aurora Storage | 200K | 2.0 | $102 | Cloud-native OLTP |
| S3 Standard | 5.5K | 15-25 | $23-$408 | Analytics, batch processing |

### Elasticity Savings Summary
| Scaling Model | Monthly Cost | Savings vs Monolithic |
|---------------|--------------|----------------------|
| Traditional Monolithic | $43,200 | 0% (baseline) |
| Snowflake Disaggregated | $36,000 | 16.7% |
| BigQuery Serverless | $29,250 | 32.3% |
| Aurora Serverless v2 | $21,600 | 50.0% |
| PlanetScale Serverless | $18,000 | 58.3% |

### TCO Scale Economics
| Workload Size | Local NVMe $/TB | Disaggregated $/TB | Savings |
|---------------|----------------|-------------------|---------|
| 0.5TB | $1,290 | $514 | 60.2% |
| 10TB | $525 | $248 | 52.8% |
| 100TB | $535 | $189 | 64.7% |
| 1PB | N/A (not viable) | $315 | Only option |

### Performance per Dollar Analysis
| Engine | Storage | Performance Metric | Performance/$ |
|--------|---------|-------------------|---------------|
| ClickHouse | Local NVMe | 2,800 queries/hour | 4.76 queries/$/hour |
| Trino | S3 | 1,850 queries/hour | 5.56 queries/$/hour |
| PostgreSQL | Local NVMe | 125K tpmC | 312.5 tpmC/$/hour |
| Aurora | Cloud Storage | 98K tpmC | 196.1 tpmC/$/hour |

## Data Quality and Limitations

### Strengths
- **Comprehensive Coverage:** All major storage architectures and cloud providers
- **Multiple Benchmarks:** TPC-C, TPC-H, YCSB, and real-world case studies
- **Real Production Data:** Case studies from Netflix, Uber, Airbnb, Stripe
- **Complete Metadata:** All datasets include detailed metadata with source attribution

### Limitations
- Cost estimates based on list pricing (enterprise discounts not reflected)
- Performance metrics represent specific configurations and may vary
- Operational costs vary significantly by organization
- Migration and training costs not included in TCO analysis

## Recommendations for Further Analysis

1. **Cost Optimization Opportunities**
   - Hybrid architectures combining local and disaggregated storage
   - Workload-specific storage tier selection
   - Auto-tiering based on access patterns

2. **Performance Optimization**
   - Caching strategies to bridge latency gaps
   - Workload routing between storage tiers
   - Predictive scaling based on usage patterns

3. **Risk Assessment**
   - Data movement tax impact on multi-cloud strategies
   - Vendor lock-in considerations for proprietary storage formats
   - Operational complexity of managing multiple storage tiers

## Usage Guidelines

All datasets follow the naming convention:
```
YYYY-MM-DD__data__<category>__<source>__<description>.csv
```

Each CSV file has an accompanying `.meta.yaml` file with:
- Complete column descriptions
- Data quality indicators
- Source attribution
- Usage limitations

The data supports research into:
- Database architecture cost modeling
- Storage tier optimization strategies
- Cloud migration TCO analysis
- Performance-cost trade-off analysis
- Workload placement optimization