#!/usr/bin/env python3
"""
Cross-Border Data Compliance Cost Collector
Focuses specifically on cross-border data governance requirements
and their associated costs and complexity
"""

import csv
import json
from datetime import datetime

def collect_cross_border_scenarios():
    """Collect cross-border compliance cost scenarios"""
    scenarios = []
    
    # Major cross-border compliance scenarios
    compliance_routes = [
        {
            "route": "US-EU", 
            "primary": "us-east-1", 
            "replica": "eu-west-1",
            "regulations": ["GDPR", "CCPA"],
            "base_latency": 120,
            "complexity_multiplier": 2.5
        },
        {
            "route": "EU-APAC", 
            "primary": "eu-west-1", 
            "replica": "ap-southeast-1",
            "regulations": ["GDPR", "PDPA"],
            "base_latency": 180,
            "complexity_multiplier": 3.0
        },
        {
            "route": "US-APAC", 
            "primary": "us-west-2", 
            "replica": "ap-northeast-1",
            "regulations": ["CCPA", "PIPEDA"],
            "base_latency": 150,
            "complexity_multiplier": 2.2
        },
        {
            "route": "EU-UK", 
            "primary": "eu-central-1", 
            "replica": "uk-west-1",
            "regulations": ["GDPR", "UK-DPA"],
            "base_latency": 45,
            "complexity_multiplier": 1.8
        },
        {
            "route": "US-CANADA", 
            "primary": "us-east-1", 
            "replica": "ca-central-1",
            "regulations": ["CCPA", "PIPEDA"],
            "base_latency": 35,
            "complexity_multiplier": 1.5
        },
        {
            "route": "EU-SWITZERLAND", 
            "primary": "eu-west-3", 
            "replica": "ch-central-1",
            "regulations": ["GDPR", "nDSG"],
            "base_latency": 25,
            "complexity_multiplier": 2.8
        }
    ]
    
    # Data types with different compliance requirements
    data_types = [
        {"type": "PII", "cost_multiplier": 3.5, "policy_multiplier": 4},
        {"type": "Financial", "cost_multiplier": 4.2, "policy_multiplier": 5},
        {"type": "Healthcare", "cost_multiplier": 5.1, "policy_multiplier": 6},
        {"type": "Generic", "cost_multiplier": 1.0, "policy_multiplier": 1}
    ]
    
    # Stack types for cross-border scenarios
    stack_types = [
        {
            "name": "Sync Replication + Encryption",
            "base_cost_per_gb": 0.15,
            "governance_overhead": 0.35
        },
        {
            "name": "Async Replication + Policy Engine", 
            "base_cost_per_gb": 0.08,
            "governance_overhead": 0.25
        },
        {
            "name": "Event Sourcing + Audit Trail",
            "base_cost_per_gb": 0.22,
            "governance_overhead": 0.45
        },
        {
            "name": "Zero-Trust Multi-Region",
            "base_cost_per_gb": 0.35,
            "governance_overhead": 0.60
        }
    ]
    
    for route in compliance_routes:
        for data_type in data_types:
            for stack in stack_types:
                for gb_replicated in [500, 2500, 10000, 50000, 250000]:
                    # Base replication cost
                    base_cost = gb_replicated * stack["base_cost_per_gb"]
                    
                    # Apply data type multiplier
                    adjusted_cost = base_cost * data_type["cost_multiplier"]
                    
                    # Apply route complexity multiplier
                    route_cost = adjusted_cost * route["complexity_multiplier"]
                    
                    # Add governance overhead
                    governance_cost = route_cost * stack["governance_overhead"]
                    total_monthly_cost = route_cost + governance_cost
                    
                    # Calculate policy objects
                    base_policies = max(20, gb_replicated // 2500)
                    policy_objects = base_policies * data_type["policy_multiplier"] * len(route["regulations"])
                    
                    # Compliance tier based on data type and regulations
                    if data_type["type"] in ["PII", "Financial", "Healthcare"]:
                        compliance_tier = "Strict"
                    else:
                        compliance_tier = "Standard"
                    
                    # Governance complexity
                    if len(route["regulations"]) > 2 and data_type["type"] != "Generic":
                        complexity = "Very High"
                    elif len(route["regulations"]) > 1:
                        complexity = "High"
                    else:
                        complexity = "Medium"
                    
                    scenarios.append({
                        "provider": "Multi-Cloud Cross-Border",
                        "primary_region": route["primary"],
                        "replica_region": route["replica"],
                        "stack_type": f"{stack['name']} ({data_type['type']})",
                        "gb_replicated": gb_replicated,
                        "policy_objects": policy_objects,
                        "monthly_cost_usd": round(total_monthly_cost, 2),
                        "governance_complexity": complexity,
                        "compliance_tier": compliance_tier,
                        "data_sovereignty": "Cross-Border",
                        "regulations": "/".join(route["regulations"]),
                        "route": route["route"],
                        "latency_ms": route["base_latency"],
                        "data_type": data_type["type"]
                    })
    
    return scenarios

def collect_regulatory_penalty_costs():
    """Collect regulatory penalty and non-compliance cost data"""
    penalty_scenarios = []
    
    # Major regulations and their penalty structures
    regulations = [
        {
            "name": "GDPR",
            "max_penalty_pct": 4.0,  # 4% of annual revenue
            "base_penalty": 20000000,  # €20M
            "regions": ["EU", "UK"]
        },
        {
            "name": "CCPA", 
            "max_penalty_pct": 0.1,  # Per violation penalties
            "base_penalty": 7500,  # $7,500 per violation
            "regions": ["California"]
        },
        {
            "name": "PIPEDA",
            "max_penalty_pct": 0.0,
            "base_penalty": 100000,  # CAD $100K
            "regions": ["Canada"]
        }
    ]
    
    # Company revenue tiers for penalty calculation
    revenue_tiers = [
        {"tier": "Startup", "annual_revenue": 5000000},
        {"tier": "SMB", "annual_revenue": 50000000}, 
        {"tier": "Enterprise", "annual_revenue": 1000000000},
        {"tier": "Fortune500", "annual_revenue": 10000000000}
    ]
    
    for regulation in regulations:
        for tier in revenue_tiers:
            for gb_replicated in [1000, 10000, 100000]:
                # Calculate potential penalty
                revenue_penalty = tier["annual_revenue"] * (regulation["max_penalty_pct"] / 100)
                max_penalty = max(regulation["base_penalty"], revenue_penalty)
                
                # Probability of violation increases with data volume and complexity
                violation_probability = min(0.15, (gb_replicated / 500000) * 0.1 + 0.02)
                
                # Expected annual penalty cost
                expected_penalty = max_penalty * violation_probability
                
                # Monthly prevention cost (usually 10-20% of expected penalty)
                prevention_cost = expected_penalty * 0.15 / 12
                
                # Policy objects for compliance
                policy_objects = max(50, gb_replicated // 1000)
                
                penalty_scenarios.append({
                    "provider": "Compliance Prevention",
                    "primary_region": "multi-region",
                    "replica_region": regulation["regions"][0] if regulation["regions"] else "global",
                    "stack_type": f"{regulation['name']} Prevention ({tier['tier']})",
                    "gb_replicated": gb_replicated,
                    "policy_objects": policy_objects,
                    "monthly_cost_usd": round(prevention_cost, 2),
                    "governance_complexity": "Very High",
                    "compliance_tier": "Prevention",
                    "data_sovereignty": "Mandatory",
                    "max_penalty_usd": round(max_penalty, 2),
                    "expected_annual_penalty": round(expected_penalty, 2),
                    "violation_probability": round(violation_probability * 100, 2)
                })
    
    return penalty_scenarios

def main():
    print("Collecting cross-border compliance cost data...")
    
    # Collect data
    cross_border_data = collect_cross_border_scenarios()
    penalty_data = collect_regulatory_penalty_costs()
    
    all_data = cross_border_data + penalty_data
    
    print(f"Collected {len(all_data)} cross-border compliance scenarios")
    
    # Save main dataset
    filename = "2025-08-21__data__cross-border-governance__compliance__regulatory-costs.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        if all_data:
            fieldnames = all_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
    
    print(f"Cross-border compliance data saved to {filename}")
    
    # Summary statistics
    costs = [row['monthly_cost_usd'] for row in all_data]
    print(f"\nCross-Border Compliance Cost Summary:")
    print(f"Records: {len(all_data)}")
    print(f"Cost range: ${min(costs):.2f} - ${max(costs):,.2f}")
    print(f"Average monthly cost: ${sum(costs)/len(costs):,.2f}")
    
    return filename

if __name__ == "__main__":
    main()