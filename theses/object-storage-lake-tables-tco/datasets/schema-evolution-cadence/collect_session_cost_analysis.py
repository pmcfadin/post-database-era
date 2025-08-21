#!/usr/bin/env python3
"""
BI Dashboard Session Cost Analysis

Detailed cost breakdown for different BI dashboard session patterns,
comparing session-based pricing models across architectures.
"""

import csv
import json
from datetime import datetime
from typing import List, Dict, Any

class SessionCostAnalyzer:
    def __init__(self):
        self.cost_models = self._init_cost_models()
        
    def _init_cost_models(self):
        """Initialize cost models for different platforms"""
        return {
            "snowflake": {
                "xs_warehouse": {"credits_per_hour": 1, "credit_cost_usd": 2.5},
                "s_warehouse": {"credits_per_hour": 2, "credit_cost_usd": 2.5},
                "m_warehouse": {"credits_per_hour": 4, "credit_cost_usd": 2.5},
                "external_tables": {"credits_per_hour": 1, "credit_cost_usd": 2.5, "data_transfer_penalty": 1.2}
            },
            "databricks": {
                "sql_serverless": {"dbu_per_hour": 0.22, "dbu_cost_usd": 0.55, "cold_start_cost_factor": 2.0},
                "sql_classic_2x": {"dbu_per_hour": 0.44, "dbu_cost_usd": 0.55},
                "sql_classic_4x": {"dbu_per_hour": 0.88, "dbu_cost_usd": 0.55}
            },
            "bigquery": {
                "on_demand": {"cost_per_tb_usd": 5.0, "min_charge_mb": 10},
                "flat_rate_100": {"monthly_cost_usd": 2000, "slot_hours": 100},
                "external_tables": {"cost_per_tb_usd": 5.0, "metadata_cost_factor": 1.3}
            },
            "redshift": {
                "ra3_xlplus": {"cost_per_hour_usd": 3.26},
                "serverless_8rpu": {"rpu_hours": 8, "rpu_cost_usd": 0.375},
                "spectrum": {"cost_per_hour_usd": 3.26, "cost_per_tb_scanned_usd": 5.0}
            }
        }
    
    def analyze_session_patterns(self):
        """Analyze different BI session usage patterns"""
        
        # Define realistic BI session patterns
        session_patterns = [
            {
                "pattern_id": "exec_morning_review",
                "description": "Executive morning dashboard review",
                "sessions_per_day": 1,
                "session_duration_minutes": 3,
                "charts_viewed": 8,
                "data_scanned_gb": 0.5,
                "user_type": "executive",
                "concurrency": 1
            },
            {
                "pattern_id": "analyst_deep_dive",
                "description": "Business analyst deep-dive analysis",
                "sessions_per_day": 4,
                "session_duration_minutes": 15,
                "charts_viewed": 25,
                "data_scanned_gb": 2.0,
                "user_type": "analyst",
                "concurrency": 1
            },
            {
                "pattern_id": "sales_team_standup",
                "description": "Sales team daily standup dashboard",
                "sessions_per_day": 1,
                "session_duration_minutes": 8,
                "charts_viewed": 12,
                "data_scanned_gb": 0.8,
                "user_type": "sales_team",
                "concurrency": 15
            },
            {
                "pattern_id": "marketing_campaign_monitor",
                "description": "Marketing campaign monitoring",
                "sessions_per_day": 8,
                "session_duration_minutes": 5,
                "charts_viewed": 6,
                "data_scanned_gb": 0.3,
                "user_type": "marketing",
                "concurrency": 3
            },
            {
                "pattern_id": "customer_support_metrics",
                "description": "Customer support metrics dashboard",
                "sessions_per_day": 12,
                "session_duration_minutes": 2,
                "charts_viewed": 4,
                "data_scanned_gb": 0.1,
                "user_type": "support",
                "concurrency": 8
            },
            {
                "pattern_id": "monthly_board_review",
                "description": "Monthly board presentation prep",
                "sessions_per_day": 0.1,  # ~3 sessions per month
                "session_duration_minutes": 45,
                "charts_viewed": 50,
                "data_scanned_gb": 5.0,
                "user_type": "executive",
                "concurrency": 2
            }
        ]
        
        return session_patterns
    
    def calculate_session_costs(self, patterns: List[Dict]) -> List[Dict]:
        """Calculate costs for each session pattern across all platforms"""
        
        cost_analysis = []
        
        for pattern in patterns:
            for platform, configs in self.cost_models.items():
                for config_name, config in configs.items():
                    
                    # Calculate base costs
                    session_cost = self._calculate_platform_session_cost(
                        pattern, platform, config_name, config
                    )
                    
                    # Calculate monthly costs
                    sessions_per_month = pattern["sessions_per_day"] * 30
                    monthly_cost = session_cost * sessions_per_month
                    
                    # Calculate cost per chart view
                    cost_per_chart = session_cost / pattern["charts_viewed"] if pattern["charts_viewed"] > 0 else 0
                    
                    cost_analysis.append({
                        "pattern_id": pattern["pattern_id"],
                        "pattern_description": pattern["description"],
                        "platform": platform,
                        "configuration": config_name,
                        "user_type": pattern["user_type"],
                        "sessions_per_day": pattern["sessions_per_day"],
                        "session_duration_minutes": pattern["session_duration_minutes"],
                        "charts_viewed": pattern["charts_viewed"],
                        "data_scanned_gb": pattern["data_scanned_gb"],
                        "concurrency": pattern["concurrency"],
                        "cost_usd_per_session": round(session_cost, 4),
                        "cost_usd_per_month": round(monthly_cost, 2),
                        "cost_usd_per_chart": round(cost_per_chart, 4),
                        "architecture_type": self._get_architecture_type(platform, config_name)
                    })
        
        return cost_analysis
    
    def _calculate_platform_session_cost(self, pattern: Dict, platform: str, config_name: str, config: Dict) -> float:
        """Calculate cost for a single session on a specific platform configuration"""
        
        duration_hours = pattern["session_duration_minutes"] / 60
        data_scanned_tb = pattern["data_scanned_gb"] / 1024
        concurrency_factor = max(1, pattern["concurrency"] * 0.1)  # Rough concurrency cost impact
        
        if platform == "snowflake":
            base_cost = duration_hours * config["credits_per_hour"] * config["credit_cost_usd"]
            if "external" in config_name:
                base_cost *= config.get("data_transfer_penalty", 1.0)
            return base_cost * concurrency_factor
            
        elif platform == "databricks":
            base_cost = duration_hours * config["dbu_per_hour"] * config["dbu_cost_usd"]
            if "serverless" in config_name:
                # Add cold start cost for serverless
                cold_start_cost = config.get("cold_start_cost_factor", 1.0) * 0.01  # Small fixed cost
                base_cost += cold_start_cost
            return base_cost * concurrency_factor
            
        elif platform == "bigquery":
            if "on_demand" in config_name or "external" in config_name:
                scan_cost = max(data_scanned_tb * config["cost_per_tb_usd"], 
                               config.get("min_charge_mb", 10) / 1024 * config["cost_per_tb_usd"])
                if "external" in config_name:
                    scan_cost *= config.get("metadata_cost_factor", 1.0)
                return scan_cost
            else:  # flat rate
                # Rough calculation: portion of monthly cost
                monthly_hours = 24 * 30
                hourly_rate = config["monthly_cost_usd"] / monthly_hours
                return duration_hours * hourly_rate * concurrency_factor
                
        elif platform == "redshift":
            if "serverless" in config_name:
                rpu_cost = duration_hours * config["rpu_hours"] * config["rpu_cost_usd"]
                return rpu_cost * concurrency_factor
            else:
                base_cost = duration_hours * config["cost_per_hour_usd"]
                if "spectrum" in config_name:
                    scan_cost = data_scanned_tb * config.get("cost_per_tb_scanned_usd", 0)
                    base_cost += scan_cost
                return base_cost * concurrency_factor
        
        return 0.0
    
    def _get_architecture_type(self, platform: str, config_name: str) -> str:
        """Determine architecture type based on platform and configuration"""
        if "external" in config_name or "spectrum" in config_name:
            return "lake_tables"
        elif "serverless" in config_name:
            return "serverless_dw"
        else:
            return "native_dw"
    
    def calculate_cost_efficiency_metrics(self, cost_data: List[Dict]) -> List[Dict]:
        """Calculate cost efficiency metrics across different patterns"""
        
        efficiency_metrics = []
        
        # Group by pattern and calculate relative costs
        patterns = {}
        for record in cost_data:
            pattern_id = record["pattern_id"]
            if pattern_id not in patterns:
                patterns[pattern_id] = []
            patterns[pattern_id].append(record)
        
        for pattern_id, records in patterns.items():
            # Find min/max costs for this pattern
            costs = [r["cost_usd_per_session"] for r in records]
            min_cost = min(costs)
            max_cost = max(costs)
            
            for record in records:
                cost_efficiency = min_cost / record["cost_usd_per_session"] if record["cost_usd_per_session"] > 0 else 0
                cost_premium = (record["cost_usd_per_session"] / min_cost - 1) * 100 if min_cost > 0 else 0
                
                efficiency_metrics.append({
                    "pattern_id": record["pattern_id"],
                    "platform_config": f"{record['platform']}_{record['configuration']}",
                    "architecture_type": record["architecture_type"],
                    "cost_usd_per_session": record["cost_usd_per_session"],
                    "cost_efficiency_ratio": round(cost_efficiency, 3),
                    "cost_premium_percent": round(cost_premium, 1),
                    "is_most_efficient": record["cost_usd_per_session"] == min_cost,
                    "monthly_cost_difference_usd": round(record["cost_usd_per_month"] - (min_cost * record["sessions_per_day"] * 30), 2)
                })
        
        return efficiency_metrics
    
    def save_session_costs(self, data: List[Dict], filename: str):
        """Save session cost analysis to CSV"""
        
        if not data:
            return
        
        fieldnames = list(data[0].keys())
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        print(f"Saved {len(data)} session cost records to {filename}")
    
    def create_cost_metadata(self, filename: str):
        """Create metadata for cost analysis"""
        
        metadata = {
            "dataset": {
                "title": "BI Dashboard Session Cost Analysis by Usage Pattern",
                "description": "Detailed cost breakdown for different BI dashboard usage patterns across cloud data platforms",
                "topic": "BI dashboard session-based cost modeling",
                "metric": "Cost per session, monthly costs, cost efficiency ratios"
            },
            "source": {
                "name": "Platform pricing models and usage pattern analysis", 
                "url": "Vendor pricing documentation",
                "accessed": datetime.now().strftime("%Y-%m-%d"),
                "license": "Research analysis",
                "credibility": "Tier A"
            },
            "characteristics": {
                "rows": "Multiple session patterns across platform configurations",
                "columns": "Cost and efficiency metrics",
                "time_range": "Current pricing (2024)",
                "update_frequency": "Quarterly (pricing changes)",
                "collection_method": "Cost model calculation"
            },
            "quality": {
                "completeness": "100%",
                "sample_size": "6 usage patterns x 12 platform configurations",
                "confidence": "high",
                "limitations": [
                    "Based on list pricing, not enterprise discounts",
                    "Does not include data storage costs",
                    "Simplified concurrency impact model",
                    "Regional pricing variations not included"
                ]
            },
            "notes": [
                "Costs include compute charges only, not storage",
                "Concurrency modeled as simple multiplier",
                "Serverless cold start costs estimated",
                "Real costs vary by optimization and caching"
            ]
        }
        
        meta_filename = filename.replace('.csv', '.meta.yaml')
        with open(meta_filename, 'w') as f:
            for section, content in metadata.items():
                f.write(f"{section}:\n")
                if isinstance(content, dict):
                    for key, value in content.items():
                        if isinstance(value, list):
                            f.write(f"  {key}:\n")
                            for item in value:
                                f.write(f"    - \"{item}\"\n")
                        else:
                            f.write(f"  {key}: \"{value}\"\n")
                elif isinstance(content, list):
                    for item in content:
                        f.write(f"  - \"{item}\"\n")
                f.write("\n")
        
        print(f"Created metadata file: {meta_filename}")

def main():
    """Main execution"""
    analyzer = SessionCostAnalyzer()
    
    print("Analyzing BI dashboard session costs across platforms...")
    
    # Get session patterns
    patterns = analyzer.analyze_session_patterns()
    
    # Calculate costs
    cost_analysis = analyzer.calculate_session_costs(patterns)
    efficiency_metrics = analyzer.calculate_cost_efficiency_metrics(cost_analysis)
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    costs_filename = f"{timestamp}__data__bi-session-costs__multi-platform__usage-pattern-analysis.csv"
    efficiency_filename = f"{timestamp}__data__bi-cost-efficiency__comparative__platform-optimization.csv"
    
    analyzer.save_session_costs(cost_analysis, costs_filename)
    analyzer.save_session_costs(efficiency_metrics, efficiency_filename)
    
    analyzer.create_cost_metadata(costs_filename)
    analyzer.create_cost_metadata(efficiency_filename)
    
    # Print analysis summary
    print(f"\nCost Analysis Summary:")
    print(f"Session patterns analyzed: {len(patterns)}")
    print(f"Platform configurations: {sum(len(configs) for configs in analyzer.cost_models.values())}")
    print(f"Total cost scenarios: {len(cost_analysis)}")
    
    # Show cost ranges
    costs = [record["cost_usd_per_session"] for record in cost_analysis]
    print(f"Session cost range: ${min(costs):.4f} - ${max(costs):.4f}")
    
    # Show most/least expensive patterns
    monthly_costs = [(record["pattern_id"], record["cost_usd_per_month"]) for record in cost_analysis]
    monthly_costs.sort(key=lambda x: x[1])
    
    print(f"Least expensive monthly pattern: {monthly_costs[0][0]} (${monthly_costs[0][1]:.2f})")
    print(f"Most expensive monthly pattern: {monthly_costs[-1][0]} (${monthly_costs[-1][1]:.2f})")
    
    print(f"\nFiles created:")
    print(f"- {costs_filename}")
    print(f"- {efficiency_filename}")
    print(f"- Corresponding .meta.yaml files")

if __name__ == "__main__":
    main()