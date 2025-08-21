#!/usr/bin/env python3
"""
Analyze and summarize compute utilization datasets
"""

import pandas as pd
import json
from datetime import datetime

def analyze_datasets():
    """Analyze the created compute utilization datasets"""
    
    # Load all datasets
    datasets = {
        'cluster_serverless': '2025-08-20__data__compute-utilization__multi-vendor__cluster-serverless-comparison.csv',
        'kubernetes': '2025-08-20__data__compute-utilization__kubernetes__workload-efficiency.csv',
        'case_studies': '2025-08-20__data__compute-utilization__case-studies__optimization-outcomes.csv',
        'autoscaler': '2025-08-20__data__compute-utilization__autoscaler__efficiency-metrics.csv'
    }
    
    analysis = {}
    
    for name, filename in datasets.items():
        try:
            df = pd.read_csv(filename)
            analysis[name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'sample_data': df.head(3).to_dict('records')
            }
            
            # Specific analysis for each dataset
            if name == 'cluster_serverless':
                cluster_data = df[df['mode'] == 'cluster']
                serverless_data = df[df['mode'] == 'serverless']
                
                analysis[name].update({
                    'cluster_avg_cpu_util': round(cluster_data['cpu_util_avg'].mean(), 1),
                    'serverless_avg_cpu_util': round(serverless_data['cpu_util_avg'].mean(), 1),
                    'cluster_avg_idle': round(cluster_data['idle_pct'].mean(), 1),
                    'serverless_avg_idle': round(serverless_data['idle_pct'].mean(), 1),
                    'utilization_improvement': round(serverless_data['cpu_util_avg'].mean() - cluster_data['cpu_util_avg'].mean(), 1)
                })
            
            elif name == 'kubernetes':
                analysis[name].update({
                    'avg_cpu_by_size': df.groupby('cluster_size')['cpu_util_avg'].mean().round(1).to_dict(),
                    'avg_idle_by_size': df.groupby('cluster_size')['idle_pct'].mean().round(1).to_dict(),
                    'cost_range': f"${df['cost_per_workload_hour'].min():.2f} - ${df['cost_per_workload_hour'].max():.2f}"
                })
            
            elif name == 'case_studies':
                analysis[name].update({
                    'avg_cost_reduction': round(df['cost_reduction_pct'].mean(), 1),
                    'avg_roi_months': round(df['roi_months'].mean(), 1),
                    'scenarios': df['before_deployment'].value_counts().to_dict()
                })
            
            elif name == 'autoscaler':
                analysis[name].update({
                    'avg_accuracy': round(df['scale_accuracy_pct'].mean(), 1),
                    'avg_response_time': round(df['response_time_seconds'].mean(), 1),
                    'avg_cost_savings': round(df['cost_savings_pct'].mean(), 1)
                })
                
        except Exception as e:
            analysis[name] = {'error': str(e)}
    
    return analysis

def main():
    print("Analyzing compute utilization datasets...")
    
    analysis = analyze_datasets()
    
    # Save analysis results
    timestamp = datetime.now().strftime("%Y-%m-%d")
    with open(f'{timestamp}__analysis__compute-utilization__comprehensive-summary.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    # Print summary
    print("\nDataset Summary:")
    print("================")
    
    for dataset_name, data in analysis.items():
        if 'error' in data:
            print(f"\n{dataset_name}: ERROR - {data['error']}")
            continue
            
        print(f"\n{dataset_name}:")
        print(f"  Rows: {data['rows']}")
        print(f"  Columns: {data['columns']}")
        
        # Specific insights
        if dataset_name == 'cluster_serverless':
            print(f"  Key Insights:")
            print(f"    - Cluster avg CPU: {data['cluster_avg_cpu_util']}%")
            print(f"    - Serverless avg CPU: {data['serverless_avg_cpu_util']}%")
            print(f"    - Utilization improvement: +{data['utilization_improvement']}%")
            print(f"    - Cluster avg idle: {data['cluster_avg_idle']}%")
            print(f"    - Serverless avg idle: {data['serverless_avg_idle']}%")
        
        elif dataset_name == 'kubernetes':
            print(f"  Key Insights:")
            print(f"    - CPU utilization by cluster size: {data['avg_cpu_by_size']}")
            print(f"    - Cost range: {data['cost_range']}")
        
        elif dataset_name == 'case_studies':
            print(f"  Key Insights:")
            print(f"    - Average cost reduction: {data['avg_cost_reduction']}%")
            print(f"    - Average ROI: {data['avg_roi_months']} months")
        
        elif dataset_name == 'autoscaler':
            print(f"  Key Insights:")
            print(f"    - Average scaling accuracy: {data['avg_accuracy']}%")
            print(f"    - Average response time: {data['avg_response_time']}s")
            print(f"    - Average cost savings: {data['avg_cost_savings']}%")
    
    print(f"\nDetailed analysis saved to: {timestamp}__analysis__compute-utilization__comprehensive-summary.json")

if __name__ == "__main__":
    main()