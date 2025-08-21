#!/usr/bin/env python3
"""
Lakehouse SKU Landscape Analysis
Analyzes patterns in lakehouse SKU availability and market timing
"""

import pandas as pd
import json
from datetime import datetime
from collections import Counter

def analyze_lakehouse_landscape():
    """Perform comprehensive analysis of lakehouse SKU data"""
    
    # Load the data
    df = pd.read_csv('2025-08-21__data__lakehouse-sku-availability__multi-vendor__product-catalog.csv')
    
    # Convert ga_date to datetime
    df['ga_date'] = pd.to_datetime(df['ga_date'])
    df['ga_year'] = df['ga_date'].dt.year
    
    analysis_results = {}
    
    # 1. Vendor Coverage Analysis
    vendor_coverage = df.groupby('vendor').agg({
        'lakehouse_sku': 'sum',
        'product': 'nunique',
        'cloud': 'nunique',
        'region': 'nunique'
    }).rename(columns={
        'lakehouse_sku': 'active_skus',
        'product': 'distinct_products', 
        'cloud': 'cloud_coverage',
        'region': 'region_coverage'
    })
    
    analysis_results['vendor_coverage'] = vendor_coverage.to_dict('index')
    
    # 2. Timeline Analysis - When did lakehouse SKUs emerge?
    timeline_analysis = df[df['lakehouse_sku'] == 1].groupby('ga_year').agg({
        'vendor': 'nunique',
        'product': 'count'
    }).rename(columns={
        'vendor': 'new_vendors',
        'product': 'new_skus'
    })
    
    analysis_results['ga_timeline'] = timeline_analysis.to_dict('index')
    
    # 3. Cloud Platform Analysis
    cloud_analysis = df.groupby('cloud').agg({
        'lakehouse_sku': 'sum',
        'vendor': 'nunique',
        'product': 'nunique'
    }).rename(columns={
        'lakehouse_sku': 'total_skus',
        'vendor': 'vendor_count',
        'product': 'product_count'
    })
    
    analysis_results['cloud_platform_analysis'] = cloud_analysis.to_dict('index')
    
    # 4. Market Entry Timing
    first_movers = df[df['lakehouse_sku'] == 1].groupby('vendor')['ga_date'].min().sort_values()
    analysis_results['market_entry_order'] = {
        vendor: date.strftime('%Y-%m-%d') for vendor, date in first_movers.items()
    }
    
    # 5. Product Category Analysis
    product_categories = {
        'Native Lakehouse': ['Lakehouse Platform', 'Galaxy'],
        'External Table Integration': ['External Tables', 'BigQuery External Tables', 'Redshift Spectrum'],
        'Table Format Support': ['Iceberg Tables'],
        'Query Engine': ['Athena', 'Dataproc'],
        'Data Lake Management': ['Lake Formation', 'BigLake'],
        'Analytics Platform': ['Synapse Analytics', 'EMR Studio'],
        'Next-Gen Platform': ['Fabric OneLake']
    }
    
    category_analysis = {}
    for category, products in product_categories.items():
        category_df = df[df['product'].isin(products)]
        category_analysis[category] = {
            'total_skus': int(category_df['lakehouse_sku'].sum()),
            'vendor_count': category_df['vendor'].nunique(),
            'avg_ga_year': float(category_df[category_df['lakehouse_sku'] == 1]['ga_year'].mean())
        }
    
    analysis_results['product_category_analysis'] = category_analysis
    
    # 6. Regional Coverage Patterns
    region_patterns = df.groupby('region').agg({
        'lakehouse_sku': 'sum',
        'vendor': 'nunique'
    }).rename(columns={
        'lakehouse_sku': 'total_offerings',
        'vendor': 'vendor_count'
    }).sort_values('total_offerings', ascending=False)
    
    analysis_results['regional_coverage'] = region_patterns.to_dict('index')
    
    # 7. Market Maturity Indicators
    current_year = 2025
    market_maturity = {
        'total_active_skus': int(df['lakehouse_sku'].sum()),
        'total_vendors': df['vendor'].nunique(),
        'total_products': df['product'].nunique(),
        'market_age_years': current_year - df[df['lakehouse_sku'] == 1]['ga_year'].min(),
        'recent_launches_2023_2024': int(df[(df['ga_year'] >= 2023) & (df['lakehouse_sku'] == 1)].shape[0]),
        'deprecated_services': int(df[df['lakehouse_sku'] == 0].shape[0])
    }
    
    analysis_results['market_maturity'] = market_maturity
    
    # 8. Competitive Insights
    competitive_insights = {
        'multi_cloud_vendors': df[df['lakehouse_sku'] == 1].groupby('vendor')['cloud'].nunique().to_dict(),
        'cross_vendor_products': df.groupby('cloud')['vendor'].nunique().to_dict(),
        'market_leaders_by_sku_count': df[df['lakehouse_sku'] == 1].groupby('vendor').size().sort_values(ascending=False).to_dict()
    }
    
    analysis_results['competitive_landscape'] = competitive_insights
    
    return analysis_results

def save_analysis_results():
    """Save analysis results to JSON file"""
    results = analyze_lakehouse_landscape()
    
    filename = "2025-08-21__analysis__lakehouse-sku-landscape__market-insights.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"Analysis saved to {filename}")
    return results

if __name__ == "__main__":
    results = save_analysis_results()
    
    # Print key insights
    print("\n=== LAKEHOUSE SKU LANDSCAPE INSIGHTS ===")
    print(f"Total Active SKUs: {results['market_maturity']['total_active_skus']}")
    print(f"Market Age: {results['market_maturity']['market_age_years']} years")
    print(f"Recent Launches (2023-2024): {results['market_maturity']['recent_launches_2023_2024']}")
    
    print("\n=== MARKET LEADERS BY SKU COUNT ===")
    for vendor, count in results['competitive_landscape']['market_leaders_by_sku_count'].items():
        print(f"{vendor}: {count} SKUs")
    
    print("\n=== CLOUD PLATFORM COVERAGE ===")
    for cloud, metrics in results['cloud_platform_analysis'].items():
        print(f"{cloud}: {metrics['total_skus']} SKUs, {metrics['vendor_count']} vendors")