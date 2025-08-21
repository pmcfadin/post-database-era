#!/usr/bin/env python3
"""
Performance Data Analysis
Generates summary statistics and insights from collected performance data
"""

import csv
import json
import statistics
from collections import defaultdict, Counter
from datetime import datetime

def analyze_performance_data(csv_filename):
    """Analyze the performance benchmark data"""
    
    # Read the data
    data = []
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    
    # Convert numeric fields
    for row in data:
        row['p50_ms'] = float(row['p50_ms'])
        row['p95_ms'] = float(row['p95_ms'])
        row['p99_ms'] = float(row['p99_ms'])
        row['qps_peak'] = float(row['qps_peak'])
    
    # Analysis results
    analysis = {
        'dataset_summary': {
            'total_records': len(data),
            'engines_count': len(set(row['engine'] for row in data)),
            'workload_types': len(set(row['workload'] for row in data)),
            'unique_engines': list(set(row['engine'] for row in data)),
            'workload_distribution': dict(Counter(row['workload'] for row in data))
        },
        'latency_analysis': {},
        'throughput_analysis': {},
        'workload_performance': {},
        'engine_rankings': {}
    }
    
    # Latency analysis by percentile
    all_p50 = [row['p50_ms'] for row in data]
    all_p95 = [row['p95_ms'] for row in data]
    all_p99 = [row['p99_ms'] for row in data]
    
    analysis['latency_analysis'] = {
        'p50_stats': {
            'min': min(all_p50),
            'max': max(all_p50),
            'median': statistics.median(all_p50),
            'mean': round(statistics.mean(all_p50), 1)
        },
        'p95_stats': {
            'min': min(all_p95),
            'max': max(all_p95),
            'median': statistics.median(all_p95),
            'mean': round(statistics.mean(all_p95), 1)
        },
        'p99_stats': {
            'min': min(all_p99),
            'max': max(all_p99),
            'median': statistics.median(all_p99),
            'mean': round(statistics.mean(all_p99), 1)
        }
    }
    
    # Throughput analysis
    all_qps = [row['qps_peak'] for row in data]
    analysis['throughput_analysis'] = {
        'qps_stats': {
            'min': min(all_qps),
            'max': max(all_qps),
            'median': statistics.median(all_qps),
            'mean': round(statistics.mean(all_qps), 1)
        }
    }
    
    # Performance by workload type
    workload_groups = defaultdict(list)
    for row in data:
        workload_groups[row['workload']].append(row)
    
    for workload, rows in workload_groups.items():
        p95_values = [row['p95_ms'] for row in rows]
        qps_values = [row['qps_peak'] for row in rows]
        
        analysis['workload_performance'][workload] = {
            'count': len(rows),
            'avg_p95_latency': round(statistics.mean(p95_values), 1),
            'median_p95_latency': statistics.median(p95_values),
            'avg_qps_peak': round(statistics.mean(qps_values), 1),
            'engines': list(set(row['engine'] for row in rows))
        }
    
    # Engine rankings (by P95 latency for BI workloads)
    bi_data = [row for row in data if row['workload'] == 'BI']
    if bi_data:
        bi_rankings = sorted(bi_data, key=lambda x: x['p95_ms'])
        analysis['engine_rankings']['bi_latency_leaders'] = [
            {
                'engine': row['engine'],
                'p95_ms': row['p95_ms'],
                'qps_peak': row['qps_peak'],
                'source': row['source']
            }
            for row in bi_rankings[:5]  # Top 5
        ]
    
    # QPS leaders across all workloads
    qps_rankings = sorted(data, key=lambda x: x['qps_peak'], reverse=True)
    analysis['engine_rankings']['qps_leaders'] = [
        {
            'engine': row['engine'],
            'workload': row['workload'],
            'qps_peak': row['qps_peak'],
            'p95_ms': row['p95_ms']
        }
        for row in qps_rankings[:5]  # Top 5
    ]
    
    return analysis

def print_analysis_summary(analysis):
    """Print human-readable analysis summary"""
    
    print("\\n=== PERFORMANCE BENCHMARK ANALYSIS ===\\n")
    
    print(f"Dataset Overview:")
    print(f"- Total records: {analysis['dataset_summary']['total_records']}")
    print(f"- Engines covered: {analysis['dataset_summary']['engines_count']}")
    print(f"- Workload types: {analysis['dataset_summary']['workload_types']}")
    print(f"- Workload distribution: {analysis['dataset_summary']['workload_distribution']}")
    
    print(f"\\nLatency Analysis (P95):")
    p95_stats = analysis['latency_analysis']['p95_stats']
    print(f"- Range: {p95_stats['min']}ms - {p95_stats['max']}ms")
    print(f"- Median: {p95_stats['median']}ms")
    print(f"- Average: {p95_stats['mean']}ms")
    
    print(f"\\nThroughput Analysis:")
    qps_stats = analysis['throughput_analysis']['qps_stats']
    print(f"- QPS Range: {qps_stats['min']} - {qps_stats['max']}")
    print(f"- Median QPS: {qps_stats['median']}")
    print(f"- Average QPS: {qps_stats['mean']}")
    
    print(f"\\nPerformance by Workload:")
    for workload, stats in analysis['workload_performance'].items():
        print(f"- {workload}: Avg P95={stats['avg_p95_latency']}ms, Avg QPS={stats['avg_qps_peak']}")
    
    print(f"\\nTop BI Latency Performers:")
    if 'bi_latency_leaders' in analysis['engine_rankings']:
        for i, engine in enumerate(analysis['engine_rankings']['bi_latency_leaders'][:3], 1):
            print(f"{i}. {engine['engine']}: {engine['p95_ms']}ms P95, {engine['qps_peak']} QPS")
    
    print(f"\\nTop Throughput Performers:")
    for i, engine in enumerate(analysis['engine_rankings']['qps_leaders'][:3], 1):
        print(f"{i}. {engine['engine']} ({engine['workload']}): {engine['qps_peak']} QPS")

if __name__ == "__main__":
    csv_file = "datasets/2025-08-20__data__query-performance__multi-engine__latency-throughput.csv"
    
    # Run analysis
    results = analyze_performance_data(csv_file)
    
    # Print summary
    print_analysis_summary(results)
    
    # Save detailed analysis
    timestamp = datetime.now().strftime('%Y-%m-%d')
    analysis_file = f"datasets/{timestamp}__analysis__query-performance__statistical-summary.json"
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\\nDetailed analysis saved to: {analysis_file}")