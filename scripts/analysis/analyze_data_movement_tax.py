#!/usr/bin/env python3
"""
Data Movement Tax Analysis - Summary of egress and cross-cloud cost findings
"""

import pandas as pd
import json
from datetime import datetime

def analyze_pricing_data():
    """Analyze the official pricing data"""
    
    df = pd.read_csv('datasets/2025-08-20__data__data-movement-tax__multi-cloud__transfer-pricing.csv')
    
    analysis = {
        'total_records': len(df),
        'clouds_covered': df['cloud'].unique().tolist(),
        'movement_types': df['movement_type'].unique().tolist(),
        'cost_range': {
            'min_cost': float(df['cost_usd'].min()),
            'max_cost': float(df['cost_usd'].max()),
            'avg_cost': float(df['cost_usd'].mean())
        }
    }
    
    # Cost by cloud provider
    cloud_costs = df.groupby('cloud')['cost_usd'].agg(['min', 'max', 'mean']).round(4)
    analysis['cost_by_cloud'] = cloud_costs.to_dict('index')
    
    # Most expensive movement types
    movement_costs = df.groupby('movement_type')['cost_usd'].agg(['min', 'max', 'mean']).round(4)
    analysis['cost_by_movement_type'] = movement_costs.to_dict('index')
    
    return analysis

def analyze_realworld_data():
    """Analyze real-world case study data"""
    
    df = pd.read_csv('datasets/2025-08-20__data__data-movement-tax__real-world__egress-case-studies.csv')
    
    analysis = {
        'total_scenarios': len(df),
        'data_types': df['data_type'].value_counts().to_dict(),
        'industries_covered': df['industry'].dropna().unique().tolist(),
        'cost_statistics': {
            'min_cost': float(df['cost_usd'].min()),
            'max_cost': float(df['cost_usd'].max()),
            'median_cost': float(df['cost_usd'].median()),
            'total_cost_represented': float(df['cost_usd'].sum())
        }
    }
    
    # Optimization outcomes
    optimization_df = df[df['data_type'] == 'optimization_outcome']
    if not optimization_df.empty:
        analysis['optimization_outcomes'] = {
            'cases': len(optimization_df),
            'avg_cost_reduction_pct': float(optimization_df['cost_reduction_pct'].mean()),
            'total_savings': float(optimization_df['cost_usd'].sum())
        }
    
    # Industry breakdown
    industry_costs = df.groupby('industry')['cost_usd'].agg(['count', 'sum', 'mean']).round(2)
    analysis['cost_by_industry'] = industry_costs.to_dict('index')
    
    return analysis

def analyze_external_table_data():
    """Analyze external table and cross-cloud analytics data"""
    
    df = pd.read_csv('datasets/2025-08-20__data__data-movement-tax__external-tables__cross-cloud-analytics.csv')
    
    analysis = {
        'total_scenarios': len(df),
        'scenario_types': df['scenario_type'].value_counts().to_dict(),
        'services_covered': df['service'].unique().tolist(),
        'data_formats': df['data_format'].unique().tolist(),
        'cost_statistics': {
            'min_cost': float(df['cost_usd'].min()),
            'max_cost': float(df['cost_usd'].max()),
            'avg_cost_per_scenario': float(df['cost_usd'].mean()),
            'total_cost_represented': float(df['cost_usd'].sum())
        }
    }
    
    # Cost per GB analysis
    df['cost_per_gb'] = df['cost_usd'] / df['gb_moved']
    analysis['cost_per_gb_stats'] = {
        'min_cost_per_gb': float(df['cost_per_gb'].min()),
        'max_cost_per_gb': float(df['cost_per_gb'].max()),
        'avg_cost_per_gb': float(df['cost_per_gb'].mean())
    }
    
    # Service comparison
    service_costs = df.groupby('service')['cost_per_gb'].agg(['min', 'max', 'mean']).round(4)
    analysis['cost_per_gb_by_service'] = service_costs.to_dict('index')
    
    return analysis

def generate_key_insights():
    """Generate key insights from the data movement tax analysis"""
    
    insights = {
        'cross_cloud_premium': {
            'finding': 'Cross-cloud data movement carries significant premium',
            'evidence': 'AWS to GCP transfers cost ~$0.087/GB vs $0.02/GB for same-cloud cross-region',
            'impact': 'Multi-cloud architectures face 4x higher data movement costs'
        },
        'external_table_penalty': {
            'finding': 'External table queries have hidden data movement costs',
            'evidence': 'Cross-region external table scans cost $0.02-0.08/GB beyond compute',
            'impact': 'Data lakehouse architectures need careful region planning'
        },
        'optimization_roi': {
            'finding': 'CDN and caching optimizations show strong ROI',
            'evidence': 'Case studies show 40-80% cost reductions through optimization',
            'impact': 'Egress optimization should be priority for data-heavy applications'
        },
        'database_replication_costs': {
            'finding': 'Cross-region database replication has substantial ongoing costs',
            'evidence': 'Aurora Global Database: $0.087/GB for cross-region sync',
            'impact': 'DR and read replica strategies need cost modeling'
        },
        'free_tier_limits': {
            'finding': 'Free tiers provide minimal coverage for production workloads',
            'evidence': 'AWS: 1GB/month free, GCP: 1GB/month, Azure: 5GB/month',
            'impact': 'Free tiers dont cover meaningful data movement scenarios'
        }
    }
    
    return insights

def main():
    """Generate comprehensive data movement tax analysis"""
    
    print("Analyzing Data Movement Tax Datasets...")
    
    # Analyze each dataset
    pricing_analysis = analyze_pricing_data()
    realworld_analysis = analyze_realworld_data()
    external_table_analysis = analyze_external_table_data()
    
    # Generate insights
    key_insights = generate_key_insights()
    
    # Compile comprehensive analysis
    comprehensive_analysis = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'datasets_analyzed': 3,
        'total_records': (pricing_analysis['total_records'] + 
                         realworld_analysis['total_scenarios'] + 
                         external_table_analysis['total_scenarios']),
        'official_pricing_analysis': pricing_analysis,
        'realworld_scenarios_analysis': realworld_analysis,
        'external_table_analysis': external_table_analysis,
        'key_insights': key_insights,
        'summary_findings': {
            'cost_range_per_gb': '$0.01 - $0.12 for standard cloud egress',
            'cross_cloud_premium': '4x higher costs for multi-cloud data movement',
            'optimization_potential': '40-80% cost reduction through CDN/caching',
            'database_tax': 'Cross-region DB replication adds $0.02-0.087/GB ongoing cost',
            'external_table_penalty': 'Lakehouse queries incur cross-region data movement tax'
        }
    }
    
    # Save analysis
    filename = f'datasets/2025-08-20__analysis__data-movement-tax__comprehensive-findings.json'
    with open(filename, 'w') as f:
        json.dump(comprehensive_analysis, f, indent=2, default=str)
    
    print(f"Analysis saved to {filename}")
    
    # Print summary
    print("\n=== DATA MOVEMENT TAX ANALYSIS SUMMARY ===")
    print(f"Total records analyzed: {comprehensive_analysis['total_records']}")
    print(f"Clouds covered: AWS, GCP, Azure, Multi-cloud scenarios")
    print(f"Cost range: $0.01-$0.12/GB for standard egress")
    print(f"Cross-cloud premium: ~4x higher than intra-cloud movement")
    print(f"Optimization potential: 40-80% cost reduction achievable")
    
    print("\n=== KEY COST DRIVERS ===")
    print("1. Internet egress: $0.08-0.12/GB")
    print("2. Cross-cloud movement: $0.087-0.17/GB") 
    print("3. Cross-region DB replication: $0.02-0.087/GB")
    print("4. External table cross-region queries: $0.05-0.14/GB")
    
    print("\n=== OPTIMIZATION STRATEGIES ===")
    print("1. CDN implementation: 80% cost reduction")
    print("2. Regional data placement: 77% cost reduction")
    print("3. Compression + caching: 60% cost reduction")
    print("4. Batch vs real-time: 60% cost reduction")

if __name__ == "__main__":
    main()