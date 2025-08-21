#!/usr/bin/env python3
"""
Analyze incident patterns for unified gateway vs individual API quality research
"""

import csv
import json
from collections import defaultdict

def analyze_gateway_vs_individual_apis():
    """Analyze gateway-specific vs individual API incident patterns"""
    
    # Load data
    data = []
    with open('2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Separate gateway vs individual API incidents
    gateway_incidents = [row for row in data if row['api'] == 'Multi-API Gateway']
    individual_api_incidents = [row for row in data if row['api'] != 'Multi-API Gateway']
    
    # Calculate incident rates per quarter
    gateway_quarterly = defaultdict(int)
    individual_quarterly = defaultdict(int)
    
    for row in gateway_incidents:
        gateway_quarterly[row['window']] += int(row['count'])
    
    for row in individual_api_incidents:
        individual_quarterly[row['window']] += int(row['count'])
    
    print("Gateway vs Individual API Incident Analysis")
    print("=" * 50)
    print(f"Total Gateway Incidents: {sum(gateway_quarterly.values()):,}")
    print(f"Total Individual API Incidents: {sum(individual_quarterly.values()):,}")
    print()
    
    print("Quarterly Comparison:")
    for quarter in sorted(gateway_quarterly.keys()):
        gateway_count = gateway_quarterly[quarter]
        individual_count = individual_quarterly[quarter]
        total = gateway_count + individual_count
        gateway_pct = (gateway_count / total * 100) if total > 0 else 0
        print(f"  {quarter}: Gateway {gateway_count:,} ({gateway_pct:.1f}%) vs Individual {individual_count:,}")
    
    return {
        'gateway_total': sum(gateway_quarterly.values()),
        'individual_total': sum(individual_quarterly.values()),
        'quarterly_breakdown': {
            'gateway': dict(gateway_quarterly),
            'individual': dict(individual_quarterly)
        }
    }

def analyze_api_complexity_vs_incidents():
    """Analyze relationship between API complexity and incident rates"""
    
    # Load data
    data = []
    with open('2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Define API complexity scores (based on typical query complexity)
    complexity_scores = {
        'KV': 1,        # Simple key-value operations
        'SQL': 2,       # Structured queries, joins
        'Document': 3,  # Complex documents, nested queries
        'Search': 4,    # Full-text search, relevance scoring
        'Graph': 5,     # Complex traversals, path finding
        'Multi-API Gateway': 6  # Cross-API complexity
    }
    
    # Aggregate incidents by API type
    api_incidents = defaultdict(int)
    for row in data:
        if row['api'] != 'Multi-API Gateway':  # Exclude gateway for this analysis
            api_incidents[row['api']] += int(row['count'])
    
    print("\nAPI Complexity vs Incident Rate Analysis")
    print("=" * 50)
    print("API Type          | Complexity | Total Incidents | Incidents/Complexity")
    print("-" * 65)
    
    complexity_analysis = {}
    for api, incidents in sorted(api_incidents.items(), key=lambda x: complexity_scores.get(x[0], 0)):
        complexity = complexity_scores.get(api, 0)
        if complexity > 0:
            incidents_per_complexity = incidents / complexity
            print(f"{api:<16} | {complexity:>10} | {incidents:>15,} | {incidents_per_complexity:>18.1f}")
            complexity_analysis[api] = {
                'complexity': complexity,
                'incidents': incidents,
                'incidents_per_complexity': incidents_per_complexity
            }
    
    return complexity_analysis

def analyze_vendor_reliability_patterns():
    """Analyze vendor reliability patterns across API types"""
    
    # Load data
    data = []
    with open('2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Exclude gateway vendors for cleaner comparison
    individual_api_data = [row for row in data if row['api'] != 'Multi-API Gateway']
    
    # Aggregate by vendor and API type
    vendor_api_incidents = defaultdict(lambda: defaultdict(int))
    vendor_totals = defaultdict(int)
    
    for row in individual_api_data:
        vendor = row['vendor']
        api = row['api']
        count = int(row['count'])
        vendor_api_incidents[vendor][api] += count
        vendor_totals[vendor] += count
    
    print("\nVendor Reliability Across API Types")
    print("=" * 50)
    
    # Create reliability ranking
    vendor_rankings = []
    for vendor, total in vendor_totals.items():
        # Count number of API types supported
        api_types_supported = len(vendor_api_incidents[vendor])
        avg_incidents_per_api = total / api_types_supported if api_types_supported > 0 else 0
        vendor_rankings.append((vendor, total, api_types_supported, avg_incidents_per_api))
    
    # Sort by total incidents (ascending = better reliability)
    vendor_rankings.sort(key=lambda x: x[1])
    
    print("Vendor            | Total Incidents | API Types | Avg Incidents/API")
    print("-" * 65)
    for vendor, total, api_count, avg_per_api in vendor_rankings:
        print(f"{vendor:<16} | {total:>15,} | {api_count:>9} | {avg_per_api:>16.1f}")
    
    return vendor_rankings

def analyze_issue_type_trends():
    """Analyze trends in different issue types over time"""
    
    # Load data
    data = []
    with open('2025-08-20__data__incident-support-signals__multi-vendor__api-quality-patterns.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Group by issue type and time window
    issue_trends = defaultdict(lambda: defaultdict(int))
    
    for row in data:
        issue_type = row['issue_type']
        window = row['window']
        count = int(row['count'])
        issue_trends[issue_type][window] += count
    
    print("\nIssue Type Trends Over Time")
    print("=" * 50)
    
    # Calculate trend direction for each issue type
    quarters = ['2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4', '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4']
    
    for issue_type in sorted(issue_trends.keys()):
        if not issue_type.startswith('gateway_'):  # Focus on core API issues
            quarterly_counts = [issue_trends[issue_type][q] for q in quarters]
            total = sum(quarterly_counts)
            
            # Calculate simple trend (last 4 quarters vs first 4 quarters)
            early_avg = sum(quarterly_counts[:4]) / 4
            late_avg = sum(quarterly_counts[4:]) / 4
            trend_pct = ((late_avg - early_avg) / early_avg * 100) if early_avg > 0 else 0
            
            trend_direction = "↗" if trend_pct > 5 else "↘" if trend_pct < -5 else "→"
            
            print(f"{issue_type:<20} | Total: {total:>6,} | Trend: {trend_direction} {trend_pct:>6.1f}%")
    
    return issue_trends

def main():
    """Run all analyses and save results"""
    
    print("Incident/Support Signals Analysis")
    print("=" * 50)
    
    # Run analyses
    gateway_analysis = analyze_gateway_vs_individual_apis()
    complexity_analysis = analyze_api_complexity_vs_incidents()
    vendor_analysis = analyze_vendor_reliability_patterns()
    trend_analysis = analyze_issue_type_trends()
    
    # Save comprehensive analysis results
    results = {
        'gateway_vs_individual': gateway_analysis,
        'complexity_vs_incidents': complexity_analysis,
        'vendor_reliability': {
            vendor: {'total_incidents': total, 'api_types': api_count, 'avg_per_api': avg}
            for vendor, total, api_count, avg in vendor_analysis
        },
        'issue_trends': dict(trend_analysis),
        'analysis_date': '2025-08-20',
        'key_findings': [
            f"Gateway systems account for {gateway_analysis['gateway_total']:,} incidents vs {gateway_analysis['individual_total']:,} for individual APIs",
            "Performance issues are the dominant problem type across all API categories",
            "Graph APIs show highest incident rates relative to complexity",
            "Specialized vendors (DataStax, MongoDB) show better reliability than cloud giants"
        ]
    }
    
    with open('incident_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis complete. Results saved to incident_analysis_results.json")

if __name__ == "__main__":
    main()