#!/usr/bin/env python3
"""
Gateway Terms Dataset Analysis
Analyze the collected gateway terminology tracking data
"""

import csv
import pandas as pd
from collections import Counter
from datetime import datetime

def analyze_dataset():
    """Analyze the gateway terms dataset"""
    
    filename = '/Users/patrickmcfadin/local_projects/post-database-era/datasets/2025-08-20__data__gateway-terms__industry-discourse__terminology-tracking.csv'
    
    # Read the data
    data = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    
    print("=== Gateway Terms Dataset Analysis ===\n")
    
    # Basic statistics
    print(f"Total records: {len(data)}")
    print(f"Date range: {min(row['date'] for row in data)} to {max(row['date'] for row in data)}")
    print(f"Average phrase length: {sum(int(row['phrase_word_count']) for row in data) / len(data):.1f} words")
    
    # Term distribution
    print("\n=== Term Distribution ===")
    terms = Counter(row['term_found'] for row in data)
    for term, count in terms.most_common():
        print(f"{term}: {count}")
    
    # Source distribution  
    print("\n=== Source Distribution ===")
    sources = Counter(row['source'] for row in data)
    for source, count in sources.most_common():
        print(f"{source}: {count}")
        
    # Context distribution
    print("\n=== Context Distribution ===")
    contexts = Counter(row['context'] for row in data)
    for context, count in contexts.most_common():
        print(f"{context}: {count}")
    
    # Source credibility analysis
    tier_a_sources = [
        'Gartner', 'Forrester', 'IDC Report', 'AWS Blog', 'Google Cloud Blog', 
        'Microsoft Azure Blog', 'AWS re:Invent', 'Google Cloud Next', 'Microsoft Build'
    ]
    tier_b_sources = ['InfoWorld', 'ZDNet', 'TechCrunch']
    
    tier_a_count = sum(1 for row in data if row['source'] in tier_a_sources)
    tier_b_count = sum(1 for row in data if row['source'] in tier_b_sources)
    
    print(f"\n=== Source Credibility ===")
    print(f"Tier A sources: {tier_a_count} ({tier_a_count/len(data)*100:.1f}%)")
    print(f"Tier B sources: {tier_b_count} ({tier_b_count/len(data)*100:.1f}%)")
    
    # Temporal analysis
    print(f"\n=== Temporal Distribution ===")
    years = Counter(row['date'][:4] for row in data)
    for year, count in sorted(years.items()):
        print(f"{year}: {count}")
    
    # Sample phrases by term
    print(f"\n=== Sample Phrases by Term ===")
    for term in terms.keys():
        phrases = [row['exact_phrase'] for row in data if row['term_found'] == term]
        print(f"\n{term}:")
        for phrase in phrases[:2]:  # Show first 2 examples
            print(f"  - \"{phrase}\"")
    
    return data

if __name__ == "__main__":
    analyze_dataset()