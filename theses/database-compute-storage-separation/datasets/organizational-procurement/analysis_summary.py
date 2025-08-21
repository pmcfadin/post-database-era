#!/usr/bin/env python3
"""
Analysis Summary for Organizational and Procurement Datasets
Extracts key insights and trends from the collected data
"""

import csv
import json
from collections import defaultdict, Counter

def analyze_finops_patterns():
    """Analyze FinOps budget allocation patterns"""
    
    with open('2025-08-21__data__finops-budget-allocation__framework__models.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print("=== FinOps Budget Allocation Analysis ===")
    
    # Budget model distribution
    budget_models = Counter(row['budget_model'] for row in data)
    print(f"Budget Models: {dict(budget_models)}")
    
    # Compute vs Storage allocation independence
    independent_compute = sum(1 for row in data if 'based' in row['compute_allocation_method'])
    independent_storage = sum(1 for row in data if 'based' in row['storage_allocation_method'])
    
    print(f"Independent Compute Allocation: {independent_compute}/{len(data)} organizations")
    print(f"Independent Storage Allocation: {independent_storage}/{len(data)} organizations")
    
    # Reserved instance patterns
    reserved_percentages = [int(row['reserved_instance_policy'].split('_')[0]) for row in data]
    avg_reserved = sum(reserved_percentages) / len(reserved_percentages)
    print(f"Average Reserved Instance Usage: {avg_reserved:.1f}%")
    
    return {
        'budget_models': budget_models,
        'independent_allocation_rate': (independent_compute + independent_storage) / (2 * len(data)),
        'avg_reserved_usage': avg_reserved
    }

def analyze_contract_independence():
    """Analyze contract structure for compute/storage independence"""
    
    with open('2025-08-21__data__enterprise-contracts__database__compute-storage-terms.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print("\n=== Contract Independence Analysis ===")
    
    # Pricing independence
    compute_independent = sum(1 for row in data if row['compute_pricing_independence'] == 'yes')
    storage_independent = sum(1 for row in data if row['storage_pricing_independence'] == 'yes')
    
    print(f"Compute Pricing Independence: {compute_independent}/{len(data)} vendors")
    print(f"Storage Pricing Independence: {storage_independent}/{len(data)} vendors")
    
    # Minimum commitments
    compute_commits = [int(row['min_commit_compute_usd']) for row in data if row['min_commit_compute_usd'].isdigit()]
    storage_commits = [int(row['min_commit_storage_usd']) for row in data if row['min_commit_storage_usd'].isdigit()]
    
    if compute_commits:
        avg_compute_commit = sum(compute_commits) / len(compute_commits)
        print(f"Average Compute Commitment: ${avg_compute_commit:,.0f}")
    
    if storage_commits:
        avg_storage_commit = sum(storage_commits) / len(storage_commits)
        print(f"Average Storage Commitment: ${avg_storage_commit:,.0f}")
    
    # Auto-scaling rights
    auto_scaling = Counter(row['auto_scaling_rights'] for row in data)
    print(f"Auto-scaling Rights: {dict(auto_scaling)}")
    
    return {
        'compute_independence_rate': compute_independent / len(data),
        'storage_independence_rate': storage_independent / len(data),
        'avg_compute_commit': avg_compute_commit if compute_commits else 0,
        'avg_storage_commit': avg_storage_commit if storage_commits else 0,
        'auto_scaling_distribution': auto_scaling
    }

def analyze_organizational_evolution():
    """Analyze organizational structure evolution patterns"""
    
    with open('2025-08-21__data__organizational-structure__teams__cloud-center-excellence.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print("\n=== Organizational Evolution Analysis ===")
    
    # CCOE maturity by company size
    size_maturity = defaultdict(list)
    for row in data:
        size_maturity[row['company_size']].append(row['ccoe_maturity'])
    
    print("CCOE Maturity by Company Size:")
    for size, maturities in size_maturity.items():
        maturity_counts = Counter(maturities)
        print(f"  {size}: {dict(maturity_counts)}")
    
    # Storage vs Compute ownership separation
    storage_owners = Counter(row['storage_ops_ownership'] for row in data)
    compute_owners = Counter(row['compute_ops_ownership'] for row in data)
    
    separated_ownership = sum(1 for row in data 
                            if row['storage_ops_ownership'] != row['compute_ops_ownership'])
    
    print(f"Separated Storage/Compute Ownership: {separated_ownership}/{len(data)} organizations")
    
    # Platform engineering adoption
    platform_adoption = Counter(row['platform_engineering_adoption'] for row in data)
    print(f"Platform Engineering Adoption: {dict(platform_adoption)}")
    
    return {
        'separated_ownership_rate': separated_ownership / len(data),
        'platform_adoption_distribution': platform_adoption,
        'size_maturity_correlation': dict(size_maturity)
    }

def analyze_database_pricing_patterns():
    """Analyze database workload pricing patterns"""
    
    with open('2025-08-21__data__database-pricing__reserved-spot__usage-patterns.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    print("\n=== Database Pricing Pattern Analysis ===")
    
    # Reserved vs Spot usage by workload criticality
    criticality_patterns = defaultdict(list)
    for row in data:
        criticality = row['business_criticality']
        reserved_pct = int(row['reserved_compute_percent'])
        spot_pct = int(row['spot_compute_percent'])
        criticality_patterns[criticality].append((reserved_pct, spot_pct))
    
    print("Reserved/Spot Usage by Business Criticality:")
    for criticality, patterns in criticality_patterns.items():
        avg_reserved = sum(p[0] for p in patterns) / len(patterns)
        avg_spot = sum(p[1] for p in patterns) / len(patterns)
        print(f"  {criticality}: {avg_reserved:.1f}% reserved, {avg_spot:.1f}% spot")
    
    # Cost savings distribution
    cost_savings = [int(row['cost_savings_percent']) for row in data]
    avg_savings = sum(cost_savings) / len(cost_savings)
    print(f"Average Cost Savings: {avg_savings:.1f}%")
    
    # Workload suitability for separation
    high_spot_workloads = [row['workload_type'] for row in data 
                          if int(row['spot_compute_percent']) > 40]
    print(f"High Spot Usage Workloads (>40%): {high_spot_workloads}")
    
    return {
        'criticality_patterns': dict(criticality_patterns),
        'avg_cost_savings': avg_savings,
        'high_spot_workloads': high_spot_workloads
    }

def main():
    """Main analysis function"""
    
    print("Organizational and Procurement Data Analysis")
    print("=" * 50)
    
    finops_insights = analyze_finops_patterns()
    contract_insights = analyze_contract_independence()
    org_insights = analyze_organizational_evolution()
    pricing_insights = analyze_database_pricing_patterns()
    
    # Summary insights
    print("\n=== KEY INSIGHTS SUMMARY ===")
    print(f"1. FinOps Independence: {finops_insights['independent_allocation_rate']:.1%} of organizations use independent compute/storage allocation")
    print(f"2. Contract Evolution: {contract_insights['compute_independence_rate']:.1%} of vendors offer independent compute pricing")
    print(f"3. Organizational Separation: {org_insights['separated_ownership_rate']:.1%} of organizations separate compute/storage ownership")
    print(f"4. Cost Optimization: {pricing_insights['avg_cost_savings']:.1f}% average cost savings from optimized pricing strategies")
    
    # Evidence for thesis
    print(f"\n=== THESIS EVIDENCE ===")
    separation_indicators = [
        finops_insights['independent_allocation_rate'],
        contract_insights['compute_independence_rate'],
        contract_insights['storage_independence_rate'],
        org_insights['separated_ownership_rate']
    ]
    
    avg_separation_adoption = sum(separation_indicators) / len(separation_indicators)
    print(f"Average Separation Adoption Rate: {avg_separation_adoption:.1%}")
    
    if avg_separation_adoption > 0.5:
        print("✓ Data supports thesis: Organizations are adopting separated compute/storage models")
    else:
        print("⚠ Data suggests separation adoption is still emerging")

if __name__ == "__main__":
    main()