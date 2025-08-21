#!/usr/bin/env python3
"""
Compute-Storage Separation Adoption Analysis

Analyzes the collected data on database compute-storage separation adoption signals
across the three key datasets:
1. Vendor Architecture Census
2. Cloud Primitives Timeline  
3. SKU Decoupling Scorecard

Generates insights on adoption patterns, evolution timeline, and current state.
"""

import csv
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import yaml
import matplotlib.pyplot as plt
import seaborn as sns

class ComputeStorageSeparationAnalysis:
    def __init__(self, datasets_path: str):
        self.datasets_path = datasets_path
        self.timestamp = datetime.now().strftime('%Y-%m-%d')
        
        # Load datasets
        self.architecture_data = self.load_csv_data('architecture-census')
        self.primitives_data = self.load_csv_data('primitives-timeline')
        self.scorecard_data = self.load_csv_data('sku-decoupling-scorecard')
        
        self.analysis_results = {}
    
    def load_csv_data(self, dataset_type: str) -> pd.DataFrame:
        """Load CSV data based on dataset type"""
        try:
            if dataset_type == 'architecture-census':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__vendors__architecture-census.csv"
            elif dataset_type == 'primitives-timeline':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__cloud-providers__primitives-timeline.csv"
            elif dataset_type == 'sku-decoupling-scorecard':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__vendors__sku-decoupling-scorecard.csv"
            
            return pd.read_csv(filename)
        except Exception as e:
            print(f"Warning: Could not load {dataset_type} data: {e}")
            return pd.DataFrame()
    
    def analyze_architecture_patterns(self) -> Dict[str, Any]:
        """Analyze architecture patterns and separation capabilities"""
        if self.architecture_data.empty:
            return {}
        
        analysis = {}
        
        # Separation capability distribution
        separation_dist = self.architecture_data['compute_storage_separated'].value_counts()
        analysis['separation_distribution'] = separation_dist.to_dict()
        
        # Architecture types
        arch_types = self.architecture_data['architecture_type'].value_counts()
        analysis['architecture_types'] = arch_types.to_dict()
        
        # Engine types vs separation
        engine_separation = pd.crosstab(
            self.architecture_data['engine_type'],
            self.architecture_data['compute_storage_separated']
        )
        analysis['engine_separation_matrix'] = engine_separation.to_dict()
        
        # Vendor separation capability
        vendor_separation = self.architecture_data.groupby('vendor')['compute_storage_separated'].apply(
            lambda x: (x == 'Yes').sum() / len(x) * 100
        ).round(1)
        analysis['vendor_separation_percentage'] = vendor_separation.to_dict()
        
        # Launch year trends
        launch_trends = self.architecture_data.groupby('launch_year').agg({
            'compute_storage_separated': lambda x: (x == 'Yes').sum(),
            'product': 'count'
        }).rename(columns={'compute_storage_separated': 'separated_count', 'product': 'total_count'})
        launch_trends['separation_rate'] = (launch_trends['separated_count'] / launch_trends['total_count'] * 100).round(1)
        analysis['launch_year_trends'] = launch_trends.to_dict()
        
        return analysis
    
    def analyze_primitives_evolution(self) -> Dict[str, Any]:
        """Analyze cloud primitive evolution timeline"""
        if self.primitives_data.empty:
            return {}
        
        analysis = {}
        
        # Timeline by category
        category_timeline = self.primitives_data.groupby(['primitive_category', 'launch_year']).size().unstack(fill_value=0)
        analysis['category_timeline'] = category_timeline.to_dict()
        
        # Provider innovation timeline
        provider_timeline = self.primitives_data.groupby(['cloud_provider', 'launch_year']).size().unstack(fill_value=0)
        analysis['provider_timeline'] = provider_timeline.to_dict()
        
        # Key milestones by decade
        decade_milestones = {}
        for decade in ['2000s', '2010s', '2020s']:
            if decade == '2000s':
                year_filter = (self.primitives_data['launch_year'] >= 2000) & (self.primitives_data['launch_year'] < 2010)
            elif decade == '2010s':
                year_filter = (self.primitives_data['launch_year'] >= 2010) & (self.primitives_data['launch_year'] < 2020)
            else:
                year_filter = (self.primitives_data['launch_year'] >= 2020)
            
            decade_data = self.primitives_data[year_filter]
            decade_milestones[decade] = {
                'count': len(decade_data),
                'key_innovations': decade_data.nlargest(3, 'launch_year')[['primitive_name', 'evolution_milestone']].to_dict('records')
            }
        
        analysis['decade_milestones'] = decade_milestones
        
        # Performance evolution
        performance_keywords = ['IOPS', 'Gbps', 'GB/s', 'latency', 'throughput']
        performance_evolution = []
        for _, row in self.primitives_data.iterrows():
            perf_spec = str(row['performance_spec']).lower()
            has_perf = any(keyword.lower() in perf_spec for keyword in performance_keywords)
            if has_perf:
                performance_evolution.append({
                    'year': row['launch_year'],
                    'primitive': row['primitive_name'],
                    'performance': row['performance_spec']
                })
        
        analysis['performance_evolution'] = performance_evolution
        
        return analysis
    
    def analyze_decoupling_scorecard(self) -> Dict[str, Any]:
        """Analyze SKU decoupling scores and pricing patterns"""
        if self.scorecard_data.empty:
            return {}
        
        analysis = {}
        
        # Score distribution
        score_stats = {
            'mean': self.scorecard_data['decoupling_score'].mean(),
            'median': self.scorecard_data['decoupling_score'].median(),
            'std': self.scorecard_data['decoupling_score'].std(),
            'min': self.scorecard_data['decoupling_score'].min(),
            'max': self.scorecard_data['decoupling_score'].max()
        }
        analysis['score_statistics'] = {k: round(v, 1) for k, v in score_stats.items()}
        
        # Top and bottom performers
        analysis['top_performers'] = self.scorecard_data.nlargest(5, 'decoupling_score')[
            ['vendor', 'service', 'decoupling_score']
        ].to_dict('records')
        
        analysis['bottom_performers'] = self.scorecard_data.nsmallest(5, 'decoupling_score')[
            ['vendor', 'service', 'decoupling_score']
        ].to_dict('records')
        
        # Vendor average scores
        vendor_scores = self.scorecard_data.groupby('vendor')['decoupling_score'].agg(['mean', 'count']).round(1)
        analysis['vendor_average_scores'] = vendor_scores.to_dict()
        
        # Pricing model patterns
        pricing_independence = self.scorecard_data['independent_pricing'].value_counts()
        analysis['pricing_independence_distribution'] = pricing_independence.to_dict()
        
        # Autoscaling capabilities
        compute_autoscaling = self.scorecard_data['compute_autoscaling'].value_counts()
        storage_autoscaling = self.scorecard_data['storage_autoscaling'].value_counts()
        analysis['autoscaling_capabilities'] = {
            'compute': compute_autoscaling.to_dict(),
            'storage': storage_autoscaling.to_dict()
        }
        
        # Billing granularity analysis
        billing_granularity = self.scorecard_data['billing_granularity'].value_counts()
        analysis['billing_granularity_distribution'] = billing_granularity.to_dict()
        
        # Score correlation with features
        numeric_cols = ['decoupling_score']
        for col in ['independent_pricing', 'compute_autoscaling', 'storage_autoscaling', 'elastic_scaling']:
            if col in self.scorecard_data.columns:
                # Convert Yes/No to 1/0 for correlation
                yes_no_map = {'Yes': 1, 'No': 0, 'Partial': 0.5, 'Limited': 0.25}
                numeric_data = self.scorecard_data[col].map(yes_no_map)
                correlation = numeric_data.corr(self.scorecard_data['decoupling_score'])
                analysis[f'{col}_correlation'] = round(correlation, 3)
        
        return analysis
    
    def generate_cross_dataset_insights(self) -> Dict[str, Any]:
        """Generate insights that span multiple datasets"""
        insights = {}
        
        # Evolution timeline insights
        if not self.primitives_data.empty and not self.architecture_data.empty:
            # Compare primitive availability vs service adoption
            earliest_primitive = self.primitives_data['launch_year'].min()
            earliest_separated_service = self.architecture_data[
                self.architecture_data['compute_storage_separated'] == 'Yes'
            ]['launch_year'].min()
            
            insights['adoption_lag'] = {
                'earliest_enabling_primitive': int(earliest_primitive),
                'earliest_separated_service': int(earliest_separated_service),
                'lag_years': int(earliest_separated_service - earliest_primitive)
            }
        
        # Vendor maturity analysis
        if not self.architecture_data.empty and not self.scorecard_data.empty:
            # Merge architecture and scorecard data
            vendor_maturity = {}
            for vendor in self.architecture_data['vendor'].unique():
                arch_data = self.architecture_data[self.architecture_data['vendor'] == vendor]
                score_data = self.scorecard_data[self.scorecard_data['vendor'] == vendor]
                
                separated_services = (arch_data['compute_storage_separated'] == 'Yes').sum()
                total_services = len(arch_data)
                avg_score = score_data['decoupling_score'].mean() if not score_data.empty else 0
                
                vendor_maturity[vendor] = {
                    'separation_rate': round(separated_services / total_services * 100, 1),
                    'average_decoupling_score': round(avg_score, 1),
                    'service_count': total_services
                }
            
            insights['vendor_maturity'] = vendor_maturity
        
        # Market evolution patterns
        if not self.primitives_data.empty:
            storage_primitives = self.primitives_data[
                self.primitives_data['primitive_category'].str.contains('Storage', case=False)
            ]
            networking_primitives = self.primitives_data[
                self.primitives_data['primitive_category'].str.contains('Networking', case=False)
            ]
            
            insights['infrastructure_readiness'] = {
                'storage_primitives_count': len(storage_primitives),
                'networking_primitives_count': len(networking_primitives),
                'first_storage_primitive': storage_primitives['launch_year'].min() if not storage_primitives.empty else None,
                'first_networking_primitive': networking_primitives['launch_year'].min() if not networking_primitives.empty else None
            }
        
        return insights
    
    def run_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis across all datasets"""
        print("Running compute-storage separation adoption analysis...")
        
        self.analysis_results = {
            'analysis_metadata': {
                'timestamp': datetime.now().isoformat(),
                'datasets_analyzed': {
                    'architecture_census': len(self.architecture_data),
                    'primitives_timeline': len(self.primitives_data),
                    'sku_decoupling_scorecard': len(self.scorecard_data)
                }
            },
            'architecture_patterns': self.analyze_architecture_patterns(),
            'primitives_evolution': self.analyze_primitives_evolution(),
            'decoupling_scorecard': self.analyze_decoupling_scorecard(),
            'cross_dataset_insights': self.generate_cross_dataset_insights()
        }
        
        return self.analysis_results
    
    def save_analysis(self, output_path: str):
        """Save analysis results to JSON and generate summary"""
        # Save full analysis as JSON
        json_filename = f"{output_path}/{self.timestamp}__analysis__compute-storage-separation__adoption-signals.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        # Generate markdown summary
        summary_filename = f"{output_path}/{self.timestamp}__analysis__compute-storage-separation__adoption-signals.md"
        self.generate_markdown_summary(summary_filename)
        
        print(f"Analysis saved to:")
        print(f"  - {json_filename}")
        print(f"  - {summary_filename}")
        
        return json_filename, summary_filename
    
    def generate_markdown_summary(self, filename: str):
        """Generate markdown summary of key findings"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Database Compute-Storage Separation Adoption Analysis\n\n")
            f.write(f"**Analysis Date:** {self.timestamp}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            
            if 'cross_dataset_insights' in self.analysis_results:
                insights = self.analysis_results['cross_dataset_insights']
                if 'adoption_lag' in insights:
                    lag = insights['adoption_lag']
                    f.write(f"- **Infrastructure-to-Adoption Lag:** {lag['lag_years']} years between first enabling primitive ({lag['earliest_enabling_primitive']}) and first separated service ({lag['earliest_separated_service']})\n")
            
            if 'decoupling_scorecard' in self.analysis_results:
                scorecard = self.analysis_results['decoupling_scorecard']
                if 'score_statistics' in scorecard:
                    stats = scorecard['score_statistics']
                    f.write(f"- **Decoupling Maturity:** Average score {stats['mean']}/100, median {stats['median']}/100\n")
                
                if 'top_performers' in scorecard:
                    top = scorecard['top_performers'][0]
                    f.write(f"- **Leading Implementation:** {top['vendor']} {top['service']} (Score: {top['decoupling_score']}/100)\n")
            
            # Architecture Patterns
            f.write("\n## Architecture Patterns\n\n")
            if 'architecture_patterns' in self.analysis_results:
                arch = self.analysis_results['architecture_patterns']
                
                if 'separation_distribution' in arch:
                    f.write("### Compute-Storage Separation Distribution\n")
                    for level, count in arch['separation_distribution'].items():
                        f.write(f"- **{level}:** {count} services\n")
                    f.write("\n")
                
                if 'vendor_separation_percentage' in arch:
                    f.write("### Vendor Separation Capabilities\n")
                    for vendor, percentage in sorted(arch['vendor_separation_percentage'].items(), 
                                                   key=lambda x: x[1], reverse=True):
                        f.write(f"- **{vendor}:** {percentage}% of services support separation\n")
                    f.write("\n")
            
            # Infrastructure Evolution
            f.write("## Infrastructure Evolution Timeline\n\n")
            if 'primitives_evolution' in self.analysis_results:
                primitives = self.analysis_results['primitives_evolution']
                
                if 'decade_milestones' in primitives:
                    f.write("### Key Milestones by Decade\n")
                    for decade, data in primitives['decade_milestones'].items():
                        f.write(f"\n#### {decade}\n")
                        f.write(f"- **Total Primitives:** {data['count']}\n")
                        if 'key_innovations' in data:
                            f.write("- **Key Innovations:**\n")
                            for innovation in data['key_innovations']:
                                f.write(f"  - {innovation['primitive_name']}: {innovation['evolution_milestone']}\n")
            
            # Pricing Model Evolution
            f.write("\n## Pricing Model Evolution\n\n")
            if 'decoupling_scorecard' in self.analysis_results:
                scorecard = self.analysis_results['decoupling_scorecard']
                
                if 'pricing_independence_distribution' in scorecard:
                    f.write("### Pricing Independence\n")
                    for level, count in scorecard['pricing_independence_distribution'].items():
                        f.write(f"- **{level}:** {count} services\n")
                    f.write("\n")
                
                if 'vendor_average_scores' in scorecard:
                    f.write("### Vendor Decoupling Scores\n")
                    scores = scorecard['vendor_average_scores']['mean']
                    for vendor, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                        f.write(f"- **{vendor}:** {score}/100\n")
                    f.write("\n")
            
            # Market Implications
            f.write("## Market Implications\n\n")
            if 'cross_dataset_insights' in self.analysis_results:
                insights = self.analysis_results['cross_dataset_insights']
                
                if 'vendor_maturity' in insights:
                    f.write("### Vendor Maturity Analysis\n")
                    maturity = insights['vendor_maturity']
                    for vendor, data in sorted(maturity.items(), 
                                             key=lambda x: x[1]['average_decoupling_score'], reverse=True):
                        f.write(f"- **{vendor}:** {data['separation_rate']}% separation rate, ")
                        f.write(f"{data['average_decoupling_score']}/100 avg score ")
                        f.write(f"({data['service_count']} services)\n")
            
            f.write("\n---\n")
            f.write(f"*Analysis generated on {self.timestamp} from database compute-storage separation research datasets.*\n")

def main():
    # Set up paths
    base_path = "/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation"
    datasets_path = f"{base_path}/datasets"
    
    # Run analysis
    analyzer = ComputeStorageSeparationAnalysis(datasets_path)
    results = analyzer.run_analysis()
    
    # Save results
    json_file, md_file = analyzer.save_analysis(datasets_path)
    
    print("\nCompute-Storage Separation Adoption Analysis completed!")
    print(f"\nKey Findings:")
    
    # Print summary statistics
    if 'decoupling_scorecard' in results:
        scorecard = results['decoupling_scorecard']
        if 'score_statistics' in scorecard:
            stats = scorecard['score_statistics']
            print(f"- Average decoupling score: {stats['mean']}/100")
            print(f"- Score range: {stats['min']}-{stats['max']}")
        
        if 'top_performers' in scorecard:
            print("\n- Top 3 decoupling implementations:")
            for i, performer in enumerate(scorecard['top_performers'][:3], 1):
                print(f"  {i}. {performer['vendor']} {performer['service']}: {performer['decoupling_score']}/100")
    
    if 'cross_dataset_insights' in results:
        insights = results['cross_dataset_insights']
        if 'adoption_lag' in insights:
            lag = insights['adoption_lag']
            print(f"\n- Infrastructure readiness to adoption lag: {lag['lag_years']} years")

if __name__ == "__main__":
    main()