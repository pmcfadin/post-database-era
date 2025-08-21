#!/usr/bin/env python3
"""
Data collection script for catalog & governance service costs
Searches multiple sources for pricing data on data catalog and governance platforms
"""

import requests
import json
import csv
import time
from datetime import datetime
from urllib.parse import quote

def search_github_for_cost_data():
    """Search GitHub for cost data and billing information"""
    cost_data = []
    
    # GitHub search queries for cost-related repositories and discussions
    queries = [
        "AWS Glue Data Catalog pricing cost",
        "Databricks Unity Catalog cost billing",
        "Apache Atlas operational cost",
        "Collibra pricing model cost",
        "Alation pricing cost structure",
        "DataHub lineage cost pricing",
        "data catalog governance cost comparison",
        "data governance platform pricing",
        "unity catalog billing cost",
        "glue catalog cost optimization"
    ]
    
    for query in queries:
        print(f"Searching GitHub for: {query}")
        
        # Search code repositories
        search_url = f"https://api.github.com/search/repositories?q={quote(query)}&sort=updated&order=desc&per_page=10"
        
        try:
            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                results = response.json()
                
                for repo in results.get('items', []):
                    cost_data.append({
                        'source_type': 'github_repo',
                        'query': query,
                        'title': repo.get('name', ''),
                        'description': repo.get('description', ''),
                        'url': repo.get('html_url', ''),
                        'stars': repo.get('stargazers_count', 0),
                        'updated': repo.get('updated_at', ''),
                        'language': repo.get('language', ''),
                        'topics': ','.join(repo.get('topics', []))
                    })
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            continue
    
    return cost_data

def search_for_pricing_pages():
    """Collect known pricing page URLs for manual verification"""
    pricing_sources = [
        {
            'service': 'AWS Glue Data Catalog',
            'pricing_url': 'https://aws.amazon.com/glue/pricing/',
            'documentation': 'https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html',
            'pricing_model': 'pay_per_request',
            'notes': 'First million objects free per month'
        },
        {
            'service': 'Databricks Unity Catalog',
            'pricing_url': 'https://databricks.com/product/unity-catalog',
            'documentation': 'https://docs.databricks.com/en/data-governance/unity-catalog/index.html',
            'pricing_model': 'included_with_platform',
            'notes': 'Included with Databricks platform subscription'
        },
        {
            'service': 'Collibra Data Catalog',
            'pricing_url': 'https://www.collibra.com/pricing',
            'documentation': 'https://www.collibra.com/us/en/products/data-catalog',
            'pricing_model': 'enterprise_license',
            'notes': 'Contact sales for pricing'
        },
        {
            'service': 'Alation Data Catalog',
            'pricing_url': 'https://www.alation.com/pricing/',
            'documentation': 'https://www.alation.com/product/data-catalog/',
            'pricing_model': 'tiered_subscription',
            'notes': 'Multiple tiers: Essentials, Professional, Enterprise'
        },
        {
            'service': 'Apache Atlas',
            'pricing_url': 'https://atlas.apache.org/',
            'documentation': 'https://atlas.apache.org/#/Documentation',
            'pricing_model': 'open_source',
            'notes': 'Open source - infrastructure costs only'
        },
        {
            'service': 'DataHub',
            'pricing_url': 'https://datahubproject.io/',
            'documentation': 'https://datahubproject.io/docs/',
            'pricing_model': 'open_source_saas',
            'notes': 'Open source + Acryl Data managed service'
        },
        {
            'service': 'Google Cloud Data Catalog',
            'pricing_url': 'https://cloud.google.com/data-catalog/pricing',
            'documentation': 'https://cloud.google.com/data-catalog/docs',
            'pricing_model': 'pay_per_request',
            'notes': 'Free tier available'
        },
        {
            'service': 'Azure Purview',
            'pricing_url': 'https://azure.microsoft.com/en-us/pricing/details/azure-purview/',
            'documentation': 'https://docs.microsoft.com/en-us/azure/purview/',
            'pricing_model': 'consumption_based',
            'notes': 'Pay for data map units and scanning'
        }
    ]
    
    return pricing_sources

def collect_cost_studies():
    """Collect known cost studies and analysis reports"""
    cost_studies = [
        {
            'source': 'Gartner',
            'title': 'Total Cost of Ownership for Data Catalog Solutions',
            'year': '2024',
            'access': 'subscription_required',
            'url': 'https://www.gartner.com/en/documents/catalog-metadata-management',
            'focus': 'TCO analysis across vendors'
        },
        {
            'source': 'Forrester',
            'title': 'The Total Economic Impact of Data Governance Platforms',
            'year': '2023',
            'access': 'subscription_required',
            'url': 'https://www.forrester.com/report/the-total-economic-impact-of-data-governance/',
            'focus': 'ROI and cost benefit analysis'
        },
        {
            'source': 'IDC',
            'title': 'Worldwide Data Integration and Intelligence Software Market',
            'year': '2024',
            'access': 'subscription_required',
            'url': 'https://www.idc.com/getdoc.jsp?containerId=US49817923',
            'focus': 'Market sizing and vendor analysis'
        }
    ]
    
    return cost_studies

def main():
    print("Collecting catalog & governance cost data...")
    
    # Collect data from various sources
    github_data = search_github_for_cost_data()
    pricing_sources = search_for_pricing_pages()
    cost_studies = collect_cost_studies()
    
    # Save GitHub search results
    with open('catalog_governance_github_search.json', 'w') as f:
        json.dump(github_data, f, indent=2)
    
    # Save pricing sources
    with open('catalog_governance_pricing_sources.json', 'w') as f:
        json.dump(pricing_sources, f, indent=2)
    
    # Save cost studies
    with open('catalog_governance_cost_studies.json', 'w') as f:
        json.dump(cost_studies, f, indent=2)
    
    print(f"Collected {len(github_data)} GitHub results")
    print(f"Documented {len(pricing_sources)} pricing sources")
    print(f"Listed {len(cost_studies)} cost studies")

if __name__ == "__main__":
    main()