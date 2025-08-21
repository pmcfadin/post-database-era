#!/usr/bin/env python3
"""
Practitioner Signal Analysis for Section 9
Analyzes architect surveys and postmortem coding to identify quantitative trends
"""

import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class PractitionerSignalAnalyzer:
    def __init__(self, base_path="/Users/patrickmcfadin/local_projects/post-database-era/datasets/practitioner-signals"):
        self.base_path = base_path
        self.survey_data = None
        self.postmortem_data = None
        
    def load_data(self):
        """Load both survey and postmortem datasets"""
        try:
            # Load survey data
            survey_file = f"{self.base_path}/architect-surveys/2025-08-20__data__architect-surveys__multi-source__architecture-preferences.csv"
            self.survey_data = pd.read_csv(survey_file)
            
            # Load postmortem data
            postmortem_file = f"{self.base_path}/postmortem-coding/2025-08-20__data__postmortems__multi-source__incident-coding.csv"
            self.postmortem_data = pd.read_csv(postmortem_file)
            
            print(f"Loaded {len(self.survey_data)} survey responses and {len(self.postmortem_data)} incident records")
            
        except FileNotFoundError as e:
            print(f"Data file not found: {e}")
            return False
        return True
    
    def analyze_architecture_preferences(self):
        """Analyze current vs preferred architecture distributions"""
        if self.survey_data is None:
            return
        
        print("\n=== ARCHITECTURE PREFERENCE ANALYSIS ===")
        
        # Current architecture distribution
        current_dist = self.survey_data['current_architecture'].value_counts()
        print("\nCurrent Architecture Distribution:")
        for arch, count in current_dist.items():
            pct = (count / len(self.survey_data)) * 100
            print(f"  {arch}: {count} ({pct:.1f}%)")
        
        # Preferred architecture distribution
        preferred_dist = self.survey_data['preferred_architecture'].value_counts()
        print("\nPreferred Architecture Distribution:")
        for arch, count in preferred_dist.items():
            pct = (count / len(self.survey_data)) * 100
            print(f"  {arch}: {count} ({pct:.1f}%)")
        
        # Migration intentions
        print("\nMigration Intentions:")
        for idx, row in self.survey_data.iterrows():
            current = row['current_architecture']
            preferred = row['preferred_architecture']
            if current != preferred:
                print(f"  {current} → {preferred} ({row['respondent_role']})")
        
        return {
            'current_distribution': current_dist.to_dict(),
            'preferred_distribution': preferred_dist.to_dict()
        }
    
    def analyze_adoption_drivers_blockers(self):
        """Analyze key drivers and blockers for architecture adoption"""
        if self.survey_data is None:
            return
        
        print("\n=== ADOPTION DRIVERS & BLOCKERS ANALYSIS ===")
        
        # Primary drivers
        drivers = self.survey_data['adoption_driver_primary'].value_counts()
        print("\nPrimary Adoption Drivers:")
        for driver, count in drivers.items():
            pct = (count / len(self.survey_data)) * 100
            print(f"  {driver}: {count} ({pct:.1f}%)")
        
        # Main blockers
        blockers = self.survey_data['main_blocker'].value_counts()
        print("\nMain Adoption Blockers:")
        for blocker, count in blockers.items():
            pct = (count / len(self.survey_data)) * 100
            print(f"  {blocker}: {count} ({pct:.1f}%)")
        
        # Adoption readiness by role
        print("\nAdoption Readiness by Role:")
        readiness_by_role = self.survey_data.groupby('respondent_role')['adoption_readiness_score'].mean()
        for role, score in readiness_by_role.items():
            print(f"  {role}: {score:.1f}/5.0")
        
        return {
            'drivers': drivers.to_dict(),
            'blockers': blockers.to_dict(),
            'readiness_by_role': readiness_by_role.to_dict()
        }
    
    def analyze_sla_targets(self):
        """Analyze SLA target distributions"""
        if self.survey_data is None:
            return
        
        print("\n=== SLA TARGET ANALYSIS ===")
        
        sla_stats = self.survey_data['sla_target_ms'].describe()
        print(f"\nSLA Target Statistics (milliseconds):")
        print(f"  Mean: {sla_stats['mean']:.1f}ms")
        print(f"  Median: {sla_stats['50%']:.1f}ms")
        print(f"  Min: {sla_stats['min']:.1f}ms")
        print(f"  Max: {sla_stats['max']:.1f}ms")
        
        # SLA targets by architecture preference
        print("\nSLA Targets by Architecture Preference:")
        sla_by_arch = self.survey_data.groupby('preferred_architecture')['sla_target_ms'].agg(['mean', 'median'])
        for arch in sla_by_arch.index:
            mean_sla = sla_by_arch.loc[arch, 'mean']
            median_sla = sla_by_arch.loc[arch, 'median']
            print(f"  {arch}: Mean={mean_sla:.1f}ms, Median={median_sla:.1f}ms")
        
        return sla_by_arch.to_dict()
    
    def analyze_postmortem_patterns(self):
        """Analyze postmortem coding patterns"""
        if self.postmortem_data is None:
            return
        
        print("\n=== POSTMORTEM ANALYSIS ===")
        
        # Architecture impact distribution
        impact_dist = self.postmortem_data['separated_arch_impact'].value_counts()
        print("\nSeparated Architecture Impact Assessment:")
        for impact, count in impact_dist.items():
            pct = (count / len(self.postmortem_data)) * 100
            print(f"  {impact}: {count} ({pct:.1f}%)")
        
        # MTTR by architecture type
        if 'architecture_type' in self.postmortem_data.columns:
            print("\nMTTR by Architecture Type:")
            mttr_by_arch = self.postmortem_data.groupby('architecture_type')['mttr_minutes'].agg(['mean', 'median'])
            for arch in mttr_by_arch.index:
                mean_mttr = mttr_by_arch.loc[arch, 'mean']
                median_mttr = mttr_by_arch.loc[arch, 'median']
                print(f"  {arch}: Mean={mean_mttr:.1f}min, Median={median_mttr:.1f}min")
        
        # Failure domain analysis
        domains = self.postmortem_data['failure_domain'].value_counts()
        print("\nFailure Domain Distribution:")
        for domain, count in domains.items():
            pct = (count / len(self.postmortem_data)) * 100
            print(f"  {domain}: {count} ({pct:.1f}%)")
        
        return {
            'impact_distribution': impact_dist.to_dict(),
            'failure_domains': domains.to_dict()
        }
    
    def generate_summary_statistics(self):
        """Generate overall summary statistics"""
        print("\n=== SUMMARY STATISTICS ===")
        
        if self.survey_data is not None:
            # Architecture preference shift
            coupled_current = (self.survey_data['current_architecture'] == 'Coupled').sum()
            separated_preferred = (self.survey_data['preferred_architecture'] == 'Separated').sum()
            
            print(f"\nArchitecture Trends:")
            print(f"  Currently using Coupled: {coupled_current}/{len(self.survey_data)} ({coupled_current/len(self.survey_data)*100:.1f}%)")
            print(f"  Prefer Separated: {separated_preferred}/{len(self.survey_data)} ({separated_preferred/len(self.survey_data)*100:.1f}%)")
            
            # Average adoption timeline
            avg_adoption_time = self.survey_data['time_to_adopt_months'].mean()
            print(f"  Average adoption timeline: {avg_adoption_time:.1f} months")
        
        if self.postmortem_data is not None:
            # Separation benefit ratio
            positive_impact = (self.postmortem_data['separated_arch_impact'].str.contains('Positive')).sum()
            total_incidents = len(self.postmortem_data)
            benefit_ratio = positive_impact / total_incidents
            
            print(f"\nIncident Analysis:")
            print(f"  Incidents where separation would help: {positive_impact}/{total_incidents} ({benefit_ratio*100:.1f}%)")
            
            # Average MTTR
            avg_mttr = self.postmortem_data['mttr_minutes'].mean()
            print(f"  Average MTTR: {avg_mttr:.1f} minutes")
    
    def export_summary_csv(self):
        """Export key metrics to CSV for further analysis"""
        summary_data = []
        
        if self.survey_data is not None:
            # Add survey summary rows
            arch_prefs = self.survey_data['preferred_architecture'].value_counts()
            for arch, count in arch_prefs.items():
                summary_data.append({
                    'metric_type': 'architecture_preference',
                    'category': arch,
                    'value': count,
                    'percentage': (count / len(self.survey_data)) * 100,
                    'sample_size': len(self.survey_data)
                })
        
        if self.postmortem_data is not None:
            # Add postmortem summary rows
            impact_counts = self.postmortem_data['separated_arch_impact'].value_counts()
            for impact, count in impact_counts.items():
                summary_data.append({
                    'metric_type': 'separation_impact',
                    'category': impact,
                    'value': count,
                    'percentage': (count / len(self.postmortem_data)) * 100,
                    'sample_size': len(self.postmortem_data)
                })
        
        # Save summary
        if summary_data:
            timestamp = datetime.now().strftime('%Y-%m-%d')
            summary_df = pd.DataFrame(summary_data)
            filename = f"{self.base_path}/analysis/{timestamp}__summary__practitioner-signals__quantitative-metrics.csv"
            
            # Create analysis directory if it doesn't exist
            import os
            os.makedirs(f"{self.base_path}/analysis", exist_ok=True)
            
            summary_df.to_csv(filename, index=False)
            print(f"\nSummary exported to: {filename}")

def main():
    analyzer = PractitionerSignalAnalyzer()
    
    if not analyzer.load_data():
        print("Failed to load data. Exiting.")
        return
    
    # Run all analyses
    analyzer.analyze_architecture_preferences()
    analyzer.analyze_adoption_drivers_blockers()
    analyzer.analyze_sla_targets()
    analyzer.analyze_postmortem_patterns()
    analyzer.generate_summary_statistics()
    analyzer.export_summary_csv()

if __name__ == '__main__':
    main()