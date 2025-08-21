#!/usr/bin/env python3
"""
Stack Overflow Historical Trends Collector
Collects quarterly data for key multi-API tags over the past 2 years
"""

import requests
import json
import csv
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import urllib.parse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_questions_for_period(tag: str, fromdate: int, todate: int) -> Dict[str, Any]:
    """Get questions for a specific tag in a date range"""
    base_url = "https://api.stackexchange.com/2.3"
    url = f"{base_url}/questions"
    
    params = {
        'site': 'stackoverflow',
        'tagged': tag,
        'fromdate': fromdate,
        'todate': todate,
        'pagesize': 100,
        'filter': 'default'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {tag} for period: {e}")
        return {}

def main():
    # Key tags to track
    key_tags = [
        'azure-cosmosdb',
        'mongodb',
        'mongodb-atlas',
        'aws-documentdb',
        'firebase',
        'amazon-dynamodb',
        'api-gateway',
        'nosql'
    ]
    
    results = []
    
    # Generate quarterly periods for the last 2 years
    end_date = datetime.now()
    periods = []
    
    for year in [2023, 2024, 2025]:
        for quarter in [1, 2, 3, 4]:
            if quarter == 1:
                start_month, end_month = 1, 3
            elif quarter == 2:
                start_month, end_month = 4, 6
            elif quarter == 3:
                start_month, end_month = 7, 9
            else:
                start_month, end_month = 10, 12
            
            period_start = datetime(year, start_month, 1)
            if end_month == 12:
                period_end = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                period_end = datetime(year, end_month + 1, 1) - timedelta(days=1)
            
            # Only include periods that have ended or current quarter
            if period_start <= end_date:
                periods.append({
                    'label': f"{year}-Q{quarter}",
                    'start': int(period_start.timestamp()),
                    'end': int(period_end.timestamp())
                })
    
    logger.info(f"Collecting data for {len(periods)} quarters and {len(key_tags)} tags")
    
    for period in periods:
        logger.info(f"Processing period: {period['label']}")
        
        for tag in key_tags:
            logger.info(f"  Tag: {tag}")
            
            questions_data = get_questions_for_period(tag, period['start'], period['end'])
            
            if 'items' in questions_data:
                question_count = len(questions_data['items'])
                
                # Calculate metrics
                total_score = sum(q.get('score', 0) for q in questions_data['items'])
                total_views = sum(q.get('view_count', 0) for q in questions_data['items'])
                answered_count = sum(1 for q in questions_data['items'] if q.get('is_answered', False))
                
                # Categorize
                if tag in ['azure-cosmosdb', 'mongodb', 'mongodb-atlas', 'aws-documentdb']:
                    category = 'multi-api'
                elif tag == 'api-gateway':
                    category = 'gateway'
                elif tag == 'nosql':
                    category = 'cross-api'
                else:
                    category = 'platform'
                
                result = {
                    'platform_tag': 'stackoverflow',
                    'api_tag': tag,
                    'tag_category': category,
                    'count': question_count,
                    'month': period['label'],
                    'total_score': total_score,
                    'total_views': total_views,
                    'answered_count': answered_count,
                    'answer_rate': answered_count / question_count if question_count > 0 else 0,
                    'avg_score': total_score / question_count if question_count > 0 else 0,
                    'avg_views': total_views / question_count if question_count > 0 else 0
                }
                
                results.append(result)
                logger.info(f"    {question_count} questions")
            
            time.sleep(0.1)  # Rate limiting
    
    # Save results
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"/Users/patrickmcfadin/local_projects/post-database-era/datasets/{timestamp}__data__stackoverflow-forum-tag-mix__stackoverflow__quarterly-trends.csv"
    
    fieldnames = ['platform_tag', 'api_tag', 'tag_category', 'count', 'month', 
                 'total_score', 'total_views', 'answered_count', 'answer_rate', 
                 'avg_score', 'avg_views']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    logger.info(f"Quarterly trends saved to {filename}")
    logger.info(f"Total records: {len(results)}")

if __name__ == "__main__":
    main()