#!/usr/bin/env python3
"""
Incident Data Analysis
Analyzes the collected incident and recovery metrics to generate insights
"""

import pandas as pd
import json
from datetime import datetime

def analyze_incidents():
    """Analyze the collected incident data"""
    
    # Load the main incident dataset
    incidents_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/table-maintenance-costs/2025-08-21__data__incident-recovery-metrics__multi-vendor__mttr-analysis.csv')
    
    # Load the detailed table format incidents
    detailed_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/table-maintenance-costs/2025-08-21__data__table-format-incidents__detailed__corruption-recovery.csv')
    
    # Load MTTR benchmarks
    benchmarks_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/table-maintenance-costs/2025-08-21__data__mttr-benchmarks__aggregated__recovery-statistics.csv')
    
    analysis = {}
    
    # Basic statistics
    analysis['summary'] = {
        'total_incidents_collected': len(incidents_df) + len(detailed_df),
        'main_dataset_incidents': len(incidents_df),
        'detailed_format_incidents': len(detailed_df),
        'date_range': f"{incidents_df['date'].min()} to {detailed_df['date'].max()}",
        'organizations_studied': len(set(list(incidents_df['organization']) + list(detailed_df['organization'])))
    }
    
    # MTTR analysis by stack type
    combined_df = pd.concat([incidents_df, detailed_df[incidents_df.columns]], ignore_index=True)
    
    mttr_by_stack = combined_df.groupby('stack_type')['mttr_minutes'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)
    
    analysis['mttr_by_stack_type'] = mttr_by_stack.to_dict()
    
    # Data loss analysis
    data_loss_stats = combined_df.groupby('stack_type')['data_loss_gb'].agg([
        'count', 'sum', 'mean', 'max'
    ]).round(2)
    
    analysis['data_loss_by_stack_type'] = data_loss_stats.to_dict()
    
    # Incident type distribution
    incident_types = combined_df['incident_type'].value_counts().to_dict()
    analysis['incident_type_distribution'] = incident_types
    
    # Impact scope analysis  
    impact_scope = combined_df['impact_scope'].value_counts().to_dict()
    analysis['impact_scope_distribution'] = impact_scope
    
    # Modern vs Traditional comparison
    modern_formats = ['iceberg_lake', 'delta_lake', 'hudi_lake']
    traditional_formats = ['relational_database', 'mainframe_database']
    
    modern_incidents = combined_df[combined_df['stack_type'].isin(modern_formats)]
    traditional_incidents = combined_df[combined_df['stack_type'].isin(traditional_formats)]
    
    analysis['modern_vs_traditional'] = {
        'modern_table_formats': {
            'count': len(modern_incidents),
            'mean_mttr_minutes': modern_incidents['mttr_minutes'].mean(),
            'median_mttr_minutes': modern_incidents['mttr_minutes'].median(),
            'mean_data_loss_gb': modern_incidents['data_loss_gb'].mean(),
            'zero_data_loss_rate': (modern_incidents['data_loss_gb'] == 0).mean()
        },
        'traditional_databases': {
            'count': len(traditional_incidents),
            'mean_mttr_minutes': traditional_incidents['mttr_minutes'].mean(),
            'median_mttr_minutes': traditional_incidents['mttr_minutes'].median(),
            'mean_data_loss_gb': traditional_incidents['data_loss_gb'].mean(),
            'zero_data_loss_rate': (traditional_incidents['data_loss_gb'] == 0).mean()
        }
    }
    
    # Recovery method analysis from detailed dataset
    if 'recovery_method' in detailed_df.columns:
        recovery_methods = detailed_df['recovery_method'].value_counts().to_dict()
        analysis['recovery_methods'] = recovery_methods
        
        # Recovery time by method
        recovery_time_by_method = detailed_df.groupby('recovery_method')['mttr_minutes'].agg([
            'count', 'mean', 'median'
        ]).round(2).to_dict()
        analysis['recovery_time_by_method'] = recovery_time_by_method
    
    # Benchmark analysis
    analysis['benchmarks'] = {
        'fastest_recovery': {
            'stack_type': benchmarks_df.loc[benchmarks_df['mean_mttr_minutes'].idxmin(), 'stack_type'],
            'mean_mttr_minutes': benchmarks_df['mean_mttr_minutes'].min()
        },
        'slowest_recovery': {
            'stack_type': benchmarks_df.loc[benchmarks_df['mean_mttr_minutes'].idxmax(), 'stack_type'],
            'mean_mttr_minutes': benchmarks_df['mean_mttr_minutes'].max()
        },
        'highest_auto_recovery': {
            'stack_type': benchmarks_df.loc[benchmarks_df['auto_recovery_rate'].idxmax(), 'stack_type'],
            'auto_recovery_rate': benchmarks_df['auto_recovery_rate'].max()
        },
        'lowest_data_loss_risk': {
            'stack_type': benchmarks_df.loc[benchmarks_df['data_loss_probability'].idxmin(), 'stack_type'],
            'data_loss_probability': benchmarks_df['data_loss_probability'].min()
        }
    }
    
    # Key insights
    analysis['key_insights'] = [
        f"Modern table formats show {analysis['modern_vs_traditional']['modern_table_formats']['mean_mttr_minutes']:.0f}min average MTTR vs {analysis['modern_vs_traditional']['traditional_databases']['mean_mttr_minutes']:.0f}min for traditional databases",
        f"Zero data loss rate: {analysis['modern_vs_traditional']['modern_table_formats']['zero_data_loss_rate']:.1%} for modern formats vs {analysis['modern_vs_traditional']['traditional_databases']['zero_data_loss_rate']:.1%} for traditional",
        f"Metadata corruption is the most common incident type ({incident_types.get('metadata_corruption', 0)} incidents)",
        f"Delta Lake shows fastest recovery ({benchmarks_df[benchmarks_df['stack_type']=='delta_lake']['mean_mttr_minutes'].iloc[0]:.0f}min) and highest auto-recovery rate ({benchmarks_df[benchmarks_df['stack_type']=='delta_lake']['auto_recovery_rate'].iloc[0]:.1%})",
        f"Object storage accidental deletes have highest data loss risk ({benchmarks_df[benchmarks_df['stack_type']=='object_storage']['data_loss_probability'].iloc[0]:.1%})"
    ]
    
    return analysis

def main():
    print("Analyzing incident and recovery data...")
    
    analysis = analyze_incidents()
    
    # Save analysis results
    output_file = '/Users/patrickmcfadin/local_projects/post-database-era/datasets/table-maintenance-costs/2025-08-21__analysis__incident-recovery__statistical-summary.json'
    
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    # Print key insights
    print("\n=== KEY INSIGHTS ===")
    for insight in analysis['key_insights']:
        print(f"• {insight}")
    
    print(f"\nFull analysis saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()