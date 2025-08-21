#!/usr/bin/env python3
"""
Compute-Storage Separation Adoption Analysis (Simple Version)

Analyzes the collected data on database compute-storage separation adoption signals
using only standard library modules to avoid dependency issues.
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict, Counter

class ComputeStorageSeparationAnalysis:
    def __init__(self, datasets_path: str):
        self.datasets_path = datasets_path
        self.timestamp = datetime.now().strftime('%Y-%m-%d')
        
        # Load datasets
        self.architecture_data = self.load_csv_data('architecture-census')
        self.primitives_data = self.load_csv_data('primitives-timeline')
        self.scorecard_data = self.load_csv_data('sku-decoupling-scorecard')
        
        self.analysis_results = {}
    
    def load_csv_data(self, dataset_type: str) -> List[Dict[str, Any]]:
        """Load CSV data based on dataset type"""
        try:
            if dataset_type == 'architecture-census':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__vendors__architecture-census.csv"
            elif dataset_type == 'primitives-timeline':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__cloud-providers__primitives-timeline.csv"
            elif dataset_type == 'sku-decoupling-scorecard':
                filename = f"{self.datasets_path}/{self.timestamp}__data__compute-storage-separation__vendors__sku-decoupling-scorecard.csv"
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)
        except Exception as e:
            print(f"Warning: Could not load {dataset_type} data: {e}")
            return []
    
    def analyze_architecture_patterns(self) -> Dict[str, Any]:
        """Analyze architecture patterns and separation capabilities"""
        if not self.architecture_data:
            return {}
        
        analysis = {}
        
        # Separation capability distribution
        separation_count = Counter(row['compute_storage_separated'] for row in self.architecture_data)
        analysis['separation_distribution'] = dict(separation_count)
        
        # Architecture types
        arch_types = Counter(row['architecture_type'] for row in self.architecture_data)
        analysis['architecture_types'] = dict(arch_types)
        
        # Engine types vs separation
        engine_separation = defaultdict(lambda: defaultdict(int))
        for row in self.architecture_data:
            engine_separation[row['engine_type']][row['compute_storage_separated']] += 1
        analysis['engine_separation_matrix'] = {k: dict(v) for k, v in engine_separation.items()}
        
        # Vendor separation capability
        vendor_stats = defaultdict(lambda: {'total': 0, 'separated': 0})
        for row in self.architecture_data:
            vendor_stats[row['vendor']]['total'] += 1
            if row['compute_storage_separated'] == 'Yes':
                vendor_stats[row['vendor']]['separated'] += 1
        
        vendor_separation = {}
        for vendor, stats in vendor_stats.items():
            percentage = round(stats['separated'] / stats['total'] * 100, 1) if stats['total'] > 0 else 0
            vendor_separation[vendor] = percentage
        analysis['vendor_separation_percentage'] = vendor_separation
        
        # Launch year trends
        year_stats = defaultdict(lambda: {'total': 0, 'separated': 0})
        for row in self.architecture_data:
            year = int(row['launch_year'])
            year_stats[year]['total'] += 1
            if row['compute_storage_separated'] == 'Yes':
                year_stats[year]['separated'] += 1
        
        launch_trends = {}
        for year, stats in year_stats.items():
            separation_rate = round(stats['separated'] / stats['total'] * 100, 1) if stats['total'] > 0 else 0
            launch_trends[year] = {
                'total_count': stats['total'],
                'separated_count': stats['separated'],
                'separation_rate': separation_rate
            }
        analysis['launch_year_trends'] = launch_trends
        
        return analysis
    
    def analyze_primitives_evolution(self) -> Dict[str, Any]:
        """Analyze cloud primitive evolution timeline"""
        if not self.primitives_data:
            return {}
        
        analysis = {}
        
        # Timeline by category
        category_timeline = defaultdict(lambda: defaultdict(int))
        for row in self.primitives_data:
            year = int(row['launch_year'])
            category_timeline[row['primitive_category']][year] += 1
        analysis['category_timeline'] = {k: dict(v) for k, v in category_timeline.items()}
        
        # Provider innovation timeline
        provider_timeline = defaultdict(lambda: defaultdict(int))
        for row in self.primitives_data:
            year = int(row['launch_year'])
            provider_timeline[row['cloud_provider']][year] += 1
        analysis['provider_timeline'] = {k: dict(v) for k, v in provider_timeline.items()}
        
        # Key milestones by decade
        decade_data = {'2000s': [], '2010s': [], '2020s': []}
        for row in self.primitives_data:
            year = int(row['launch_year'])
            if 2000 <= year < 2010:
                decade_data['2000s'].append(row)
            elif 2010 <= year < 2020:
                decade_data['2010s'].append(row)
            elif year >= 2020:
                decade_data['2020s'].append(row)
        
        decade_milestones = {}
        for decade, data in decade_data.items():
            # Sort by year and take top 3 most recent
            sorted_data = sorted(data, key=lambda x: int(x['launch_year']), reverse=True)[:3]
            decade_milestones[decade] = {
                'count': len(data),
                'key_innovations': [
                    {'primitive_name': item['primitive_name'], 'evolution_milestone': item['evolution_milestone']}
                    for item in sorted_data
                ]
            }
        analysis['decade_milestones'] = decade_milestones
        
        # Performance evolution tracking
        performance_keywords = ['IOPS', 'Gbps', 'GB/s', 'latency', 'throughput']
        performance_evolution = []
        for row in self.primitives_data:
            perf_spec = str(row['performance_spec']).lower()
            has_perf = any(keyword.lower() in perf_spec for keyword in performance_keywords)
            if has_perf:
                performance_evolution.append({
                    'year': int(row['launch_year']),
                    'primitive': row['primitive_name'],
                    'performance': row['performance_spec']
                })
        
        # Sort by year
        performance_evolution.sort(key=lambda x: x['year'])
        analysis['performance_evolution'] = performance_evolution
        
        return analysis
    
    def analyze_decoupling_scorecard(self) -> Dict[str, Any]:
        """Analyze SKU decoupling scores and pricing patterns"""
        if not self.scorecard_data:
            return {}
        
        analysis = {}
        
        # Convert scores to numbers
        scores = [int(row['decoupling_score']) for row in self.scorecard_data if row['decoupling_score'].isdigit()]
        
        if scores:
            # Score statistics
            analysis['score_statistics'] = {
                'mean': round(sum(scores) / len(scores), 1),
                'median': sorted(scores)[len(scores)//2],
                'min': min(scores),
                'max': max(scores),
                'count': len(scores)
            }
            
            # Top and bottom performers
            scored_services = [(int(row['decoupling_score']), row['vendor'], row['service']) 
                             for row in self.scorecard_data if row['decoupling_score'].isdigit()]
            scored_services.sort(reverse=True)
            
            analysis['top_performers'] = [
                {'vendor': vendor, 'service': service, 'decoupling_score': score}
                for score, vendor, service in scored_services[:5]
            ]
            
            analysis['bottom_performers'] = [
                {'vendor': vendor, 'service': service, 'decoupling_score': score}
                for score, vendor, service in scored_services[-5:]
            ]
        
        # Vendor average scores
        vendor_scores = defaultdict(list)
        for row in self.scorecard_data:
            if row['decoupling_score'].isdigit():
                vendor_scores[row['vendor']].append(int(row['decoupling_score']))
        
        vendor_averages = {}
        for vendor, scores_list in vendor_scores.items():
            vendor_averages[vendor] = {
                'mean': round(sum(scores_list) / len(scores_list), 1),
                'count': len(scores_list)
            }
        analysis['vendor_average_scores'] = vendor_averages
        
        # Pricing model patterns
        pricing_independence = Counter(row['independent_pricing'] for row in self.scorecard_data)
        analysis['pricing_independence_distribution'] = dict(pricing_independence)
        
        # Autoscaling capabilities
        compute_autoscaling = Counter(row['compute_autoscaling'] for row in self.scorecard_data)
        storage_autoscaling = Counter(row['storage_autoscaling'] for row in self.scorecard_data)
        analysis['autoscaling_capabilities'] = {
            'compute': dict(compute_autoscaling),
            'storage': dict(storage_autoscaling)
        }
        
        # Billing granularity analysis
        billing_granularity = Counter(row['billing_granularity'] for row in self.scorecard_data)
        analysis['billing_granularity_distribution'] = dict(billing_granularity)
        
        return analysis
    
    def generate_cross_dataset_insights(self) -> Dict[str, Any]:
        """Generate insights that span multiple datasets"""
        insights = {}
        
        # Evolution timeline insights
        if self.primitives_data and self.architecture_data:
            # Find earliest primitive and separated service
            primitive_years = [int(row['launch_year']) for row in self.primitives_data]
            separated_services = [row for row in self.architecture_data if row['compute_storage_separated'] == 'Yes']
            separated_years = [int(row['launch_year']) for row in separated_services if separated_services]
            
            if primitive_years and separated_years:
                earliest_primitive = min(primitive_years)
                earliest_separated = min(separated_years)
                
                insights['adoption_lag'] = {
                    'earliest_enabling_primitive': earliest_primitive,
                    'earliest_separated_service': earliest_separated,
                    'lag_years': earliest_separated - earliest_primitive
                }
        
        # Vendor maturity analysis
        if self.architecture_data and self.scorecard_data:
            vendor_maturity = {}
            
            # Get vendor stats from architecture data
            arch_vendor_stats = defaultdict(lambda: {'total': 0, 'separated': 0})
            for row in self.architecture_data:
                arch_vendor_stats[row['vendor']]['total'] += 1
                if row['compute_storage_separated'] == 'Yes':
                    arch_vendor_stats[row['vendor']]['separated'] += 1
            
            # Get vendor scores from scorecard data
            score_vendor_stats = defaultdict(list)
            for row in self.scorecard_data:
                if row['decoupling_score'].isdigit():
                    score_vendor_stats[row['vendor']].append(int(row['decoupling_score']))
            
            # Combine data
            all_vendors = set(arch_vendor_stats.keys()) | set(score_vendor_stats.keys())
            for vendor in all_vendors:
                arch_stats = arch_vendor_stats.get(vendor, {'total': 0, 'separated': 0})
                score_stats = score_vendor_stats.get(vendor, [])
                
                separation_rate = round(arch_stats['separated'] / arch_stats['total'] * 100, 1) if arch_stats['total'] > 0 else 0
                avg_score = round(sum(score_stats) / len(score_stats), 1) if score_stats else 0
                
                vendor_maturity[vendor] = {
                    'separation_rate': separation_rate,
                    'average_decoupling_score': avg_score,
                    'service_count': arch_stats['total']
                }
            
            insights['vendor_maturity'] = vendor_maturity
        
        # Infrastructure readiness
        if self.primitives_data:
            storage_count = sum(1 for row in self.primitives_data 
                              if 'storage' in row['primitive_category'].lower())
            networking_count = sum(1 for row in self.primitives_data 
                                 if 'networking' in row['primitive_category'].lower())
            
            storage_years = [int(row['launch_year']) for row in self.primitives_data 
                           if 'storage' in row['primitive_category'].lower()]
            networking_years = [int(row['launch_year']) for row in self.primitives_data 
                              if 'networking' in row['primitive_category'].lower()]
            
            insights['infrastructure_readiness'] = {
                'storage_primitives_count': storage_count,
                'networking_primitives_count': networking_count,
                'first_storage_primitive': min(storage_years) if storage_years else None,
                'first_networking_primitive': min(networking_years) if networking_years else None
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
                    sorted_vendors = sorted(arch['vendor_separation_percentage'].items(), 
                                          key=lambda x: x[1], reverse=True)
                    for vendor, percentage in sorted_vendors:
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
                    sorted_scores = sorted(scorecard['vendor_average_scores'].items(), 
                                         key=lambda x: x[1]['mean'], reverse=True)
                    for vendor, data in sorted_scores:
                        f.write(f"- **{vendor}:** {data['mean']}/100 (based on {data['count']} services)\n")
                    f.write("\n")
            
            # Market Implications
            f.write("## Market Implications\n\n")
            if 'cross_dataset_insights' in self.analysis_results:
                insights = self.analysis_results['cross_dataset_insights']
                
                if 'vendor_maturity' in insights:
                    f.write("### Vendor Maturity Analysis\n")
                    sorted_maturity = sorted(insights['vendor_maturity'].items(), 
                                           key=lambda x: x[1]['average_decoupling_score'], reverse=True)
                    for vendor, data in sorted_maturity:
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