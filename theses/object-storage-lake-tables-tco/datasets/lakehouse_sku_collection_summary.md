# Lakehouse SKU Availability Data Collection Summary

## Dataset Overview
Successfully collected comprehensive data on managed "lakehouse SKU" availability across major cloud vendors and regions.

## Files Created
- **CSV Data**: `2025-08-21__data__lakehouse-sku-availability__multi-vendor__product-catalog.csv`
- **Metadata**: `2025-08-21__data__lakehouse-sku-availability__multi-vendor__product-catalog.meta.yaml`
- **Analysis**: `2025-08-21__analysis__lakehouse-sku-landscape__market-insights.json`

## Key Findings

### Market Coverage
- **Total Active SKUs**: 38 lakehouse offerings
- **Vendors Tracked**: 7 major providers
- **Cloud Platforms**: AWS (19 SKUs), Azure (10 SKUs), GCP (9 SKUs)
- **Market Age**: 10 years (since Google Dataproc in 2015)

### Market Leaders by SKU Count
1. **AWS**: 8 SKUs (Lake Formation, Athena, EMR Studio, Redshift Spectrum)
2. **Databricks**: 7 SKUs (Lakehouse Platform across 3 clouds)
3. **Google**: 7 SKUs (BigLake, BigQuery External Tables, Dataproc)
4. **Snowflake**: 6 SKUs (External Tables, Iceberg Tables)
5. **Microsoft**: 6 SKUs (Synapse Analytics, Fabric OneLake)
6. **Dremio**: 2 SKUs (Multi-cloud lakehouse platform)
7. **Starburst**: 2 SKUs (Galaxy platform)

### Timeline Insights
- **Early Pioneers** (2015-2017): Google Dataproc, AWS Athena, BigQuery External Tables
- **Market Expansion** (2019-2021): Lake Formation, Snowflake External Tables, Databricks Lakehouse Platform
- **Recent Innovation** (2023-2024): 8 new SKUs, including Snowflake Iceberg Tables and Microsoft Fabric OneLake

### Regional Patterns
- **Primary Regions**: us-east-1 (9 offerings), East US (6 offerings), us-central1 (5 offerings)
- **Multi-cloud Vendors**: Databricks and Snowflake lead with presence across all 3 major clouds
- **Cloud-specific Focus**: AWS, Google, and Microsoft primarily focus on their own cloud platforms

### Product Categories
- **Native Lakehouse Platforms**: Databricks, Dremio, Starburst
- **External Table Integration**: Snowflake, BigQuery, Redshift Spectrum
- **Data Lake Management**: AWS Lake Formation, Google BigLake
- **Analytics Platforms**: Azure Synapse, AWS EMR Studio
- **Next-gen Unified**: Microsoft Fabric OneLake

## Data Quality
- **Completeness**: 100% coverage for major vendors and primary regions
- **Sources**: Vendor pricing pages, product announcements, GA press releases
- **Credibility**: Tier A (official vendor sources)
- **Update Frequency**: Quarterly updates recommended for market dynamics

## Usage Notes
- `lakehouse_sku=1` indicates first-class lakehouse capabilities available
- `lakehouse_sku=0` indicates deprecated services (1 case: Microsoft Data Lake Analytics)
- GA dates represent general availability, may vary by specific features
- Regional coverage focuses on major cloud regions, not exhaustive global coverage