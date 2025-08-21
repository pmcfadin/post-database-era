#!/usr/bin/env python3
"""
Data collection script for table format specification adoption.
Focuses on Iceberg and Delta Lake version adoption in production.
"""

import requests
import json
import csv
import yaml
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin
import time

def collect_iceberg_releases():
    """Collect Iceberg specification releases and features."""
    releases = []
    
    try:
        # GitHub API for Apache Iceberg releases
        url = "https://api.github.com/repos/apache/iceberg/releases"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            for release in data[:20]:  # Last 20 releases
                version = release['tag_name'].replace('apache-iceberg-', '').replace('v', '')
                
                # Extract major features from release notes
                features = extract_iceberg_features(release.get('body', ''))
                
                releases.append({
                    'dataset_id': f"iceberg-spec-{version}",
                    'format': 'Apache Iceberg',
                    'spec_version': version,
                    'features': '; '.join(features),
                    'release_date': release['published_at'][:10],
                    'download_count': release.get('download_count', 0),
                    'is_prerelease': release['prerelease']
                })
                
    except Exception as e:
        print(f"Error collecting Iceberg releases: {e}")
    
    return releases

def extract_iceberg_features(release_notes):
    """Extract key features from Iceberg release notes."""
    features = []
    
    if not release_notes:
        return features
        
    # Common Iceberg features to look for
    feature_patterns = {
        'row-level-deletes': r'row.level.delet|delete.support|row.delet',
        'spec-v2': r'spec.v2|specification.v2|table.spec.v2',
        'spec-v3': r'spec.v3|specification.v3|table.spec.v3',
        'column-mapping': r'column.mapping|field.mapping',
        'partition-evolution': r'partition.evolution|hidden.partition',
        'schema-evolution': r'schema.evolution|schema.chang',
        'time-travel': r'time.travel|snapshot.read',
        'branching': r'branch|tag.support',
        'encryption': r'encrypt|security',
        'merge-on-read': r'merge.on.read|mor',
        'copy-on-write': r'copy.on.write|cow'
    }
    
    text = release_notes.lower()
    
    for feature, pattern in feature_patterns.items():
        if re.search(pattern, text):
            features.append(feature)
    
    return features

def collect_delta_releases():
    """Collect Delta Lake protocol versions and features."""
    releases = []
    
    try:
        # GitHub API for Delta Lake releases
        url = "https://api.github.com/repos/delta-io/delta/releases"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            for release in data[:20]:  # Last 20 releases
                version = release['tag_name'].replace('v', '')
                
                # Extract features from release notes
                features = extract_delta_features(release.get('body', ''))
                
                releases.append({
                    'dataset_id': f"delta-protocol-{version}",
                    'format': 'Delta Lake',
                    'spec_version': version,
                    'features': '; '.join(features),
                    'release_date': release['published_at'][:10],
                    'download_count': release.get('download_count', 0),
                    'is_prerelease': release['prerelease']
                })
                
    except Exception as e:
        print(f"Error collecting Delta releases: {e}")
    
    return releases

def extract_delta_features(release_notes):
    """Extract key features from Delta Lake release notes."""
    features = []
    
    if not release_notes:
        return features
        
    # Common Delta Lake features to look for
    feature_patterns = {
        'liquid-clustering': r'liquid.clustering|liquid.cluster',
        'deletion-vectors': r'deletion.vector|dv.support',
        'column-mapping': r'column.mapping|field.mapping',
        'change-data-feed': r'change.data.feed|cdf',
        'optimize': r'optimize|compaction',
        'vacuum': r'vacuum|cleanup',
        'merge': r'merge.into|upsert',
        'streaming': r'streaming|incremental',
        'time-travel': r'time.travel|version.travel',
        'clone': r'clone|deep.clone|shallow.clone',
        'restore': r'restore|rollback',
        'constraints': r'constraint|check.constraint',
        'generated-columns': r'generated.column|computed.column'
    }
    
    text = release_notes.lower()
    
    for feature, pattern in feature_patterns.items():
        if re.search(pattern, text):
            features.append(feature)
    
    return features

def collect_hudi_releases():
    """Collect Apache Hudi version information."""
    releases = []
    
    try:
        url = "https://api.github.com/repos/apache/hudi/releases"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            for release in data[:15]:  # Last 15 releases
                version = release['tag_name'].replace('release-', '').replace('v', '')
                
                features = extract_hudi_features(release.get('body', ''))
                
                releases.append({
                    'dataset_id': f"hudi-version-{version}",
                    'format': 'Apache Hudi',
                    'spec_version': version,
                    'features': '; '.join(features),
                    'release_date': release['published_at'][:10],
                    'download_count': release.get('download_count', 0),
                    'is_prerelease': release['prerelease']
                })
                
    except Exception as e:
        print(f"Error collecting Hudi releases: {e}")
    
    return releases

def extract_hudi_features(release_notes):
    """Extract key features from Hudi release notes."""
    features = []
    
    if not release_notes:
        return features
        
    feature_patterns = {
        'merge-on-read': r'merge.on.read|mor.table',
        'copy-on-write': r'copy.on.write|cow.table',
        'incremental-query': r'incremental.quer|incremental.read',
        'timeline-service': r'timeline.service|timeline.server',
        'multi-modal-index': r'multi.modal|bloom.filter|column.stats',
        'clustering': r'clustering|layout.optim',
        'compaction': r'compaction|async.compact',
        'cleaner': r'cleaner|retention',
        'metadata-table': r'metadata.table|hudi.metadata',
        'record-level-index': r'record.level.index|rli'
    }
    
    text = release_notes.lower()
    
    for feature, pattern in feature_patterns.items():
        if re.search(pattern, text):
            features.append(feature)
    
    return features

def main():
    """Main data collection function."""
    print("Collecting table format specification adoption data...")
    
    all_releases = []
    
    # Collect from each format
    print("Collecting Iceberg releases...")
    iceberg_data = collect_iceberg_releases()
    all_releases.extend(iceberg_data)
    
    print("Collecting Delta Lake releases...")
    delta_data = collect_delta_releases()
    all_releases.extend(delta_data)
    
    print("Collecting Hudi releases...")
    hudi_data = collect_hudi_releases()
    all_releases.extend(hudi_data)
    
    # Sort by release date
    all_releases.sort(key=lambda x: x['release_date'], reverse=True)
    
    # Save to CSV
    filename = f"/Users/patrickmcfadin/local_projects/post-database-era/datasets/schema-evolution-cadence/2025-08-21__data__spec-adoption__multi-format__version-releases.csv"
    
    if all_releases:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['dataset_id', 'format', 'spec_version', 'features', 'release_date', 'download_count', 'is_prerelease']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for release in all_releases:
                writer.writerow(release)
        
        print(f"Saved {len(all_releases)} release records to {filename}")
        
        # Create metadata
        create_metadata(filename, len(all_releases))
    
    return all_releases

def create_metadata(filename, row_count):
    """Create metadata file for the dataset."""
    metadata = {
        'dataset': {
            'title': 'Table Format Specification Version Releases',
            'description': 'Release history and feature adoption for Apache Iceberg, Delta Lake, and Apache Hudi',
            'topic': 'schema-evolution-cadence',
            'metric': 'version releases and feature adoption'
        },
        'source': {
            'name': 'GitHub Releases API',
            'url': 'https://api.github.com/repos/{apache/iceberg,delta-io/delta,apache/hudi}/releases',
            'accessed': datetime.now().strftime('%Y-%m-%d'),
            'license': 'Public API data',
            'credibility': 'Tier A'
        },
        'characteristics': {
            'rows': row_count,
            'columns': 7,
            'time_range': '2020 - 2025',
            'update_frequency': 'on new releases',
            'collection_method': 'automated via GitHub API'
        },
        'columns': {
            'dataset_id': {
                'type': 'string',
                'description': 'Unique identifier for each release',
                'unit': 'text'
            },
            'format': {
                'type': 'string', 
                'description': 'Table format name (Iceberg, Delta Lake, Hudi)',
                'unit': 'text'
            },
            'spec_version': {
                'type': 'string',
                'description': 'Version number of the specification/release',
                'unit': 'semver'
            },
            'features': {
                'type': 'string',
                'description': 'Key features introduced in this version',
                'unit': 'semicolon-separated list'
            },
            'release_date': {
                'type': 'date',
                'description': 'Date when version was released',
                'unit': 'YYYY-MM-DD'
            },
            'download_count': {
                'type': 'number',
                'description': 'Number of downloads from GitHub releases',
                'unit': 'count'
            },
            'is_prerelease': {
                'type': 'boolean',
                'description': 'Whether this is a pre-release version',
                'unit': 'true/false'
            }
        },
        'quality': {
            'completeness': '100% for available fields',
            'sample_size': f'{row_count} releases',
            'confidence': 'high',
            'limitations': ['GitHub API rate limits', 'Feature extraction based on release notes text']
        },
        'notes': [
            'Features extracted from release notes using keyword matching',
            'Focus on production-ready features and specification changes',
            'Data represents official releases, not development branches'
        ]
    }
    
    meta_filename = filename.replace('.csv', '.meta.yaml')
    with open(meta_filename, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created metadata file: {meta_filename}")

if __name__ == "__main__":
    main()