#!/usr/bin/env python3
"""
Parquet Features Analysis
Analyzes the collected Parquet features data to extract insights
"""

import pandas as pd
import json
from datetime import datetime

def analyze_feature_adoption():
    """Analyze feature adoption patterns"""
    # Load the comprehensive features dataset
    df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/parquet-features/2025-08-20__data__parquet-features__comprehensive__feature-adoption.csv')
    
    analysis = {
        'feature_adoption_summary': {
            'total_features': len(df),
            'enabled_features': len(df[df['enabled'] == 1]),
            'disabled_features': len(df[df['enabled'] == 0]),
            'adoption_rate': len(df[df['enabled'] == 1]) / len(df) * 100
        },
        'by_feature_type': df.groupby('feature_type')['enabled'].agg(['count', 'sum', 'mean']).to_dict(),
        'by_adoption_level': df['adoption_level'].value_counts().to_dict(),
        'compression_algorithms': df[df['feature_type'] == 'compression'][['parquet_feature', 'adoption_level', 'performance_impact']].to_dict('records'),
        'encoding_types': df[df['feature_type'] == 'encoding'][['parquet_feature', 'adoption_level', 'performance_impact']].to_dict('records')
    }
    
    return analysis

def analyze_performance_benchmarks():
    """Analyze performance benchmark data"""
    df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/parquet-features/2025-08-20__data__parquet-features__performance-studies__benchmark-results.csv')
    
    # Clean numeric columns
    numeric_cols = ['compression_ratio', 'encode_speed_mbps', 'decode_speed_mbps', 'compress_speed_mbps', 'decompress_speed_mbps']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    analysis = {
        'compression_performance': {
            'by_algorithm': df[df['study_type'] == 'compression_comparison'].groupby('parquet_feature').agg({
                'compression_ratio': 'mean',
                'compress_speed_mbps': 'mean',
                'decompress_speed_mbps': 'mean',
                'query_speedup_factor': 'mean'
            }).fillna(0).to_dict(),
            'best_compression_ratio': df.loc[df['compression_ratio'].idxmax(), ['parquet_feature', 'compression_ratio']].to_dict() if not df['compression_ratio'].isna().all() else None,
            'fastest_compression': df.loc[df['compress_speed_mbps'].idxmax(), ['parquet_feature', 'compress_speed_mbps']].to_dict() if not df['compress_speed_mbps'].isna().all() else None
        },
        'encoding_performance': {
            'by_encoding': df[df['study_type'] == 'encoding_comparison'].groupby('parquet_feature').agg({
                'compression_ratio': 'mean',
                'encode_speed_mbps': 'mean',
                'decode_speed_mbps': 'mean'
            }).fillna(0).to_dict()
        },
        'bloom_filter_effectiveness': {
            'point_lookup_speedup': df[df['parquet_feature'] == 'Bloom Filters']['point_lookup_speedup'].mean(),
            'scan_reduction': df[df['parquet_feature'] == 'Bloom Filters']['scan_reduction_percent'].mean(),
            'false_positive_rate': df[df['parquet_feature'] == 'Bloom Filters']['false_positive_rate'].mean()
        }
    }
    
    return analysis

def analyze_production_adoption():
    """Analyze production adoption patterns"""
    df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/datasets/parquet-features/2025-08-20__data__parquet-features__production-adoption__real-world-usage.csv')
    
    analysis = {
        'enterprise_adoption': {
            'companies_analyzed': df[df['dataset_id'] == 'enterprise_adoption']['company'].nunique(),
            'average_data_scale_tb': df[df['dataset_id'] == 'enterprise_adoption']['data_scale_tb'].mean(),
            'cost_savings_range': {
                'min': df[df['dataset_id'] == 'enterprise_adoption']['cost_savings_percent'].min(),
                'max': df[df['dataset_id'] == 'enterprise_adoption']['cost_savings_percent'].max(),
                'mean': df[df['dataset_id'] == 'enterprise_adoption']['cost_savings_percent'].mean()
            },
            'most_common_features': df[df['dataset_id'] == 'enterprise_adoption']['parquet_feature'].value_counts().to_dict()
        },
        'cloud_provider_support': {
            'providers_analyzed': df[df['dataset_id'] == 'cloud_provider_adoption']['provider'].nunique(),
            'bloom_filter_support_rate': df[df['dataset_id'] == 'cloud_provider_adoption']['bloom_filters_supported'].mean() * 100,
            'default_compression': df[df['dataset_id'] == 'cloud_provider_adoption']['default_compression'].value_counts().to_dict()
        },
        'open_source_adoption': {
            'projects_analyzed': df[df['dataset_id'] == 'oss_adoption']['project'].nunique(),
            'average_adoption_rate': df[df['dataset_id'] == 'oss_adoption']['adoption_rate_percent'].mean(),
            'feature_support_matrix': df[df['dataset_id'] == 'oss_adoption'].groupby('project').agg({
                'write_support': 'mean',
                'read_support': 'mean',
                'adoption_rate_percent': 'mean'
            }).to_dict()
        },
        'industry_survey_insights': {
            'general_parquet_adoption': df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'General Parquet Adoption')]['adoption_percent'].iloc[0] if len(df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'General Parquet Adoption')]) > 0 else None,
            'bloom_filter_awareness': df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Bloom Filters Awareness')]['aware_percent'].iloc[0] if len(df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Bloom Filters Awareness')]) > 0 else None,
            'compression_usage_breakdown': {
                'snappy': df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]['snappy_percent'].iloc[0] if len(df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]) > 0 else None,
                'gzip': df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]['gzip_percent'].iloc[0] if len(df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]) > 0 else None,
                'zstd': df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]['zstd_percent'].iloc[0] if len(df[(df['dataset_id'] == 'industry_survey_2024') & (df['parquet_feature'] == 'Compression Usage')]) > 0 else None
            }
        }
    }
    
    return analysis

def generate_summary_report():
    """Generate comprehensive summary report"""
    print("Analyzing Parquet Features Data...")
    
    feature_analysis = analyze_feature_adoption()
    performance_analysis = analyze_performance_benchmarks()
    adoption_analysis = analyze_production_adoption()
    
    summary = {
        'analysis_date': datetime.now().isoformat(),
        'datasets_analyzed': [
            '2025-08-20__data__parquet-features__comprehensive__feature-adoption.csv',
            '2025-08-20__data__parquet-features__performance-studies__benchmark-results.csv',
            '2025-08-20__data__parquet-features__production-adoption__real-world-usage.csv'
        ],
        'key_findings': {
            'feature_adoption': feature_analysis,
            'performance_benchmarks': performance_analysis,
            'production_adoption': adoption_analysis
        },
        'actionable_insights': [
            f"Parquet adoption rate across analyzed features: {feature_analysis['feature_adoption_summary']['adoption_rate']:.1f}%",
            f"Enterprise companies save average {adoption_analysis['enterprise_adoption']['cost_savings_range']['mean']:.1f}% on storage costs",
            f"Snappy compression dominates with {adoption_analysis['industry_survey_insights']['compression_usage_breakdown']['snappy']}% market share",
            f"Bloom filters show {performance_analysis['bloom_filter_effectiveness']['point_lookup_speedup']:.1f}x speedup but only {adoption_analysis['industry_survey_insights']['bloom_filter_awareness']}% awareness",
            f"Strong consistency now available across all major cloud providers"
        ]
    }
    
    return summary

if __name__ == "__main__":
    summary = generate_summary_report()
    
    # Save summary to JSON
    output_file = '/Users/patrickmcfadin/local_projects/post-database-era/datasets/parquet-features/2025-08-20__analysis__parquet-features__comprehensive-summary.json'
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nAnalysis complete!")
    print(f"Summary saved to: {output_file}")
    
    # Print key insights
    print("\n=== KEY INSIGHTS ===")
    for insight in summary['actionable_insights']:
        print(f"• {insight}")