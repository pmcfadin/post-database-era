#!/usr/bin/env python3
"""
Generate remaining compute utilization datasets
"""

import csv
import random
from datetime import datetime

def create_case_studies():
    """Generate cost optimization case studies"""
    studies = []
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    scenarios = [
        ('database_consolidation', 'cluster', 'serverless', 'variable', 35, 65, 40, 80),
        ('right_sizing_clusters', 'cluster', 'cluster', 'predictable', 20, 45, 25, 50),
        ('hybrid_deployment', 'cluster', 'hybrid', 'mixed', 25, 55, 30, 60)
    ]
    
    for scenario, before, after, pattern, cost_min, cost_max, util_min, util_max in scenarios:
        for i in range(5):
            study = {
                'case_study_id': f"{scenario}_{i+1}",
                'company_size': random.choice(['startup', 'mid_market', 'enterprise']),
                'industry': random.choice(['fintech', 'ecommerce', 'saas', 'media', 'healthcare']),
                'before_deployment': before,
                'after_deployment': after,
                'workload_pattern': pattern,
                'before_cpu_util_avg': round(random.uniform(15, 35), 1),
                'after_cpu_util_avg': round(random.uniform(60, 90), 1),
                'before_idle_pct': round(random.uniform(65, 85), 1),
                'after_idle_pct': round(random.uniform(10, 40), 1),
                'cost_reduction_pct': round(random.uniform(cost_min, cost_max), 1),
                'implementation_weeks': random.randint(2, 12),
                'roi_months': random.randint(1, 6)
            }
            studies.append(study)
    
    filename = f'{timestamp}__data__compute-utilization__case-studies__optimization-outcomes.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=studies[0].keys())
        writer.writeheader()
        writer.writerows(studies)
    
    print(f"Created {filename} with {len(studies)} records")
    return filename

def create_autoscaler_data():
    """Generate autoscaler efficiency metrics"""
    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    autoscaler_types = [
        "horizontal_pod_autoscaler", "vertical_pod_autoscaler", 
        "cluster_autoscaler", "serverless_autoscaler"
    ]
    
    for autoscaler in autoscaler_types:
        for i in range(8):
            record = {
                'autoscaler_type': autoscaler,
                'engine': random.choice(['PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch']),
                'trigger_metric': random.choice(['cpu', 'memory', 'custom_metric', 'queue_length']),
                'scale_up_threshold': round(random.uniform(60, 80), 1),
                'scale_down_threshold': round(random.uniform(20, 40), 1),
                'avg_scale_events_day': random.randint(5, 200),
                'scale_accuracy_pct': round(random.uniform(70, 95), 1),
                'false_positive_rate': round(random.uniform(5, 25), 1),
                'response_time_seconds': round(random.uniform(10, 300), 1),
                'cpu_util_improvement': round(random.uniform(15, 50), 1),
                'cost_savings_pct': round(random.uniform(10, 40), 1)
            }
            data.append(record)
    
    filename = f'{timestamp}__data__compute-utilization__autoscaler__efficiency-metrics.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Created {filename} with {len(data)} records")
    return filename

def main():
    case_studies_file = create_case_studies()
    autoscaler_file = create_autoscaler_data()
    
    print("All remaining datasets created successfully!")
    return case_studies_file, autoscaler_file

if __name__ == "__main__":
    main()