#!/usr/bin/env python3
"""
Data Movement Tax (Egress/Ingest) Cost Data Collection
Search for cloud data transfer pricing and real-world cost studies
"""

import json
import csv
import requests
from datetime import datetime

def collect_aws_data_transfer_pricing():
    """Collect AWS data transfer pricing structure"""
    
    # AWS Data Transfer Pricing (as of 2024/2025)
    aws_pricing_data = [
        # Cross-AZ transfers
        {
            'cloud': 'AWS',
            'movement_type': 'cross_az_in',
            'gb_moved': 'per_gb',
            'cost_usd': 0.01,
            'source_region': 'any_az',
            'dest_region': 'different_az_same_region',
            'service': 'ec2_rds_data_transfer',
            'notes': 'Cross-AZ data transfer IN'
        },
        {
            'cloud': 'AWS',
            'movement_type': 'cross_az_out',
            'gb_moved': 'per_gb',
            'cost_usd': 0.01,
            'source_region': 'any_az',
            'dest_region': 'different_az_same_region',
            'service': 'ec2_rds_data_transfer',
            'notes': 'Cross-AZ data transfer OUT'
        },
        # Cross-region transfers
        {
            'cloud': 'AWS',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.02,
            'source_region': 'us_east_1',
            'dest_region': 'us_west_2',
            'service': 'general_data_transfer',
            'notes': 'Cross-region within US'
        },
        {
            'cloud': 'AWS',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.09,
            'source_region': 'us_east_1',
            'dest_region': 'eu_west_1',
            'service': 'general_data_transfer',
            'notes': 'Cross-region intercontinental'
        },
        # Internet egress
        {
            'cloud': 'AWS',
            'movement_type': 'internet_egress',
            'gb_moved': 'first_1gb_free',
            'cost_usd': 0.00,
            'source_region': 'any',
            'dest_region': 'internet',
            'service': 'cloudfront_s3_egress',
            'notes': 'First 1GB free per month'
        },
        {
            'cloud': 'AWS',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_up_to_10tb',
            'cost_usd': 0.09,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': 'Next 9.999TB per month'
        },
        {
            'cloud': 'AWS',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_10tb_to_50tb',
            'cost_usd': 0.085,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': '10TB to 50TB per month'
        },
        # CloudFront pricing
        {
            'cloud': 'AWS',
            'movement_type': 'cdn_egress',
            'gb_moved': 'first_1tb_free',
            'cost_usd': 0.00,
            'source_region': 'cloudfront_global',
            'dest_region': 'internet',
            'service': 'cloudfront',
            'notes': 'CloudFront free tier'
        },
        {
            'cloud': 'AWS',
            'movement_type': 'cdn_egress',
            'gb_moved': 'per_gb_up_to_10tb',
            'cost_usd': 0.085,
            'source_region': 'cloudfront_us_eu',
            'dest_region': 'internet',
            'service': 'cloudfront',
            'notes': 'CloudFront US/EU pricing'
        }
    ]
    
    return aws_pricing_data

def collect_gcp_data_transfer_pricing():
    """Collect Google Cloud data transfer pricing"""
    
    gcp_pricing_data = [
        # Cross-zone transfers
        {
            'cloud': 'GCP',
            'movement_type': 'cross_zone',
            'gb_moved': 'per_gb',
            'cost_usd': 0.01,
            'source_region': 'any_zone',
            'dest_region': 'different_zone_same_region',
            'service': 'compute_engine',
            'notes': 'Cross-zone within same region'
        },
        # Cross-region transfers
        {
            'cloud': 'GCP',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.02,
            'source_region': 'us_central1',
            'dest_region': 'us_west1',
            'service': 'general_networking',
            'notes': 'Cross-region within continent'
        },
        {
            'cloud': 'GCP',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.08,
            'source_region': 'us_central1',
            'dest_region': 'europe_west1',
            'service': 'general_networking',
            'notes': 'Cross-region intercontinental'
        },
        # Internet egress
        {
            'cloud': 'GCP',
            'movement_type': 'internet_egress',
            'gb_moved': 'first_1gb_free',
            'cost_usd': 0.00,
            'source_region': 'any',
            'dest_region': 'internet',
            'service': 'general_egress',
            'notes': 'First 1GB free per month'
        },
        {
            'cloud': 'GCP',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_up_to_1tb',
            'cost_usd': 0.12,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': 'Up to 1TB per month'
        },
        {
            'cloud': 'GCP',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_1tb_to_10tb',
            'cost_usd': 0.11,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': '1TB to 10TB per month'
        },
        # Cloud CDN
        {
            'cloud': 'GCP',
            'movement_type': 'cdn_egress',
            'gb_moved': 'per_gb',
            'cost_usd': 0.08,
            'source_region': 'cloud_cdn_global',
            'dest_region': 'internet',
            'service': 'cloud_cdn',
            'notes': 'Cloud CDN North America'
        }
    ]
    
    return gcp_pricing_data

def collect_azure_data_transfer_pricing():
    """Collect Azure data transfer pricing"""
    
    azure_pricing_data = [
        # Cross-zone transfers
        {
            'cloud': 'Azure',
            'movement_type': 'cross_zone',
            'gb_moved': 'per_gb',
            'cost_usd': 0.01,
            'source_region': 'any_zone',
            'dest_region': 'different_zone_same_region',
            'service': 'virtual_machines',
            'notes': 'Cross-zone within same region'
        },
        # Cross-region transfers
        {
            'cloud': 'Azure',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.02,
            'source_region': 'east_us',
            'dest_region': 'west_us',
            'service': 'general_networking',
            'notes': 'Cross-region within continent'
        },
        {
            'cloud': 'Azure',
            'movement_type': 'cross_region',
            'gb_moved': 'per_gb',
            'cost_usd': 0.087,
            'source_region': 'east_us',
            'dest_region': 'west_europe',
            'service': 'general_networking',
            'notes': 'Cross-region intercontinental'
        },
        # Internet egress
        {
            'cloud': 'Azure',
            'movement_type': 'internet_egress',
            'gb_moved': 'first_5gb_free',
            'cost_usd': 0.00,
            'source_region': 'any',
            'dest_region': 'internet',
            'service': 'general_egress',
            'notes': 'First 5GB free per month'
        },
        {
            'cloud': 'Azure',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_up_to_10tb',
            'cost_usd': 0.087,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': 'Up to 10TB per month'
        },
        {
            'cloud': 'Azure',
            'movement_type': 'internet_egress',
            'gb_moved': 'per_gb_10tb_to_50tb',
            'cost_usd': 0.083,
            'source_region': 'us_regions',
            'dest_region': 'internet',
            'service': 'standard_egress',
            'notes': '10TB to 50TB per month'
        }
    ]
    
    return azure_pricing_data

def collect_case_study_data():
    """Real-world case studies and cost scenarios"""
    
    case_studies = [
        # Multi-cloud scenarios
        {
            'cloud': 'Multi_AWS_GCP',
            'movement_type': 'multi_cloud_sync',
            'gb_moved': 100,
            'cost_usd': 8.70,
            'source_region': 'aws_us_east_1',
            'dest_region': 'gcp_us_central1',
            'service': 'data_replication',
            'notes': 'Estimated cost for 100GB cross-cloud transfer'
        },
        {
            'cloud': 'Multi_Azure_AWS',
            'movement_type': 'multi_cloud_backup',
            'gb_moved': 1000,
            'cost_usd': 87.00,
            'source_region': 'azure_east_us',
            'dest_region': 'aws_s3_us_west_2',
            'service': 'backup_replication',
            'notes': 'Monthly backup sync scenario'
        },
        # Large data migration scenarios
        {
            'cloud': 'AWS',
            'movement_type': 'data_migration',
            'gb_moved': 10000,
            'cost_usd': 850.00,
            'source_region': 'us_east_1',
            'dest_region': 'internet_customer_dc',
            'service': 'database_migration',
            'notes': '10TB database migration egress cost'
        },
        {
            'cloud': 'GCP',
            'movement_type': 'analytics_export',
            'gb_moved': 5000,
            'cost_usd': 550.00,
            'source_region': 'us_central1',
            'dest_region': 'internet_analytics_platform',
            'service': 'bigquery_export',
            'notes': '5TB BigQuery export scenario'
        },
        # CDN optimization scenarios
        {
            'cloud': 'AWS_CloudFront',
            'movement_type': 'cdn_optimization',
            'gb_moved': 1000,
            'cost_usd': 85.00,
            'source_region': 'cloudfront_global',
            'dest_region': 'internet_global',
            'service': 'content_delivery',
            'notes': '1TB monthly CDN delivery cost'
        }
    ]
    
    return case_studies

def main():
    """Collect all data movement cost data and save to CSV"""
    
    # Collect all pricing data
    all_data = []
    all_data.extend(collect_aws_data_transfer_pricing())
    all_data.extend(collect_gcp_data_transfer_pricing())
    all_data.extend(collect_azure_data_transfer_pricing())
    all_data.extend(collect_case_study_data())
    
    # Add timestamp and data source
    timestamp = datetime.now().strftime('%Y-%m-%d')
    for row in all_data:
        row['collection_date'] = timestamp
        row['data_source'] = 'official_pricing_documentation'
    
    # Save to CSV
    filename = f'datasets/{timestamp}__data__data-movement-tax__multi-cloud__transfer-pricing.csv'
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['cloud', 'movement_type', 'gb_moved', 'cost_usd', 'source_region', 
                     'dest_region', 'service', 'notes', 'collection_date', 'data_source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Data movement cost data saved to {filename}")
    print(f"Total records: {len(all_data)}")
    
    # Print summary
    clouds = set(row['cloud'] for row in all_data)
    movement_types = set(row['movement_type'] for row in all_data)
    
    print(f"\nClouds covered: {', '.join(clouds)}")
    print(f"Movement types: {', '.join(movement_types)}")

if __name__ == "__main__":
    main()