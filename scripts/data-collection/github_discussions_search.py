#!/usr/bin/env python3
"""
GitHub Discussions and Issues Search for Multi-API Gateway Terms
Searches popular database repositories for gateway-related discussions
"""

import requests
import json
import csv
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Popular database-related repositories to search
REPOS = [
    "mongodb/mongo",
    "apache/kafka", 
    "elastic/elasticsearch",
    "redis/redis",
    "cassandra/cassandra",
    "trino-io/trino",
    "apache/arrow",
    "duckdb/duckdb",
    "apache/iceberg",
    "apache/spark"
]

# Search terms for gateway concepts
GATEWAY_TERMS = [
    "multi-api",
    "unified api",
    "database gateway", 
    "query router",
    "api gateway",
    "multi-model",
    "polyglot persistence",
    "cross-platform",
    "unified interface",
    "gateway pattern"
]

def search_github_issues(repo: str, query: str, per_page: int = 30) -> Dict[str, Any]:
    """Search GitHub issues and discussions for a specific query"""
    url = "https://api.github.com/search/issues"
    
    # Search in both issues and discussions (if available)
    search_query = f'repo:{repo} "{query}" type:issue'
    
    params = {
        'q': search_query,
        'sort': 'created',
        'order': 'desc',
        'per_page': per_page
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 403:
            logger.warning(f"Rate limited - waiting...")
            time.sleep(60)
            response = requests.get(url, params=params)
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching {repo} for '{query}': {e}")
        return {}

def analyze_results():
    """Analyze search results and create summary dataset"""
    results = []
    
    logger.info(f"Searching {len(REPOS)} repositories for {len(GATEWAY_TERMS)} gateway terms")
    
    for repo in REPOS:
        logger.info(f"Processing repository: {repo}")
        
        for term in GATEWAY_TERMS:
            logger.info(f"  Searching for: {term}")
            
            search_results = search_github_issues(repo, term)
            
            if 'items' in search_results:
                issue_count = len(search_results['items'])
                total_comments = sum(item.get('comments', 0) for item in search_results['items'])
                
                # Analyze issue titles and bodies for context
                contexts = []
                for item in search_results['items'][:5]:  # Sample first 5
                    title = item.get('title', '').lower()
                    body = item.get('body', '').lower() if item.get('body') else ''
                    
                    # Look for multi-API context
                    if any(keyword in f"{title} {body}" for keyword in ['sql', 'nosql', 'graph', 'document', 'search', 'analytics']):
                        contexts.append('multi-api-discussion')
                    elif any(keyword in f"{title} {body}" for keyword in ['gateway', 'router', 'proxy', 'unified']):
                        contexts.append('gateway-pattern')
                    else:
                        contexts.append('general')
                
                primary_context = max(set(contexts), key=contexts.count) if contexts else 'unknown'
                
                result = {
                    'platform_tag': 'github-issues',
                    'repository': repo,
                    'search_term': term,
                    'issue_count': issue_count,
                    'total_comments': total_comments,
                    'avg_comments': total_comments / issue_count if issue_count > 0 else 0,
                    'primary_context': primary_context,
                    'search_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                results.append(result)
                logger.info(f"    Found {issue_count} issues, {total_comments} total comments")
                
                # Rate limiting
                time.sleep(1)
            else:
                # No results
                result = {
                    'platform_tag': 'github-issues',
                    'repository': repo,
                    'search_term': term,
                    'issue_count': 0,
                    'total_comments': 0,
                    'avg_comments': 0,
                    'primary_context': 'none',
                    'search_date': datetime.now().strftime('%Y-%m-%d')
                }
                results.append(result)
                time.sleep(0.5)
    
    return results

def save_results(results: List[Dict[str, Any]]):
    """Save results to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"/Users/patrickmcfadin/local_projects/post-database-era/datasets/{timestamp}__data__github-discussions__github__gateway-terms.csv"
    
    fieldnames = ['platform_tag', 'repository', 'search_term', 'issue_count', 
                 'total_comments', 'avg_comments', 'primary_context', 'search_date']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    logger.info(f"GitHub search results saved to {filename}")
    logger.info(f"Total records: {len(results)}")
    
    # Print summary
    print("\nTop Repositories by Gateway Discussions:")
    repo_totals = {}
    for result in results:
        repo = result['repository']
        if repo not in repo_totals:
            repo_totals[repo] = {'issues': 0, 'comments': 0}
        repo_totals[repo]['issues'] += result['issue_count']
        repo_totals[repo]['comments'] += result['total_comments']
    
    for repo, totals in sorted(repo_totals.items(), key=lambda x: x[1]['issues'], reverse=True):
        print(f"  {repo}: {totals['issues']} issues, {totals['comments']} comments")

if __name__ == "__main__":
    try:
        results = analyze_results()
        save_results(results)
    except KeyboardInterrupt:
        logger.info("Search interrupted by user")
    except Exception as e:
        logger.error(f"Error during GitHub search: {e}")