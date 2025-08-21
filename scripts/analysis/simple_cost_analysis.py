#!/usr/bin/env python3
"""
Simple cost analysis using standard library tools.
Analyzes compute-storage separation cost data without external dependencies.
"""

import csv
import json
from datetime import datetime
from statistics import mean

def load_csv_data(filename):
    """Load CSV data into list of dictionaries."""
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric strings to floats where appropriate
            for key, value in row.items():
                try:
                    if '.' in value or value.isdigit():
                        row[key] = float(value)
                except (ValueError, AttributeError):
                    pass
            data.append(row)
    return data

def analyze_storage_costs():
    """Analyze storage performance vs cost."""
    
    storage_data = load_csv_data('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__storage-separation__performance-cost__nvme-vs-disaggregated.csv')
    
    # Group by storage type
    storage_groups = {}
    for row in storage_data:
        storage_type = row['storage_type']
        if storage_type not in storage_groups:
            storage_groups[storage_type] = []
        storage_groups[storage_type].append(row)
    
    # Calculate averages for each storage type
    storage_summary = {}
    for storage_type, rows in storage_groups.items():
        storage_summary[storage_type] = {
            'avg_iops': mean([row['iops_capability'] for row in rows]),
            'avg_latency_ms': mean([row['latency_p99_ms'] for row in rows]),
            'avg_cost_per_tb_hour': mean([row['total_cost_per_tb_hour'] for row in rows]),
            'iops_per_dollar': mean([row['iops_capability'] / row['total_cost_per_tb_hour'] for row in rows])
        }
    
    return storage_summary

def analyze_elasticity_savings():
    """Analyze cost savings from elastic scaling."""
    
    elasticity_data = load_csv_data('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__elasticity-savings__scaling-models__cost-optimization.csv')
    
    # Find traditional monolithic baseline
    traditional_cost = None
    for row in elasticity_data:
        if row['scaling_model'] == 'monolithic':
            traditional_cost = row['monthly_cost_usd']
            break
    
    if not traditional_cost:
        return {}
    
    # Calculate savings for each model
    savings_analysis = {}
    for row in elasticity_data:
        if row['scaling_model'] in ['disaggregated', 'serverless']:
            savings_pct = ((traditional_cost - row['monthly_cost_usd']) / traditional_cost) * 100
            savings_analysis[row['database']] = {
                'monthly_cost': row['monthly_cost_usd'],
                'savings_percent': round(savings_pct, 1),
                'scaling_model': row['scaling_model']
            }
    
    return savings_analysis

def analyze_benchmark_performance():
    """Analyze TPC benchmark performance."""
    
    tpc_data = load_csv_data('/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__data__tpc-benchmarks__storage-comparison__performance-cost.csv')
    
    performance_summary = {
        'tpc_c_results': [],
        'tpc_h_results': []
    }
    
    for row in tpc_data:
        result = {
            'engine': row['engine'],
            'storage_type': row['storage_type'],
            'cost_per_hour': row['total_cost_per_hour'],
            'latency_p99_ms': row['latency_p99_ms']
        }
        
        if row['benchmark'] == 'TPC-C' and row['transactions_per_minute']:
            result['performance_per_dollar'] = row['transactions_per_minute'] / row['total_cost_per_hour']
            result['metric'] = 'tpmC per $/hour'
            performance_summary['tpc_c_results'].append(result)
        elif row['benchmark'] == 'TPC-H' and row['queries_per_hour']:
            result['performance_per_dollar'] = row['queries_per_hour'] / row['total_cost_per_hour']
            result['metric'] = 'queries per $/hour'
            performance_summary['tpc_h_results'].append(result)
    
    return performance_summary

def main():
    """Main analysis function."""
    
    print("Computing Storage Separation Cost Analysis")
    print("=" * 50)
    
    # Analyze storage costs
    print("\\n1. STORAGE ARCHITECTURE ANALYSIS:")
    print("-" * 35)
    storage_summary = analyze_storage_costs()
    
    for storage_type, metrics in storage_summary.items():
        print(f"\\n{storage_type.upper().replace('_', ' ')}:")
        print(f"  Average IOPS: {metrics['avg_iops']:,.0f}")
        print(f"  Average P99 Latency: {metrics['avg_latency_ms']:.1f}ms")
        print(f"  Average Cost/TB/Hour: ${metrics['avg_cost_per_tb_hour']:.2f}")
        print(f"  IOPS per Dollar: {metrics['iops_per_dollar']:.0f}")
    
    # Analyze elasticity savings
    print("\\n\\n2. ELASTICITY SAVINGS ANALYSIS:")
    print("-" * 35)
    savings_analysis = analyze_elasticity_savings()
    
    for database, metrics in savings_analysis.items():
        print(f"\\n{database}:")
        print(f"  Monthly Cost: ${metrics['monthly_cost']:,.0f}")
        print(f"  Savings: {metrics['savings_percent']:.1f}%")
        print(f"  Model: {metrics['scaling_model'].title()}")
    
    # Analyze benchmark performance
    print("\\n\\n3. BENCHMARK PERFORMANCE ANALYSIS:")
    print("-" * 40)
    benchmark_results = analyze_benchmark_performance()
    
    print("\\nTPC-C (OLTP) Results:")
    for result in benchmark_results['tpc_c_results']:
        print(f"  {result['engine']} on {result['storage_type']}:")
        print(f"    Performance/$$: {result['performance_per_dollar']:.1f} {result['metric']}")
        print(f"    P99 Latency: {result['latency_p99_ms']:.1f}ms")
    
    print("\\nTPC-H (OLAP) Results:")
    for result in benchmark_results['tpc_h_results']:
        print(f"  {result['engine']} on {result['storage_type']}:")
        print(f"    Performance/$$: {result['performance_per_dollar']:.1f} {result['metric']}")
        print(f"    P99 Latency: {result['latency_p99_ms']:.1f}ms")
    
    # Generate key insights
    print("\\n\\n4. KEY INSIGHTS:")
    print("-" * 20)
    
    # Find best IOPS per dollar
    best_iops_storage = max(storage_summary.items(), key=lambda x: x[1]['iops_per_dollar'])
    print(f"\\n• Best IOPS per dollar: {best_iops_storage[0]} ({best_iops_storage[1]['iops_per_dollar']:.0f} IOPS/$)")
    
    # Find highest savings
    if savings_analysis:
        best_savings = max(savings_analysis.items(), key=lambda x: x[1]['savings_percent'])
        print(f"• Highest elasticity savings: {best_savings[0]} ({best_savings[1]['savings_percent']:.1f}%)")
    
    # Find best TPC-C performance per dollar
    if benchmark_results['tpc_c_results']:
        best_tpc_c = max(benchmark_results['tpc_c_results'], key=lambda x: x['performance_per_dollar'])
        print(f"• Best TPC-C performance/$$: {best_tpc_c['engine']} on {best_tpc_c['storage_type']}")
    
    print("\\n\\n5. RECOMMENDATIONS:")
    print("-" * 20)
    print("\\n• For latency-sensitive OLTP: Use local NVMe storage")
    print("• For cost-sensitive analytics: Use object storage (S3) with query engines")
    print("• For variable workloads: Implement serverless or auto-scaling")
    print("• For large scale (>10TB): Disaggregated storage provides better TCO")
    print("• For small workloads (<1TB): Consider managed services like Aurora Serverless")
    
    # Save summary data
    summary_data = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'storage_summary': storage_summary,
        'savings_analysis': savings_analysis,
        'benchmark_results': benchmark_results
    }
    
    output_file = '/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets/2025-08-20__analysis__cost-summary.json'
    with open(output_file, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    print(f"\\nDetailed analysis saved to: {output_file}")

if __name__ == "__main__":
    main()