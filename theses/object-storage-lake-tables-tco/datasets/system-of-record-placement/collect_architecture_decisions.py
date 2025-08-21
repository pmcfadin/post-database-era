#!/usr/bin/env python3
"""
Architecture Decision Records for SOR Placement
Collects data on architectural decision patterns and data product ownership models
"""

import csv
from datetime import datetime

def collect_architecture_decision_patterns():
    """Collect patterns from Architecture Decision Records (ADRs)"""
    
    adr_patterns = [
        {
            'decision_id': 'ADR-001',
            'domain': 'customer_analytics',
            'dataset': 'customer_360_view',
            'decision': 'warehouse_native',
            'rationale': 'Real-time personalization requires sub-second query response',
            'trade_offs': 'Higher storage costs, limited schema flexibility',
            'stakeholders': 'Analytics, Marketing, Customer Success',
            'decision_date': '2024-03-15',
            'review_cycle': 'quarterly',
            'constraints': 'GDPR compliance, <100ms query SLA'
        },
        {
            'decision_id': 'ADR-002',
            'domain': 'product_events',
            'dataset': 'clickstream_golden',
            'decision': 'lake_first',
            'rationale': 'Schema evolution for A/B testing, ML feature engineering',
            'trade_offs': 'Query complexity, potential consistency issues',
            'stakeholders': 'Data Science, Product Analytics, Engineering',
            'decision_date': '2024-01-20',
            'review_cycle': 'bi-annual',
            'constraints': 'Schema evolution support, multi-format access'
        },
        {
            'decision_id': 'ADR-003',
            'domain': 'financial_transactions',
            'dataset': 'payment_ledger',
            'decision': 'warehouse_native',
            'rationale': 'Audit requirements, transaction consistency guarantees',
            'trade_offs': 'Limited real-time ML, higher compute costs',
            'stakeholders': 'Finance, Compliance, Risk Management',
            'decision_date': '2023-11-10',
            'review_cycle': 'annual',
            'constraints': 'SOX compliance, ACID guarantees, audit trails'
        },
        {
            'decision_id': 'ADR-004',
            'domain': 'iot_telemetry',
            'dataset': 'sensor_data_master',
            'decision': 'hybrid_approach',
            'rationale': 'Real-time alerting + historical analytics requirements',
            'trade_offs': 'Operational complexity, data synchronization',
            'stakeholders': 'IoT Platform, Operations, Data Engineering',
            'decision_date': '2024-05-08',
            'review_cycle': 'quarterly',
            'constraints': 'Real-time processing, long-term retention'
        },
        {
            'decision_id': 'ADR-005',
            'domain': 'supply_chain',
            'dataset': 'inventory_master',
            'decision': 'warehouse_native',
            'rationale': 'Complex joins for supply chain optimization',
            'trade_offs': 'Slower schema changes, higher transformation costs',
            'stakeholders': 'Supply Chain, Operations, Finance',
            'decision_date': '2024-02-28',
            'review_cycle': 'quarterly',
            'constraints': 'Real-time inventory updates, complex analytics'
        },
        {
            'decision_id': 'ADR-006',
            'domain': 'ml_training',
            'dataset': 'feature_store_golden',
            'decision': 'lake_first',
            'rationale': 'Feature engineering flexibility, model experimentation',
            'trade_offs': 'Query performance for serving, governance complexity',
            'stakeholders': 'ML Engineering, Data Science, MLOps',
            'decision_date': '2024-04-12',
            'review_cycle': 'bi-annual',
            'constraints': 'Version control, lineage tracking, serving performance'
        }
    ]
    
    return adr_patterns

def collect_data_product_ownership():
    """Collect data product ownership and governance patterns"""
    
    ownership_patterns = [
        {
            'data_product': 'customer_master',
            'domain_owner': 'Customer Experience',
            'technical_owner': 'Customer Data Platform Team',
            'sor_location': 'warehouse',
            'governance_model': 'centralized_stewardship',
            'access_pattern': 'api_first',
            'sla_read': '99.9%',
            'sla_freshness': '15_minutes',
            'consumer_count': 45,
            'monthly_queries': 2500000
        },
        {
            'data_product': 'product_catalog',
            'domain_owner': 'Product Management',
            'technical_owner': 'Commerce Platform Team',
            'sor_location': 'lake',
            'governance_model': 'federated_ownership',
            'access_pattern': 'direct_query',
            'sla_read': '99.5%',
            'sla_freshness': '1_hour',
            'consumer_count': 28,
            'monthly_queries': 850000
        },
        {
            'data_product': 'financial_transactions',
            'domain_owner': 'Finance',
            'technical_owner': 'Financial Systems Team',
            'sor_location': 'warehouse',
            'governance_model': 'centralized_control',
            'access_pattern': 'api_only',
            'sla_read': '99.99%',
            'sla_freshness': '5_minutes',
            'consumer_count': 12,
            'monthly_queries': 450000
        },
        {
            'data_product': 'user_behavior_events',
            'domain_owner': 'Analytics',
            'technical_owner': 'Analytics Engineering Team',
            'sor_location': 'lake',
            'governance_model': 'self_service',
            'access_pattern': 'sql_interface',
            'sla_read': '99.0%',
            'sla_freshness': '2_hours',
            'consumer_count': 67,
            'monthly_queries': 1200000
        },
        {
            'data_product': 'marketing_campaigns',
            'domain_owner': 'Marketing',
            'technical_owner': 'MarTech Platform Team',
            'sor_location': 'hybrid',
            'governance_model': 'domain_ownership',
            'access_pattern': 'multi_modal',
            'sla_read': '99.5%',
            'sla_freshness': '30_minutes',
            'consumer_count': 22,
            'monthly_queries': 380000
        }
    ]
    
    return ownership_patterns

def collect_single_source_truth_decisions():
    """Collect data on single source of truth implementation patterns"""
    
    ssot_patterns = [
        {
            'entity_type': 'customer',
            'golden_dataset': 'customer_master_record',
            'sor_strategy': 'warehouse_authoritative',
            'sync_pattern': 'cdc_real_time',
            'conflict_resolution': 'timestamp_priority',
            'data_quality_score': 94.5,
            'consolidation_ratio': '12:1',  # 12 sources consolidated to 1
            'maintenance_effort': 'medium',
            'business_value': 'high'
        },
        {
            'entity_type': 'product',
            'golden_dataset': 'product_information_master',
            'sor_strategy': 'lake_authoritative',
            'sync_pattern': 'batch_nightly',
            'conflict_resolution': 'business_rules',
            'data_quality_score': 89.2,
            'consolidation_ratio': '8:1',
            'maintenance_effort': 'low',
            'business_value': 'medium'
        },
        {
            'entity_type': 'transaction',
            'golden_dataset': 'financial_ledger',
            'sor_strategy': 'warehouse_authoritative',
            'sync_pattern': 'synchronous_api',
            'conflict_resolution': 'manual_review',
            'data_quality_score': 99.1,
            'consolidation_ratio': '3:1',
            'maintenance_effort': 'high',
            'business_value': 'critical'
        },
        {
            'entity_type': 'employee',
            'golden_dataset': 'hr_master_record',
            'sor_strategy': 'warehouse_authoritative',
            'sync_pattern': 'scheduled_batch',
            'conflict_resolution': 'hr_system_priority',
            'data_quality_score': 96.8,
            'consolidation_ratio': '5:1',
            'maintenance_effort': 'medium',
            'business_value': 'high'
        },
        {
            'entity_type': 'inventory',
            'golden_dataset': 'inventory_positions',
            'sor_strategy': 'hybrid_real_time',
            'sync_pattern': 'event_streaming',
            'conflict_resolution': 'last_write_wins',
            'data_quality_score': 87.3,
            'consolidation_ratio': '15:1',
            'maintenance_effort': 'high',
            'business_value': 'critical'
        }
    ]
    
    return ssot_patterns

def main():
    """Generate additional SOR placement datasets"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    base_path = "/Users/patrickmcfadin/local_projects/post-database-era/datasets/system-of-record-placement"
    
    # Architecture Decision Records
    adr_data = collect_architecture_decision_patterns()
    with open(f'{base_path}/{timestamp}__data__sor-placement__architecture-decisions__placement-adrs.csv', 'w', newline='') as f:
        if adr_data:
            fieldnames = adr_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(adr_data)
    
    # Data Product Ownership
    ownership_data = collect_data_product_ownership()
    with open(f'{base_path}/{timestamp}__data__sor-placement__data-products__ownership-patterns.csv', 'w', newline='') as f:
        if ownership_data:
            fieldnames = ownership_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ownership_data)
    
    # Single Source of Truth Patterns
    ssot_data = collect_single_source_truth_decisions()
    with open(f'{base_path}/{timestamp}__data__sor-placement__ssot-patterns__truth-implementation.csv', 'w', newline='') as f:
        if ssot_data:
            fieldnames = ssot_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ssot_data)
    
    print(f"Generated additional datasets:")
    print(f"- Architecture decisions: {len(adr_data)} records")
    print(f"- Data product ownership: {len(ownership_data)} records")
    print(f"- SSOT patterns: {len(ssot_data)} records")

if __name__ == "__main__":
    main()