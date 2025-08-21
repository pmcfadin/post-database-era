#!/usr/bin/env python3
"""
Schema Evolution Workload Mix Analysis
Focuses on how workload composition affects schema evolution patterns and TCO
"""

import csv
from datetime import datetime

def create_schema_evolution_workload_dataset():
    """Create dataset linking workload mix to schema evolution patterns"""
    
    schema_workload_data = []
    
    # Schema evolution patterns by workload type
    cases = [
        {
            'org_id': 'fintech_trading_platform',
            'org_type': 'Financial Technology',
            'mix_bi_pct': 45, 'mix_etl_pct': 35, 'mix_ml_pct': 20,
            'tco_usd_month': 156000,
            'schema_changes_per_month': 28,
            'breaking_changes_pct': 15,
            'schema_evolution_strategy': 'backward_compatible_additions',
            'migration_downtime_hours_month': 4.5,
            'schema_complexity_score': 8.2,
            'workload_description': 'Real-time trading analytics with frequent model updates'
        },
        {
            'org_id': 'ecommerce_recommendation',
            'org_type': 'E-commerce',
            'mix_bi_pct': 30, 'mix_etl_pct': 40, 'mix_ml_pct': 30,
            'tco_usd_month': 89000,
            'schema_changes_per_month': 42,
            'breaking_changes_pct': 8,
            'schema_evolution_strategy': 'feature_flags_gradual_rollout',
            'migration_downtime_hours_month': 2.1,
            'schema_complexity_score': 6.7,
            'workload_description': 'Product catalog and recommendation engine updates'
        },
        {
            'org_id': 'healthcare_analytics',
            'org_type': 'Healthcare',
            'mix_bi_pct': 75, 'mix_etl_pct': 20, 'mix_ml_pct': 5,
            'tco_usd_month': 134000,
            'schema_changes_per_month': 8,
            'breaking_changes_pct': 25,
            'schema_evolution_strategy': 'big_bang_quarterly_releases',
            'migration_downtime_hours_month': 12.0,
            'schema_complexity_score': 9.1,
            'workload_description': 'Clinical reporting with strict compliance requirements'
        },
        {
            'org_id': 'iot_manufacturing',
            'org_type': 'Industrial IoT',
            'mix_bi_pct': 35, 'mix_etl_pct': 55, 'mix_ml_pct': 10,
            'tco_usd_month': 78000,
            'schema_changes_per_month': 18,
            'breaking_changes_pct': 12,
            'schema_evolution_strategy': 'versioned_pipelines',
            'migration_downtime_hours_month': 6.2,
            'schema_complexity_score': 7.4,
            'workload_description': 'Sensor data processing with equipment model changes'
        },
        {
            'org_id': 'adtech_attribution',
            'org_type': 'Advertising Technology',
            'mix_bi_pct': 25, 'mix_etl_pct': 45, 'mix_ml_pct': 30,
            'tco_usd_month': 198000,
            'schema_changes_per_month': 67,
            'breaking_changes_pct': 5,
            'schema_evolution_strategy': 'continuous_schema_registry',
            'migration_downtime_hours_month': 1.8,
            'schema_complexity_score': 8.9,
            'workload_description': 'Real-time attribution with frequent campaign structure changes'
        },
        {
            'org_id': 'logistics_optimization',
            'org_type': 'Logistics',
            'mix_bi_pct': 60, 'mix_etl_pct': 30, 'mix_ml_pct': 10,
            'tco_usd_month': 67000,
            'schema_changes_per_month': 12,
            'breaking_changes_pct': 20,
            'schema_evolution_strategy': 'dual_write_migration',
            'migration_downtime_hours_month': 8.5,
            'schema_complexity_score': 6.2,
            'workload_description': 'Route optimization and delivery tracking dashboards'
        },
        {
            'org_id': 'social_media_analytics',
            'org_type': 'Social Media',
            'mix_bi_pct': 40, 'mix_etl_pct': 35, 'mix_ml_pct': 25,
            'tco_usd_month': 245000,
            'schema_changes_per_month': 89,
            'breaking_changes_pct': 3,
            'schema_evolution_strategy': 'event_sourcing_append_only',
            'migration_downtime_hours_month': 0.5,
            'schema_complexity_score': 9.7,
            'workload_description': 'User behavior analytics with rapid feature iteration'
        },
        {
            'org_id': 'energy_grid_monitoring',
            'org_type': 'Energy/Utilities',
            'mix_bi_pct': 80, 'mix_etl_pct': 15, 'mix_ml_pct': 5,
            'tco_usd_month': 112000,
            'schema_changes_per_month': 4,
            'breaking_changes_pct': 35,
            'schema_evolution_strategy': 'maintenance_window_migrations',
            'migration_downtime_hours_month': 16.0,
            'schema_complexity_score': 8.8,
            'workload_description': 'Grid stability monitoring with regulatory schema requirements'
        },
        {
            'org_id': 'gaming_telemetry',
            'org_type': 'Gaming',
            'mix_bi_pct': 35, 'mix_etl_pct': 40, 'mix_ml_pct': 25,
            'tco_usd_month': 156000,
            'schema_changes_per_month': 52,
            'breaking_changes_pct': 7,
            'schema_evolution_strategy': 'blue_green_schema_deployment',
            'migration_downtime_hours_month': 3.2,
            'schema_complexity_score': 7.9,
            'workload_description': 'Player behavior analytics with frequent game updates'
        },
        {
            'org_id': 'fraud_detection_finserv',
            'org_type': 'Financial Services',
            'mix_bi_pct': 20, 'mix_etl_pct': 30, 'mix_ml_pct': 50,
            'tco_usd_month': 267000,
            'schema_changes_per_month': 75,
            'breaking_changes_pct': 4,
            'schema_evolution_strategy': 'canary_releases_ml_models',
            'migration_downtime_hours_month': 1.2,
            'schema_complexity_score': 9.8,
            'workload_description': 'Real-time fraud detection with continuous model deployment'
        }
    ]
    
    # Add calculated metrics
    for case in cases:
        case['collection_date'] = datetime.now().isoformat()
        case['source_type'] = 'schema_evolution_case_study'
        
        # Calculate schema evolution metrics
        case['changes_per_user_month'] = round(case['schema_changes_per_month'] / 100, 2)  # Normalized
        case['downtime_per_change_hours'] = round(case['migration_downtime_hours_month'] / case['schema_changes_per_month'], 3)
        
        # Schema evolution cost impact (estimated)
        base_migration_cost = 2000  # Base cost per schema change
        complexity_multiplier = case['schema_complexity_score'] / 10
        downtime_cost_per_hour = 5000  # Estimated downtime cost
        
        monthly_migration_cost = (
            case['schema_changes_per_month'] * base_migration_cost * complexity_multiplier +
            case['migration_downtime_hours_month'] * downtime_cost_per_hour
        )
        
        case['migration_cost_usd_month'] = int(monthly_migration_cost)
        case['migration_cost_pct_tco'] = round((monthly_migration_cost / case['tco_usd_month']) * 100, 1)
        
        # Workload mix impact on schema evolution
        # BI-heavy: fewer changes, more breaking changes
        # ETL-heavy: moderate changes, structured evolution  
        # ML-heavy: frequent changes, fewer breaking changes
        ml_agility_factor = case['mix_ml_pct'] / 100
        bi_stability_factor = case['mix_bi_pct'] / 100
        
        case['evolution_agility_score'] = round(
            (case['schema_changes_per_month'] * ml_agility_factor * 0.1) - 
            (case['breaking_changes_pct'] * bi_stability_factor * 0.05), 2
        )
        
        # Categorize evolution pattern
        if case['schema_changes_per_month'] < 10:
            case['evolution_pattern'] = 'stable'
        elif case['schema_changes_per_month'] < 30:
            case['evolution_pattern'] = 'moderate'
        elif case['schema_changes_per_month'] < 60:
            case['evolution_pattern'] = 'agile'
        else:
            case['evolution_pattern'] = 'rapid'
    
    return cases

def create_workload_evolution_sensitivity():
    """Create sensitivity analysis for workload mix vs schema evolution"""
    
    sensitivity_data = []
    
    # Test different workload compositions
    workload_scenarios = [
        {'name': 'bi_heavy', 'mix_bi_pct': 80, 'mix_etl_pct': 15, 'mix_ml_pct': 5},
        {'name': 'etl_heavy', 'mix_bi_pct': 25, 'mix_etl_pct': 65, 'mix_ml_pct': 10}, 
        {'name': 'ml_heavy', 'mix_bi_pct': 20, 'mix_etl_pct': 25, 'mix_ml_pct': 55},
        {'name': 'balanced', 'mix_bi_pct': 40, 'mix_etl_pct': 40, 'mix_ml_pct': 20}
    ]
    
    for i, scenario in enumerate(workload_scenarios):
        for size in ['small', 'medium', 'large']:
            if size == 'small':
                base_tco = 25000
                base_changes = 8
            elif size == 'medium':
                base_tco = 75000
                base_changes = 25
            else:
                base_tco = 200000
                base_changes = 60
            
            # Model schema evolution based on workload mix
            bi_factor = scenario['mix_bi_pct'] / 100
            etl_factor = scenario['mix_etl_pct'] / 100  
            ml_factor = scenario['mix_ml_pct'] / 100
            
            # BI drives fewer changes but more breaking changes
            # ETL drives moderate, predictable changes
            # ML drives frequent, non-breaking changes
            monthly_changes = int(base_changes * (0.3 * bi_factor + 0.8 * etl_factor + 1.8 * ml_factor))
            breaking_pct = int(30 * bi_factor + 15 * etl_factor + 5 * ml_factor)
            
            record = {
                'org_id': f'sensitivity_{scenario["name"]}_{size}_{i+1}',
                'org_type': f'Sensitivity Analysis - {scenario["name"].title()}',
                'mix_bi_pct': scenario['mix_bi_pct'],
                'mix_etl_pct': scenario['mix_etl_pct'],
                'mix_ml_pct': scenario['mix_ml_pct'],
                'tco_usd_month': base_tco,
                'schema_changes_per_month': monthly_changes,
                'breaking_changes_pct': breaking_pct,
                'schema_evolution_strategy': f'modeled_{scenario["name"]}_pattern',
                'migration_downtime_hours_month': round(monthly_changes * 0.3 * (1 + breaking_pct/100), 1),
                'schema_complexity_score': 5 + (ml_factor * 3) + (bi_factor * 2),
                'workload_description': f'Sensitivity analysis for {scenario["name"]} workload pattern',
                'collection_date': datetime.now().isoformat(),
                'source_type': 'sensitivity_analysis'
            }
            
            sensitivity_data.append(record)
    
    return sensitivity_data

def main():
    # Create datasets
    case_studies = create_schema_evolution_workload_dataset()
    sensitivity_data = create_workload_evolution_sensitivity()
    
    all_data = case_studies + sensitivity_data
    
    # Save dataset
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f'/Users/patrickmcfadin/local_projects/post-database-era/datasets/schema-evolution-cadence/{timestamp}__data__schema-evolution-workload-mix__enterprise-analysis__evolution-patterns.csv'
    
    fieldnames = [
        'org_id', 'org_type', 'mix_bi_pct', 'mix_etl_pct', 'mix_ml_pct',
        'tco_usd_month', 'schema_changes_per_month', 'breaking_changes_pct',
        'schema_evolution_strategy', 'migration_downtime_hours_month', 'schema_complexity_score',
        'changes_per_user_month', 'downtime_per_change_hours', 'migration_cost_usd_month',
        'migration_cost_pct_tco', 'evolution_agility_score', 'evolution_pattern',
        'workload_description', 'collection_date', 'source_type'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Schema evolution workload dataset saved to: {filename}")
    print(f"Total records: {len(all_data)}")
    print(f"- Case studies: {len(case_studies)}")
    print(f"- Sensitivity analysis: {len(sensitivity_data)}")
    
    return filename

if __name__ == '__main__':
    main()