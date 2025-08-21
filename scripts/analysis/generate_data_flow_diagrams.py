#!/usr/bin/env python3
"""
Data Flow Diagram Generator
Creates ASCII art diagrams showing data movement and interoperability patterns.
"""

import os
from datetime import datetime

def generate_etl_elt_diagram():
    """Generate ETL vs ELT flow diagram"""
    return """
# ETL vs ELT Data Flow Patterns

## Traditional ETL Pattern (65% adoption)
```
[Source DB] ──→ [ETL Engine] ──→ [Data Warehouse]
     │               │                   │
     │         [Transform]         [Query Engine]
     │         [Validate]               │
     │         [Clean]                  ▼
     └────── Hours-Days ──────→ [Analytics/BI]

Cost Model: Dedicated Compute + Storage
Latency: Hours to Days
```

## Modern ELT Pattern (45% adoption)  
```
[Source DB] ──→ [Data Lake] ──→ [Query Engine] ──→ [Analytics]
     │              │              │                   │
     │        [Raw Storage]   [Transform]              │
     │        [Staging]       [On-demand]              │
     └────── Minutes-Hours ────────────────────────────┘

Cost Model: Storage + Query Compute
Latency: Minutes to Hours
```

## Real-time Streaming (30% adoption)
```
[Source] ──→ [Stream Processor] ──→ [Target Systems]
    │              │                       │
    │        [Real-time]               [Live Data]
    │        [Transform]               [Events]
    └────── Milliseconds-Seconds ─────────┘

Cost Model: Continuous Compute
Latency: Sub-second
```
"""

def generate_hybrid_storage_diagram():
    """Generate hybrid storage tiering diagram"""
    return """
# Hybrid Storage Architecture Patterns

## Hot-Warm-Cold Tiering (Snowflake/Databricks Pattern)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Hot Tier  │    │  Warm Tier  │    │  Cold Tier  │
│             │    │             │    │             │
│  Local NVMe │◄──►│ Network SSD │◄──►│ Object Store│
│    SSD      │    │             │    │    (S3)     │
│             │    │             │    │             │
│ 5-10% data  │    │ 20-30% data │    │ 60-70% data │
│ 85-95% hit  │    │ 70-85% hit  │    │ Archival    │
│ 10-50x perf │    │ 2-10x perf  │    │ 60-80% cost│
│             │    │             │    │ reduction   │
└─────────────┘    └─────────────┘    └─────────────┘
       ▲                  ▲                  ▲
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                   [Query Engine]
                   [Cache Manager]
                   [Access Predictor]
```

## Intelligent Caching Strategy
```
[Query Request] ──→ [Cache Check] ──→ [Local SSD] ──→ [Results]
       │                 │              ▲
       │                 ▼              │
       │          [Cache Miss]          │
       │                 │              │
       │                 ▼              │
       └──→ [Object Storage] ───────────┘
              [Background Cache]
              [ML Access Prediction]

Performance: 100-1000x improvement for cached data
Cost: 80-90% reduction vs in-memory
```
"""

def generate_query_federation_diagram():
    """Generate query federation vs replication diagram"""
    return """
# Query Engine Federation Patterns

## Federated Query Architecture (Trino Pattern)
```
┌─────────────────────────────────────────────────────────┐
│                 Trino Coordinator                       │
└─────────────────────┬───────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌─────────┐    ┌─────────────┐    ┌─────────────┐
│PostgreSQL│    │    Hive     │    │    S3       │
│Connector │    │  Connector  │    │ Connector   │
└─────────┘    └─────────────┘    └─────────────┘
    │                 │                 │
    ▼                 ▼                 ▼
[RDBMS Data]    [Warehouse Data]   [Lake Data]

Query Latency: Higher (network dependent)
Storage Cost: Lower (no duplication) 
Network Cost: Higher (data movement per query)
Best For: Occasional cross-source queries
```

## Data Replication Architecture
```
┌─────────────┐    ┌─────────────────────────────────┐
│   Sources   │    │        Target System            │
│             │    │                                 │
│ PostgreSQL  │───►│  ┌─────────┐  ┌─────────────┐  │
│    Hive     │───►│  │Replicated│  │    Query    │  │
│     S3      │───►│  │  Data    │  │   Engine    │  │
│             │    │  └─────────┘  └─────────────┘  │
└─────────────┘    └─────────────────────────────────┘

Query Latency: Lower (local access)
Storage Cost: Higher (data duplication)
Network Cost: Lower (one-time movement)
Best For: Frequent cross-source analytics
```

## Hybrid Approach (Cache + Federation)
```
[Query] ──→ [Cache Check] ──→ [Local Results]
   │             │
   │         [Cache Miss]
   │             │
   │             ▼
   └──→ [Federation Query] ──→ [Remote Sources]
              │
              ▼
        [Cache Update]
        [ML Prediction]

Latency: Variable (cache hit dependent)
Cost: Medium (selective caching)
Complexity: Higher (cache management)
Best For: Mixed query patterns
```
"""

def generate_cdc_patterns_diagram():
    """Generate CDC pattern diagram"""
    return """
# Change Data Capture Patterns

## Log-based CDC (40% adoption)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Source    │    │     CDC     │    │   Target    │
│  Database   │    │    Agent    │    │   Systems   │
│             │    │             │    │             │
│ Transaction │───►│  Log Reader │───►│ Data Lake   │
│    Log      │    │  Parser     │    │ Warehouse   │
│             │    │  Filter     │    │ Analytics   │
└─────────────┘    └─────────────┘    └─────────────┘

Latency: Sub-second
Volume: Transaction log size
Cost: Agent + Network
Use Case: Real-time replication
```

## Trigger-based CDC (25% adoption)
```
┌─────────────────────────────────────────────────────────┐
│                Source Database                          │
│                                                         │
│  [Table] ──→ [Trigger] ──→ [Change Table] ──→ [Export] │
│                │                                        │
│         [Insert/Update/Delete]                          │
│                │                                        │
│                ▼                                        │
│         [Log Changes]                                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                   [Target Systems]

Latency: Seconds to minutes  
Volume: Changed records only
Cost: Database overhead
Use Case: Legacy integration
```
"""

def save_diagrams():
    """Save all diagrams to markdown files"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    base_dir = "/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets"
    
    # Combine all diagrams
    full_content = f"""# Data Movement and Interoperability Flow Diagrams

Generated: {timestamp}

{generate_etl_elt_diagram()}

{generate_hybrid_storage_diagram()}

{generate_query_federation_diagram()}

{generate_cdc_patterns_diagram()}

## Summary

These diagrams illustrate the key architectural patterns discovered in our data movement and interoperability research:

1. **Pipeline Evolution**: ETL remains dominant but ELT is growing for lakehouse architectures
2. **Storage Optimization**: Multi-tier caching provides significant cost and performance benefits
3. **Query Federation**: Trade-offs between federation and replication depend on access patterns
4. **Real-time Integration**: CDC patterns enable sub-second data movement for real-time use cases

The diagrams show how compute-storage separation enables these flexible architectures while maintaining performance through intelligent caching and optimization strategies.
"""
    
    diagram_path = os.path.join(base_dir, f"{timestamp}__diagrams__data-movement-patterns.md")
    with open(diagram_path, 'w', encoding='utf-8') as mdfile:
        mdfile.write(full_content)
    
    return diagram_path

def main():
    """Main execution function"""
    print("Generating data flow diagrams...")
    
    diagram_path = save_diagrams()
    
    print(f"✓ Data flow diagrams saved to: {diagram_path}")
    print("✓ Includes ETL/ELT, hybrid storage, federation, and CDC patterns")

if __name__ == "__main__":
    main()