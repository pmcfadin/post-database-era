#!/usr/bin/env python3
"""
API Coverage Analysis Script
Analyzes the collected API coverage data to identify convergence patterns and gaps
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import json

def load_data():
    """Load the API coverage data"""
    df = pd.read_csv('2025-08-20__data__api-coverage-parity__multi-vendor__feature-matrix.csv')
    return df

def analyze_vendor_coverage(df):
    """Analyze API coverage by vendor"""
    print("=== VENDOR API COVERAGE ANALYSIS ===\n")
    
    # Coverage by vendor and paradigm
    paradigms = ['SQL', 'KV', 'Document', 'Graph', 'Search']
    
    vendor_coverage = {}
    for vendor in df['vendor'].unique():
        vendor_data = df[df['vendor'] == vendor]
        coverage = {}
        
        for paradigm in paradigms:
            paradigm_apis = vendor_data[vendor_data['api'].str.contains(paradigm, na=False)]
            total_features = len(paradigm_apis)
            ga_features = len(paradigm_apis[paradigm_apis['status'] == 'GA'])
            preview_features = len(paradigm_apis[paradigm_apis['status'] == 'Preview'])
            
            if total_features > 0:
                coverage[paradigm] = {
                    'total': total_features,
                    'ga': ga_features,
                    'preview': preview_features,
                    'ga_percentage': (ga_features / total_features) * 100
                }
            else:
                coverage[paradigm] = {
                    'total': 0,
                    'ga': 0,
                    'preview': 0,
                    'ga_percentage': 0
                }
        
        vendor_coverage[vendor] = coverage
    
    # Print coverage matrix
    print("API Paradigm Coverage by Vendor:")
    print("=" * 80)
    header = f"{'Vendor':<12} {'SQL':<10} {'KV':<10} {'Document':<12} {'Graph':<10} {'Search':<10}"
    print(header)
    print("=" * 80)
    
    for vendor, coverage in vendor_coverage.items():
        row = f"{vendor:<12}"
        for paradigm in paradigms:
            if coverage[paradigm]['total'] > 0:
                ga_pct = coverage[paradigm]['ga_percentage']
                ga_count = coverage[paradigm]['ga']
                total_count = coverage[paradigm]['total']
                row += f" {ga_count}/{total_count}({ga_pct:.0f}%)"[:10].ljust(10)
            else:
                row += f" {'N/A':<10}"
        print(row)
    
    return vendor_coverage

def analyze_feature_parity(df):
    """Analyze feature parity across vendors"""
    print("\n=== FEATURE PARITY ANALYSIS ===\n")
    
    # Core features that should be available across paradigms
    core_features = [
        'CRUD', 'Index', 'Pagination', 'Transaction', 'Search'
    ]
    
    feature_patterns = {
        'CRUD': ['GET', 'PUT', 'DELETE', 'SELECT', 'INSERT', 'UPDATE', 'find', 'create', 'update', 'delete'],
        'Index': ['Index', 'Secondary', 'B-Tree', 'Composite'],
        'Pagination': ['Pagination', 'Cursor', 'Token', 'LIMIT', 'OFFSET'],
        'Transaction': ['ACID', 'Transaction'],
        'Search': ['Search', 'Full-Text', 'Vector']
    }
    
    # Analyze feature availability by category
    feature_analysis = {}
    
    for category, patterns in feature_patterns.items():
        category_features = df[df['feature'].str.contains('|'.join(patterns), case=False, na=False)]
        
        vendors_with_feature = category_features['vendor'].unique()
        ga_implementations = category_features[category_features['status'] == 'GA']
        preview_implementations = category_features[category_features['status'] == 'Preview']
        
        feature_analysis[category] = {
            'total_implementations': len(category_features),
            'vendors_with_feature': len(vendors_with_feature),
            'ga_implementations': len(ga_implementations),
            'preview_implementations': len(preview_implementations),
            'vendor_list': list(vendors_with_feature)
        }
    
    print("Feature Category Adoption:")
    print("=" * 60)
    for category, analysis in feature_analysis.items():
        print(f"{category}:")
        print(f"  Total implementations: {analysis['total_implementations']}")
        print(f"  Vendors offering: {analysis['vendors_with_feature']}/6")
        print(f"  GA status: {analysis['ga_implementations']}")
        print(f"  Preview status: {analysis['preview_implementations']}")
        print(f"  Vendors: {', '.join(analysis['vendor_list'])}")
        print()
    
    return feature_analysis

def analyze_convergence_trends(df):
    """Analyze API convergence trends over time"""
    print("\n=== CONVERGENCE TRENDS ANALYSIS ===\n")
    
    # Convert added_date to datetime
    df['added_date'] = pd.to_datetime(df['added_date'], errors='coerce')
    df['year'] = df['added_date'].dt.year
    
    # Filter out rows without dates (NA features)
    dated_features = df.dropna(subset=['added_date'])
    
    # Analyze multi-API platforms vs single-API
    multi_api_vendors = []
    for vendor in df['vendor'].unique():
        vendor_data = df[df['vendor'] == vendor]
        api_types = set()
        for api in vendor_data['api'].unique():
            if '-SQL' in api:
                api_types.add('SQL')
            if '-KV' in api:
                api_types.add('KV')
            if '-Document' in api:
                api_types.add('Document')
            if '-Graph' in api:
                api_types.add('Graph')
            if '-Search' in api:
                api_types.add('Search')
        
        if len(api_types) >= 3:
            multi_api_vendors.append(vendor)
    
    print("Multi-API Platform Analysis:")
    print("=" * 40)
    print(f"Vendors with 3+ API paradigms: {', '.join(multi_api_vendors)}")
    print(f"Proportion: {len(multi_api_vendors)}/6 ({len(multi_api_vendors)/6*100:.1f}%)")
    
    # Timeline analysis
    if len(dated_features) > 0:
        timeline = dated_features.groupby(['year', 'vendor']).size().reset_index(name='features_added')
        
        print(f"\nFeature Introduction Timeline:")
        print("=" * 40)
        year_summary = dated_features.groupby('year').agg({
            'feature': 'count',
            'vendor': 'nunique'
        }).rename(columns={'feature': 'total_features', 'vendor': 'active_vendors'})
        
        for year, data in year_summary.iterrows():
            if not pd.isna(year):
                print(f"{int(year)}: {data['total_features']} features, {data['active_vendors']} vendors active")

def analyze_cross_api_gaps(df):
    """Identify gaps in cross-API capabilities"""
    print("\n=== CROSS-API CAPABILITY GAPS ===\n")
    
    # Look for NA status features that indicate missing cross-API support
    na_features = df[df['status'] == 'NA']
    
    gap_analysis = {}
    for vendor in df['vendor'].unique():
        vendor_gaps = na_features[na_features['vendor'] == vendor]
        gap_patterns = defaultdict(list)
        
        for _, row in vendor_gaps.iterrows():
            api_type = row['api'].split('-')[1] if '-' in row['api'] else 'Unknown'
            gap_patterns[api_type].append(row['feature'])
        
        gap_analysis[vendor] = dict(gap_patterns)
    
    print("Missing Cross-API Capabilities by Vendor:")
    print("=" * 50)
    for vendor, gaps in gap_analysis.items():
        if gaps:
            print(f"\n{vendor}:")
            for api_type, features in gaps.items():
                if features:
                    print(f"  {api_type}: {', '.join(features[:3])}{'...' if len(features) > 3 else ''}")
        else:
            print(f"\n{vendor}: No major gaps identified")

def generate_summary_insights(df):
    """Generate key insights summary"""
    print("\n=== KEY INSIGHTS SUMMARY ===\n")
    
    total_features = len(df)
    ga_features = len(df[df['status'] == 'GA'])
    preview_features = len(df[df['status'] == 'Preview'])
    na_features = len(df[df['status'] == 'NA'])
    
    print(f"Dataset Overview:")
    print(f"- Total feature points analyzed: {total_features}")
    print(f"- Generally Available: {ga_features} ({ga_features/total_features*100:.1f}%)")
    print(f"- Preview/Beta: {preview_features} ({preview_features/total_features*100:.1f}%)")
    print(f"- Not Available: {na_features} ({na_features/total_features*100:.1f}%)")
    
    # Vendor maturity analysis
    vendor_maturity = {}
    for vendor in df['vendor'].unique():
        vendor_data = df[df['vendor'] == vendor]
        ga_ratio = len(vendor_data[vendor_data['status'] == 'GA']) / len(vendor_data)
        vendor_maturity[vendor] = ga_ratio
    
    most_mature = max(vendor_maturity, key=vendor_maturity.get)
    print(f"\nVendor Maturity (by GA feature ratio):")
    for vendor, ratio in sorted(vendor_maturity.items(), key=lambda x: x[1], reverse=True):
        print(f"- {vendor}: {ratio*100:.1f}% GA features")
    
    # API paradigm analysis
    api_paradigm_counts = defaultdict(int)
    for api in df['api'].unique():
        if '-' in api:
            paradigm = api.split('-')[1]
            api_paradigm_counts[paradigm] += 1
    
    print(f"\nAPI Paradigm Distribution:")
    for paradigm, count in sorted(api_paradigm_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"- {paradigm}: {count} API services")

def main():
    """Main analysis function"""
    print("API Coverage & Parity Matrix Analysis")
    print("=" * 50)
    
    df = load_data()
    
    # Run all analyses
    vendor_coverage = analyze_vendor_coverage(df)
    feature_parity = analyze_feature_parity(df)
    analyze_convergence_trends(df)
    analyze_cross_api_gaps(df)
    generate_summary_insights(df)
    
    # Save analysis results
    analysis_results = {
        'vendor_coverage': vendor_coverage,
        'feature_parity': feature_parity,
        'timestamp': '2025-08-20',
        'total_records': len(df)
    }
    
    with open('api_coverage_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    print(f"\nAnalysis complete. Results saved to api_coverage_analysis_results.json")

if __name__ == "__main__":
    main()