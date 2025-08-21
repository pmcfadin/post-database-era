#!/usr/bin/env python3
"""
Analysis script for compute-storage separation cost data.
Generates insights and visualizations from the collected datasets.
"""

import pandas as pd
import json
from datetime import datetime

def analyze_storage_performance_cost():
    """Analyze storage performance vs cost trade-offs."""
    
    # Load storage comparison data
    storage_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__storage-separation__performance-cost__nvme-vs-disaggregated.csv')
    
    # Calculate performance per dollar metrics
    storage_df['iops_per_dollar'] = storage_df['iops_capability'] / storage_df['total_cost_per_tb_hour']
    storage_df['throughput_per_dollar'] = storage_df['throughput_mbps'] / storage_df['total_cost_per_tb_hour']
    
    # Group by storage type
    storage_summary = storage_df.groupby('storage_type').agg({
        'iops_capability': 'mean',
        'latency_p99_ms': 'mean',
        'total_cost_per_tb_hour': 'mean',
        'iops_per_dollar': 'mean'
    }).round(2)
    
    return storage_summary

def analyze_elasticity_savings():
    """Analyze cost savings from elastic scaling."""
    
    # Load elasticity data
    elasticity_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__elasticity-savings__scaling-models__cost-optimization.csv')
    
    # Calculate savings vs traditional monolithic
    traditional_cost = elasticity_df[elasticity_df['scaling_model'] == 'monolithic']['monthly_cost_usd'].iloc[0]
    
    # Calculate savings for each disaggregated model
    savings_analysis = []
    for _, row in elasticity_df.iterrows():
        if row['scaling_model'] in ['disaggregated', 'serverless']:
            savings_pct = ((traditional_cost - row['monthly_cost_usd']) / traditional_cost) * 100
            savings_analysis.append({
                'database': row['database'],
                'scaling_model': row['scaling_model'],
                'monthly_cost': row['monthly_cost_usd'],
                'savings_percent': round(savings_pct, 1),
                'compute_utilization': row['compute_utilization'],
                'storage_utilization': row['storage_utilization']
            })
    
    return pd.DataFrame(savings_analysis)

def analyze_tco_scale_economics():
    """Analyze TCO curves across different workload sizes."""
    
    # Load TCO data
    tco_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__tco-curves__workload-scaling__cost-per-tb.csv')
    
    # Create scale economics analysis
    scale_analysis = []
    workload_sizes = tco_df['workload_size_tb'].unique()
    
    for size in workload_sizes:
        size_data = tco_df[tco_df['workload_size_tb'] == size]
        
        local_costs = size_data[size_data['architecture'] == 'local_nvme']['cost_per_tb'].tolist()
        disagg_costs = size_data[size_data['architecture'] == 'disaggregated']['cost_per_tb'].tolist()
        
        if local_costs and disagg_costs:
            local_cost = local_costs[0]
            disagg_cost = disagg_costs[0]
            savings_pct = ((local_cost - disagg_cost) / local_cost) * 100
            
            scale_analysis.append({
                'workload_size_tb': size,
                'local_cost_per_tb': local_cost,
                'disaggregated_cost_per_tb': disagg_cost,
                'savings_percent': round(savings_pct, 1),
                'crossover_point': 'disaggregated' if disagg_cost < local_cost else 'local'
            })
    
    return pd.DataFrame(scale_analysis)

def analyze_benchmark_performance():
    """Analyze benchmark performance across storage types."""
    
    # Load TPC benchmark data
    tpc_df = pd.read_csv('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__tpc-benchmarks__storage-comparison__performance-cost.csv')
    
    # Calculate performance per dollar for different workloads
    performance_analysis = []
    
    for _, row in tpc_df.iterrows():
        perf_per_dollar = None
        metric_name = None
        
        if row['benchmark'] == 'TPC-C' and pd.notna(row['transactions_per_minute']):
            perf_per_dollar = row['transactions_per_minute'] / row['total_cost_per_hour']
            metric_name = 'tpmC_per_dollar_hour'
        elif row['benchmark'] == 'TPC-H' and pd.notna(row['queries_per_hour']):
            perf_per_dollar = row['queries_per_hour'] / row['total_cost_per_hour']
            metric_name = 'queries_per_dollar_hour'
        
        if perf_per_dollar:
            performance_analysis.append({
                'benchmark': row['benchmark'],
                'engine': row['engine'],
                'storage_type': row['storage_type'],
                'performance_per_dollar': round(perf_per_dollar, 2),
                'metric': metric_name,
                'latency_p99_ms': row['latency_p99_ms']
            })
    
    return pd.DataFrame(performance_analysis)

def generate_insights_report():
    """Generate comprehensive insights report."""
    
    # Run all analyses
    storage_summary = analyze_storage_performance_cost()
    elasticity_savings = analyze_elasticity_savings()
    scale_economics = analyze_tco_scale_economics()
    benchmark_performance = analyze_benchmark_performance()
    
    # Generate insights
    insights = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'key_findings': {
            'storage_performance': {
                'best_iops_per_dollar': storage_summary['iops_per_dollar'].idxmax(),
                'lowest_latency': storage_summary['latency_p99_ms'].idxmin(),
                'highest_cost': storage_summary['total_cost_per_tb_hour'].idxmax(),
                'performance_summary': storage_summary.to_dict()
            },
            'elasticity_savings': {
                'highest_savings': elasticity_savings.loc[elasticity_savings['savings_percent'].idxmax()].to_dict(),
                'average_savings': round(elasticity_savings['savings_percent'].mean(), 1),
                'savings_range': f"{elasticity_savings['savings_percent'].min():.1f}% - {elasticity_savings['savings_percent'].max():.1f}%"
            },
            'scale_economics': {
                'crossover_point': scale_economics[scale_economics['crossover_point'] == 'disaggregated']['workload_size_tb'].min(),
                'max_savings': scale_economics['savings_percent'].max(),
                'scale_summary': scale_economics.to_dict('records')
            },
            'benchmark_insights': {
                'best_oltp_performer': benchmark_performance[benchmark_performance['benchmark'] == 'TPC-C'].nlargest(1, 'performance_per_dollar').to_dict('records'),
                'best_olap_performer': benchmark_performance[benchmark_performance['benchmark'] == 'TPC-H'].nlargest(1, 'performance_per_dollar').to_dict('records')
            }
        },
        'recommendations': {
            'workload_guidance': {
                'small_oltp': 'Consider Aurora Serverless for cost efficiency',
                'large_oltp': 'Local NVMe for predictable latency requirements',
                'analytics': 'Object storage (S3) with query engines for cost optimization',
                'mixed_workloads': 'Hybrid architecture with workload routing'
            },
            'cost_optimization': {
                'immediate_savings': 'Move analytics workloads to disaggregated storage',
                'scaling_efficiency': 'Implement serverless or auto-scaling for variable workloads',
                'data_movement': 'Minimize cross-region transfers to reduce egress costs'
            }
        }
    }
    
    return insights

def main():
    """Main analysis function."""
    
    print("Analyzing Compute-Storage Separation Cost Data...")
    print("=" * 60)
    
    # Generate comprehensive analysis
    insights = generate_insights_report()
    
    # Save insights to JSON
    output_file = '/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__analysis__compute-storage-separation__cost-insights.json'
    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=2)
    
    # Print key findings
    print("\\nKEY FINDINGS:")
    print("-" * 40)
    
    print(f"\\n1. STORAGE PERFORMANCE:")
    print(f"   - Best IOPS/$ ratio: {insights['key_findings']['storage_performance']['best_iops_per_dollar']}")
    print(f"   - Lowest latency: {insights['key_findings']['storage_performance']['lowest_latency']}")
    
    print(f"\\n2. ELASTICITY SAVINGS:")
    print(f"   - Average savings: {insights['key_findings']['elasticity_savings']['average_savings']}%")
    print(f"   - Savings range: {insights['key_findings']['elasticity_savings']['savings_range']}")
    
    print(f"\\n3. SCALE ECONOMICS:")
    print(f"   - Disaggregated becomes cost-effective at: {insights['key_findings']['scale_economics']['crossover_point']}TB")
    print(f"   - Maximum savings: {insights['key_findings']['scale_economics']['max_savings']:.1f}%")
    
    print(f"\\n4. WORKLOAD RECOMMENDATIONS:")
    for workload, recommendation in insights['recommendations']['workload_guidance'].items():
        print(f"   - {workload.replace('_', ' ').title()}: {recommendation}")
    
    print(f"\\nDetailed analysis saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()