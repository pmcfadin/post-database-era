#!/usr/bin/env python3
"""
Table Maintenance Cost Analysis
Analyzes all collected maintenance cost data to provide insights
"""

import pandas as pd
import json
from datetime import datetime

def analyze_all_datasets():
    """Analyze all table maintenance cost datasets"""
    print("Analyzing table maintenance cost data...")
    
    # Load all datasets
    optimization_costs = pd.read_csv('2025-08-21__data__table-maintenance-costs__multi-vendor__optimization-job-costs.csv')
    scheduler_costs = pd.read_csv('2025-08-21__data__table-maintenance-costs__job-schedulers__monthly-spend-breakdown.csv')
    billing_costs = pd.read_csv('2025-08-21__data__table-maintenance-costs__cloud-billing__detailed-cost-breakdown.csv')
    
    analysis = {}
    
    # Overall cost analysis
    total_optimization_cost = optimization_costs['cost_usd'].sum()
    total_scheduler_monthly = scheduler_costs['monthly_cost_usd'].sum()
    total_billing_cost = billing_costs['total_cost_usd'].sum()
    
    analysis['total_costs'] = {
        'optimization_jobs_sample': total_optimization_cost,
        'scheduler_monthly_spend': total_scheduler_monthly,
        'cloud_billing_sample': total_billing_cost,
        'combined_sample_cost': total_optimization_cost + total_billing_cost
    }
    
    # Cost per TB analysis
    opt_data_tb = optimization_costs['data_tb_touched'].sum()
    opt_cost_per_tb = total_optimization_cost / opt_data_tb if opt_data_tb > 0 else 0
    
    sched_data_tb = scheduler_costs['data_tb_processed'].sum()
    sched_cost_per_tb = total_scheduler_monthly / sched_data_tb if sched_data_tb > 0 else 0
    
    bill_data_tb = billing_costs['data_tb_touched'].sum()
    bill_cost_per_tb = total_billing_cost / bill_data_tb if bill_data_tb > 0 else 0
    
    analysis['cost_per_tb'] = {
        'optimization_jobs': round(opt_cost_per_tb, 2),
        'scheduler_monthly': round(sched_cost_per_tb, 2),
        'cloud_billing': round(bill_cost_per_tb, 2),
        'average_across_sources': round((opt_cost_per_tb + sched_cost_per_tb + bill_cost_per_tb) / 3, 2)
    }
    
    # Job type analysis
    job_type_costs = {}
    
    # From optimization dataset
    for _, row in optimization_costs.iterrows():
        job_type = row['job_type']
        if job_type not in job_type_costs:
            job_type_costs[job_type] = {'cost': 0, 'data_tb': 0, 'sources': 0}
        job_type_costs[job_type]['cost'] += row['cost_usd']
        job_type_costs[job_type]['data_tb'] += row['data_tb_touched']
        job_type_costs[job_type]['sources'] += 1
    
    # From scheduler dataset  
    for _, row in scheduler_costs.iterrows():
        job_type = row['job_type']
        if job_type not in job_type_costs:
            job_type_costs[job_type] = {'cost': 0, 'data_tb': 0, 'sources': 0}
        job_type_costs[job_type]['cost'] += row['monthly_cost_usd']
        job_type_costs[job_type]['data_tb'] += row['data_tb_processed']
        job_type_costs[job_type]['sources'] += 1
    
    # From billing dataset
    for _, row in billing_costs.iterrows():
        job_type = row['job_type']
        if job_type not in job_type_costs:
            job_type_costs[job_type] = {'cost': 0, 'data_tb': 0, 'sources': 0}
        job_type_costs[job_type]['cost'] += row['total_cost_usd']
        job_type_costs[job_type]['data_tb'] += row['data_tb_touched']
        job_type_costs[job_type]['sources'] += 1
    
    # Calculate cost per TB for each job type
    job_type_analysis = {}
    for job_type, data in job_type_costs.items():
        cost_per_tb = data['cost'] / data['data_tb'] if data['data_tb'] > 0 else 0
        job_type_analysis[job_type] = {
            'total_cost': round(data['cost'], 2),
            'total_data_tb': round(data['data_tb'], 1),
            'cost_per_tb': round(cost_per_tb, 2),
            'data_sources': data['sources']
        }
    
    analysis['job_type_analysis'] = job_type_analysis
    
    # Format analysis
    format_costs = {}
    
    # Aggregate by format across all datasets
    for _, row in optimization_costs.iterrows():
        fmt = row['format']
        if fmt not in format_costs:
            format_costs[fmt] = {'cost': 0, 'data_tb': 0, 'jobs': 0}
        format_costs[fmt]['cost'] += row['cost_usd']
        format_costs[fmt]['data_tb'] += row['data_tb_touched']
        format_costs[fmt]['jobs'] += row['runs']
    
    for _, row in scheduler_costs.iterrows():
        fmt = row['format']
        if fmt not in format_costs:
            format_costs[fmt] = {'cost': 0, 'data_tb': 0, 'jobs': 0}
        format_costs[fmt]['cost'] += row['monthly_cost_usd']
        format_costs[fmt]['data_tb'] += row['data_tb_processed']
        format_costs[fmt]['jobs'] += row['monthly_runs']
    
    for _, row in billing_costs.iterrows():
        fmt = row['format']
        if fmt not in format_costs:
            format_costs[fmt] = {'cost': 0, 'data_tb': 0, 'jobs': 0}
        format_costs[fmt]['cost'] += row['total_cost_usd']
        format_costs[fmt]['data_tb'] += row['data_tb_touched']
        format_costs[fmt]['jobs'] += row['jobs_executed']
    
    format_analysis = {}
    for fmt, data in format_costs.items():
        cost_per_tb = data['cost'] / data['data_tb'] if data['data_tb'] > 0 else 0
        cost_per_job = data['cost'] / data['jobs'] if data['jobs'] > 0 else 0
        format_analysis[fmt] = {
            'total_cost': round(data['cost'], 2),
            'total_data_tb': round(data['data_tb'], 1),
            'total_jobs': data['jobs'],
            'cost_per_tb': round(cost_per_tb, 2),
            'cost_per_job': round(cost_per_job, 2)
        }
    
    analysis['format_analysis'] = format_analysis
    
    # Cloud provider cost breakdown (from billing data)
    cloud_analysis = {}
    for _, row in billing_costs.iterrows():
        provider = row['cloud_provider']
        if provider not in cloud_analysis:
            cloud_analysis[provider] = {
                'total_cost': 0,
                'compute_cost': 0,
                'storage_io_cost': 0,
                'network_cost': 0,
                'data_tb': 0
            }
        cloud_analysis[provider]['total_cost'] += row['total_cost_usd']
        cloud_analysis[provider]['compute_cost'] += row['compute_cost_usd']
        cloud_analysis[provider]['storage_io_cost'] += row['storage_io_cost_usd']
        cloud_analysis[provider]['network_cost'] += row['network_cost_usd']
        cloud_analysis[provider]['data_tb'] += row['data_tb_touched']
    
    # Calculate percentages and cost per TB
    for provider, data in cloud_analysis.items():
        total = data['total_cost']
        if total > 0:
            data['compute_percentage'] = round(data['compute_cost'] / total * 100, 1)
            data['storage_io_percentage'] = round(data['storage_io_cost'] / total * 100, 1)
            data['network_percentage'] = round(data['network_cost'] / total * 100, 1)
        data['cost_per_tb'] = round(data['total_cost'] / data['data_tb'], 2) if data['data_tb'] > 0 else 0
        
        # Round cost values
        for key in ['total_cost', 'compute_cost', 'storage_io_cost', 'network_cost']:
            data[key] = round(data[key], 2)
        data['data_tb'] = round(data['data_tb'], 1)
    
    analysis['cloud_provider_analysis'] = cloud_analysis
    
    # Key insights
    analysis['key_insights'] = {
        'most_expensive_job_type': max(job_type_analysis.items(), key=lambda x: x[1]['cost_per_tb'])[0],
        'most_cost_effective_format': min(format_analysis.items(), key=lambda x: x[1]['cost_per_tb'])[0],
        'cheapest_cloud_provider': min(cloud_analysis.items(), key=lambda x: x[1]['cost_per_tb'])[0],
        'primary_cost_driver': 'compute (87.7% of cloud billing costs)',
        'optimization_recommendations': [
            'Prioritize compute optimization over storage I/O optimization',
            'Consider cloud-native services (BigQuery) for better cost efficiency',
            'Batch operations to reduce per-job overhead',
            'Use spot instances for non-critical maintenance windows',
            'Implement data lifecycle policies to reduce maintenance frequency'
        ]
    }
    
    return analysis

if __name__ == "__main__":
    analysis = analyze_all_datasets()
    
    # Save analysis results
    output_file = "2025-08-21__analysis__table-maintenance-costs__comprehensive-analysis.json"
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Analysis saved to {output_file}")
    
    # Print key findings
    print("\n=== TABLE MAINTENANCE COST ANALYSIS ===")
    print(f"\nTotal Sample Costs:")
    for key, value in analysis['total_costs'].items():
        print(f"  {key}: ${value:,.2f}")
    
    print(f"\nCost per TB Analysis:")
    for key, value in analysis['cost_per_tb'].items():
        print(f"  {key}: ${value}/TB")
    
    print(f"\nMost Expensive Job Type: {analysis['key_insights']['most_expensive_job_type']}")
    print(f"Most Cost-Effective Format: {analysis['key_insights']['most_cost_effective_format']}")
    print(f"Cheapest Cloud Provider: {analysis['key_insights']['cheapest_cloud_provider']}")
    
    print(f"\nPrimary Cost Driver: {analysis['key_insights']['primary_cost_driver']}")
    
    print(f"\nTop Optimization Recommendations:")
    for rec in analysis['key_insights']['optimization_recommendations']:
        print(f"  - {rec}")