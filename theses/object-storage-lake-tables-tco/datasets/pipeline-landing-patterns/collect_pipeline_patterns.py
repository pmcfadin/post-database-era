#!/usr/bin/env python3
"""
Pipeline Landing Pattern Data Collection
Searches for ETL vs ELT adoption, data lake first architectures, and orchestration patterns
"""

import requests
import json
import csv
import time
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any

class PipelineLandingPatternCollector:
    def __init__(self):
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    
    def search_stackoverflow_patterns(self):
        """Search Stack Overflow for pipeline pattern discussions"""
        patterns = [
            "ETL vs ELT data lake",
            "landing zone object storage",
            "airflow DAG data lake first",
            "pipeline raw data s3 first",
            "ELT pattern data warehouse",
            "streaming pipeline landing zone",
            "batch ingestion object storage"
        ]
        
        results = []
        for pattern in patterns:
            try:
                # Stack Overflow API search
                url = f"https://api.stackexchange.com/2.3/search/advanced"
                params = {
                    'order': 'desc',
                    'sort': 'relevance',
                    'q': pattern,
                    'site': 'stackoverflow',
                    'pagesize': 30,
                    'filter': 'withbody'
                }
                
                response = requests.get(url, params=params, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items', []):
                        # Extract pattern indicators from questions/answers
                        body_text = item.get('body', '').lower()
                        title = item.get('title', '').lower()
                        
                        # Classify landing pattern
                        landing_pattern = self.classify_landing_pattern(title + " " + body_text)
                        
                        results.append({
                            'source': 'stackoverflow',
                            'pattern_query': pattern,
                            'post_id': item.get('question_id'),
                            'title': item.get('title'),
                            'score': item.get('score', 0),
                            'view_count': item.get('view_count', 0),
                            'answer_count': item.get('answer_count', 0),
                            'creation_date': datetime.fromtimestamp(item.get('creation_date', 0)),
                            'landing_pattern': landing_pattern,
                            'has_airflow': 'airflow' in (title + " " + body_text),
                            'has_s3': any(term in (title + " " + body_text) for term in ['s3', 'object storage', 'blob']),
                            'has_streaming': any(term in (title + " " + body_text) for term in ['stream', 'kafka', 'kinesis']),
                            'url': item.get('link')
                        })
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"Error searching pattern {pattern}: {e}")
                
        return results
    
    def search_github_dags(self):
        """Search GitHub for Airflow DAGs showing landing patterns"""
        results = []
        
        # GitHub search queries for DAG patterns
        dag_queries = [
            "airflow s3 raw data landing",
            "airflow ELT pattern",
            "airflow data lake first",
            "airflow landing zone",
            "airflow object storage first",
            "dag s3 to warehouse",
            "airflow raw data ingestion"
        ]
        
        for query in dag_queries:
            try:
                # GitHub API search for code
                url = "https://api.github.com/search/code"
                params = {
                    'q': f"{query} language:python",
                    'sort': 'indexed',
                    'per_page': 30
                }
                
                response = requests.get(url, params=params, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items', []):
                        # Analyze DAG content for patterns
                        repo_name = item.get('repository', {}).get('full_name', '')
                        file_path = item.get('path', '')
                        
                        results.append({
                            'source': 'github_dags',
                            'query': query,
                            'repo': repo_name,
                            'file_path': file_path,
                            'url': item.get('html_url'),
                            'score': item.get('score', 0),
                            'is_dag_file': file_path.endswith('.py') and ('dag' in file_path.lower() or 'airflow' in file_path.lower())
                        })
                
                time.sleep(1)  # GitHub rate limiting
                
            except Exception as e:
                print(f"Error searching GitHub for {query}: {e}")
                
        return results
    
    def search_surveys_reports(self):
        """Search for industry surveys on pipeline patterns"""
        results = []
        
        # Key reports and surveys to search for
        survey_sources = [
            "State of Data Engineering 2024",
            "Databricks Data + AI Summit pipeline patterns",
            "dbt State of Analytics Engineering",
            "Fivetran Modern Data Stack Report",
            "Airbyte State of Data Integration",
            "Snowflake Modern Data Stack survey",
            "AWS re:Invent data pipeline patterns",
            "Google Cloud data engineering survey"
        ]
        
        for source in survey_sources:
            try:
                # Search for public reports/surveys
                search_url = f"https://www.google.com/search?q=\"{source}\" ETL ELT pattern adoption filetype:pdf"
                # Note: This would need actual web scraping implementation
                # For now, documenting the search patterns
                
                results.append({
                    'source': 'industry_survey',
                    'survey_name': source,
                    'search_query': f"{source} ETL ELT pattern adoption",
                    'status': 'search_documented'
                })
                
            except Exception as e:
                print(f"Error searching survey {source}: {e}")
                
        return results
    
    def classify_landing_pattern(self, text: str) -> str:
        """Classify the landing pattern based on text content"""
        text = text.lower()
        
        # ELT indicators
        elt_indicators = [
            'raw data first', 'land raw', 'object storage first', 's3 first',
            'data lake first', 'elt pattern', 'extract load transform',
            'landing zone', 'bronze layer', 'raw layer'
        ]
        
        # ETL indicators  
        etl_indicators = [
            'transform before load', 'etl pattern', 'extract transform load',
            'warehouse first', 'clean before storage', 'transform then load'
        ]
        
        # Streaming indicators
        streaming_indicators = [
            'streaming', 'kafka', 'kinesis', 'real-time', 'event-driven',
            'stream processing', 'event streaming'
        ]
        
        if any(indicator in text for indicator in streaming_indicators):
            return 'streaming'
        elif any(indicator in text for indicator in elt_indicators):
            return 'elt_object_first'
        elif any(indicator in text for indicator in etl_indicators):
            return 'etl_warehouse_first'
        else:
            return 'unknown'
    
    def collect_all_data(self):
        """Collect data from all sources"""
        print("Collecting Stack Overflow pipeline pattern data...")
        so_data = self.search_stackoverflow_patterns()
        
        print("Collecting GitHub DAG pattern data...")
        github_data = self.search_github_dags()
        
        print("Collecting survey/report data...")
        survey_data = self.search_surveys_reports()
        
        return {
            'stackoverflow': so_data,
            'github_dags': github_data,
            'surveys': survey_data
        }

def main():
    collector = PipelineLandingPatternCollector()
    
    print("Starting pipeline landing pattern data collection...")
    all_data = collector.collect_all_data()
    
    # Save raw data
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    with open(f'pipeline_landing_raw_data_{timestamp}.json', 'w') as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print(f"Raw data saved to pipeline_landing_raw_data_{timestamp}.json")
    
    # Process and create CSV datasets
    create_pipeline_datasets(all_data, timestamp)

def create_pipeline_datasets(data, timestamp):
    """Create structured CSV datasets from collected data"""
    
    # Dataset 1: Stack Overflow Pipeline Pattern Analysis
    so_data = data['stackoverflow']
    if so_data:
        so_df = pd.DataFrame(so_data)
        so_filename = f"{timestamp}__data__pipeline-landing-patterns__stackoverflow__pattern-discussion.csv"
        so_df.to_csv(so_filename, index=False)
        print(f"Created {so_filename}")
    
    # Dataset 2: GitHub DAG Pattern Analysis  
    github_data = data['github_dags']
    if github_data:
        github_df = pd.DataFrame(github_data)
        github_filename = f"{timestamp}__data__pipeline-landing-patterns__github__dag-patterns.csv"
        github_df.to_csv(github_filename, index=False)
        print(f"Created {github_filename}")
    
    # Dataset 3: Aggregated Pattern Summary
    pattern_summary = []
    
    # Analyze Stack Overflow patterns
    if so_data:
        pattern_counts = {}
        for item in so_data:
            pattern = item.get('landing_pattern', 'unknown')
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        total_so = len(so_data)
        for pattern, count in pattern_counts.items():
            pattern_summary.append({
                'source': 'stackoverflow',
                'landing_pattern': pattern,
                'count': count,
                'percentage': (count / total_so) * 100 if total_so > 0 else 0,
                'sample_size': total_so
            })
    
    if pattern_summary:
        summary_df = pd.DataFrame(pattern_summary)
        summary_filename = f"{timestamp}__data__pipeline-landing-patterns__aggregated__pattern-adoption.csv"
        summary_df.to_csv(summary_filename, index=False)
        print(f"Created {summary_filename}")

if __name__ == "__main__":
    main()