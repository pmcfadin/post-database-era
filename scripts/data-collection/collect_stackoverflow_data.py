#!/usr/bin/env python3
"""
Stack Overflow Tag Mix Data Collector
Collects data on multi-API and gateway-related tags to track developer attention shifts
"""

import requests
import json
import csv
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StackOverflowCollector:
    def __init__(self):
        self.base_url = "https://api.stackexchange.com/2.3"
        self.site = "stackoverflow"
        
        # Target tags to track
        self.multi_api_tags = [
            "cosmos-db", "mongodb", "unified-gateway", "multi-api",
            "azure-cosmosdb", "aws-documentdb", "mongodb-atlas", "datastax"
        ]
        
        self.cross_api_tags = [
            "sql+nosql", "graph+document", "search+analytics", 
            "database-gateway", "query-router", "api-gateway"
        ]
        
        self.platform_tags = [
            "azure-cosmosdb", "aws-documentdb", "mongodb-atlas", 
            "datastax", "firebase", "amazon-dynamodb"
        ]
        
        self.gateway_terms = [
            "api-gateway", "database-gateway", "query-router",
            "unified-gateway", "multi-model", "polyglot-persistence"
        ]
        
        # Rate limiting
        self.request_delay = 0.1  # 100ms between requests
        
    def search_tags(self, tag_name: str, fromdate: int = None, todate: int = None) -> Dict[str, Any]:
        """Search for tag information and question counts"""
        params = {
            'site': self.site,
            'filter': 'default',
            'order': 'desc',
            'sort': 'creation',
            'pagesize': 100
        }
        
        if fromdate:
            params['fromdate'] = fromdate
        if todate:
            params['todate'] = todate
            
        # URL encode the tag for complex searches
        encoded_tag = urllib.parse.quote(tag_name)
        url = f"{self.base_url}/tags/{encoded_tag}/info"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(self.request_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for tag {tag_name}: {e}")
            return {}
            
    def search_questions_by_tag(self, tag: str, fromdate: int = None, todate: int = None) -> Dict[str, Any]:
        """Search for questions with specific tags"""
        params = {
            'site': self.site,
            'tagged': tag,
            'filter': 'default',
            'order': 'desc',
            'sort': 'creation',
            'pagesize': 100
        }
        
        if fromdate:
            params['fromdate'] = fromdate
        if todate:
            params['todate'] = todate
            
        url = f"{self.base_url}/questions"
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(self.request_delay)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching questions for tag {tag}: {e}")
            return {}
    
    def get_tag_stats(self, tag: str) -> Dict[str, Any]:
        """Get detailed statistics for a tag"""
        url = f"{self.base_url}/tags/{urllib.parse.quote(tag)}/info"
        params = {'site': self.site}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(self.request_delay)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                return data['items'][0]
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tag stats for {tag}: {e}")
            return {}
    
    def collect_monthly_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Collect monthly question counts for all target tags"""
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            # Calculate month boundaries
            month_start = current_date.replace(day=1)
            if current_date.month == 12:
                month_end = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
            
            fromdate = int(month_start.timestamp())
            todate = int(month_end.timestamp())
            month_str = current_date.strftime("%Y-%m")
            
            logger.info(f"Collecting data for {month_str}")
            
            # Collect data for all tag categories
            all_tags = (self.multi_api_tags + self.cross_api_tags + 
                       self.platform_tags + self.gateway_terms)
            
            for tag in all_tags:
                # Get question count for this tag in this month
                questions_data = self.search_questions_by_tag(tag, fromdate, todate)
                
                if 'items' in questions_data:
                    question_count = len(questions_data['items'])
                    
                    # Calculate additional metrics
                    total_score = sum(q.get('score', 0) for q in questions_data['items'])
                    total_views = sum(q.get('view_count', 0) for q in questions_data['items'])
                    answered_count = sum(1 for q in questions_data['items'] if q.get('is_answered', False))
                    
                    # Determine tag category
                    if tag in self.multi_api_tags:
                        category = "multi-api"
                    elif tag in self.cross_api_tags:
                        category = "cross-api"
                    elif tag in self.platform_tags:
                        category = "platform"
                    else:
                        category = "gateway"
                    
                    result = {
                        'platform_tag': 'stackoverflow',
                        'api_tag': tag,
                        'tag_category': category,
                        'count': question_count,
                        'month': month_str,
                        'total_score': total_score,
                        'total_views': total_views,
                        'answered_count': answered_count,
                        'answer_rate': answered_count / question_count if question_count > 0 else 0,
                        'avg_score': total_score / question_count if question_count > 0 else 0,
                        'avg_views': total_views / question_count if question_count > 0 else 0
                    }
                    
                    results.append(result)
                    logger.info(f"  {tag}: {question_count} questions")
                
                # Small delay to respect rate limits
                time.sleep(self.request_delay)
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return results
    
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str):
        """Save collected data to CSV file"""
        if not data:
            logger.warning("No data to save")
            return
            
        fieldnames = ['platform_tag', 'api_tag', 'tag_category', 'count', 'month', 
                     'total_score', 'total_views', 'answered_count', 'answer_rate', 
                     'avg_score', 'avg_views']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Data saved to {filename}")

def main():
    collector = StackOverflowCollector()
    
    # Collect data for the past 24 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # ~24 months
    
    logger.info(f"Collecting Stack Overflow data from {start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}")
    
    # Collect data
    data = collector.collect_monthly_data(start_date, end_date)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"/Users/patrickmcfadin/local_projects/post-database-era/datasets/{timestamp}__data__stackoverflow-forum-tag-mix__stackoverflow__question-trends.csv"
    collector.save_to_csv(data, filename)
    
    logger.info(f"Collection complete. {len(data)} records saved.")

if __name__ == "__main__":
    main()