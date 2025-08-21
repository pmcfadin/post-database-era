# Scripts Directory

This directory contains reusable scripts for data collection and analysis related to database and lakehouse research.

## Directory Structure

### `/data-collection/`
Scripts for gathering data from various sources:

**Core Data Collectors:**
- `collect_api_coverage_data.py` - API coverage and feature parity analysis
- `collect_catalog_governance_costs.py` - Data catalog and governance pricing
- `collect_compute_cost_data.py` - Compute cost analysis across platforms
- `collect_data_movement_costs.py` - Cross-cloud data movement costs
- `collect_external_table_costs.py` - External table query costs
- `collect_gateway_terms.py` - Gateway terminology and industry discourse
- `collect_incident_signals.py` - Database incident and reliability data
- `collect_lakehouse_sku_data.py` - Lakehouse product SKU availability
- `collect_performance_benchmarks.py` - Query performance benchmarks
- `collect_realworld_egress_data.py` - Real-world egress cost case studies
- `collect_stackoverflow_data.py` - StackOverflow trends and discussions
- `collect_storage_pricing.py` - Object storage vs warehouse storage costs

**Enhanced Collectors:**
- `enhanced_cost_research.py` - Advanced cost analysis with multiple sources
- `enhanced_performance_collector.py` - Comprehensive performance data collection
- `enhanced_sku_research.py` - Extended SKU and product research
- `enhanced_storage_pricing.py` - Advanced storage cost analysis

**Utility Collectors:**
- `github_discussions_search.py` - GitHub repository and discussion analysis
- `stackoverflow_trends.py` - StackOverflow tag and trend analysis
- `time_to_first_query_benchmark.py` - Developer onboarding time analysis
- `wayback_historical_analysis.py` - Historical pricing and feature analysis

### `/analysis/`
Scripts for analyzing collected data:

**Cost Analysis:**
- `analyze_catalog_governance_costs.py` - Governance and catalog cost breakdown
- `analyze_data_movement_tax.py` - Data egress and movement cost analysis
- `analyze_storage_costs.py` - Storage cost comparison and trends
- `compute_cost_analysis.py` - Compute cost efficiency analysis
- `workload_cost_analysis.py` - Workload-specific cost patterns

**Market Analysis:**
- `analyze_lakehouse_sku_landscape.py` - Lakehouse product market analysis
- `analyze_substrate_patterns.py` - Query substrate adoption patterns
- `analyze_table_format_penetration.py` - Table format market penetration

**Performance Analysis:**
- `analyze_performance_data.py` - Query performance and latency analysis
- `gateway_analysis.py` - Gateway performance and adoption analysis

**Operations Analysis:**
- `ops_cost_analysis_summary.py` - Operational cost and FTE analysis

## Usage Notes

- Scripts are designed to be run from the project root directory
- Most scripts output CSV files with accompanying metadata (`.meta.yaml`) files
- Data files follow the naming convention: `YYYY-MM-DD__data__category__source__description.csv`
- Analysis scripts often generate JSON summary files and markdown reports

## Dependencies

Common dependencies across scripts:
- `requests` - HTTP requests for API calls
- `csv` - CSV file handling
- `json` - JSON data processing
- `pandas` - Data analysis (where needed)
- `selenium` - Web scraping (specific scripts)
- `pyyaml` - YAML metadata files

## Data Quality

All data collection scripts include:
- Source attribution and URLs
- Data quality indicators
- Collection methodology documentation
- Error handling and retry logic
- Comprehensive metadata generation