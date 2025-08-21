# Manual Screenshot Collection Guide

Since automated screenshot collection requires specific browser setup, here's a manual guide for capturing marketplace tile screenshots.

## Key Screenshots Needed

### 1. Multi-API Database Tiles

#### MongoDB Atlas (Multi-API: Document + Search + Vector)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-njr3dt7flfxjo
- **GCP**: https://console.cloud.google.com/marketplace/product/mongodb-atlas-operator
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/mongodb.mongodb_atlas

#### Redis Enterprise (Multi-API: Key-Value + Search + Time-Series + Vector)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-mzwj2nqqhg2iy
- **GCP**: https://console.cloud.google.com/marketplace/product/redis-marketplace
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/redislabs.redis_enterprise_cache

#### DataStax Astra DB (Multi-API: NoSQL + Vector + Search)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-oqy3c5c7pkfds
- **GCP**: https://console.cloud.google.com/marketplace/product/datastax-public
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/datastax.astra-db

#### Couchbase Cloud (Multi-API: Document + Key-Value + Search + Analytics)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-jnsb5y4qkuzxe
- **GCP**: https://console.cloud.google.com/marketplace/product/couchbase-marketplace
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/couchbase.couchbase-capella

### 2. Single-API Database Tiles (for comparison)

#### Neo4j AuraDB (Single-API: Graph)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-akmxo4mwj5lii
- **GCP**: https://console.cloud.google.com/marketplace/product/neo4j-aura-aura-gcp
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/neo4j.neo4j-aura-azure

#### InfluxDB Cloud (Single-API: Time-Series)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-ykcdvuqp5gybw
- **Azure**: https://azuremarketplace.microsoft.com/marketplace/apps/influxdata.influxdb-cloud

#### Pinecone (Single-API: Vector)
- **AWS**: https://aws.amazon.com/marketplace/pp/prodview-peyajmjh7mmje

## Screenshot Specifications

### What to Capture
1. **Tile Overview**: Full marketplace tile showing service name, vendor, description
2. **Category Positioning**: How the service is categorized in marketplace taxonomy
3. **Feature Highlights**: Key capabilities and API types mentioned
4. **Pricing Tier Indication**: Whether positioned as enterprise/professional/starter

### Technical Requirements
- **Resolution**: 1920x1080 minimum
- **Format**: PNG preferred
- **Crop**: Focus on the database service tile, remove unnecessary marketplace chrome
- **Naming**: `YYYYMMDD_[marketplace]_[vendor]_[positioning].png`

### Key Analysis Points
1. **Multi-API Emphasis**: How prominently are multiple API types featured?
2. **Primary vs Secondary APIs**: Which APIs are highlighted as primary capabilities?
3. **Use Case Positioning**: Enterprise platform vs specialized tool?
4. **Visual Hierarchy**: How is multi-model capability communicated?

## Example Analysis

### MongoDB Atlas Tile Analysis
- **Primary Positioning**: "Document database" (legacy single-API framing)
- **Secondary Features**: Search, analytics, mobile sync prominently featured
- **Multi-API Evidence**: Vector search now prominently displayed
- **Evolution**: From document-centric to "developer data platform"

### Redis Enterprise Tile Analysis  
- **Primary Positioning**: "In-memory database" maintained
- **Secondary Features**: Search, JSON, time-series prominently featured
- **Multi-API Evidence**: Clear modules/capabilities breakdown
- **Evolution**: From cache to "real-time data platform"

## Collection Process

1. Visit each URL in a clean browser session
2. Wait for full page load
3. Capture full tile (vendor info + description + features)
4. Save with descriptive filename
5. Document positioning observations in notes
6. Compare across marketplaces for same vendor
7. Track changes over time with dated captures

## Historical Comparison

For historical analysis, use Wayback Machine:
- https://web.archive.org/
- Search for marketplace URLs from 2020, 2021, 2022, 2023
- Compare tile messaging evolution
- Document transition from single-API to multi-API positioning