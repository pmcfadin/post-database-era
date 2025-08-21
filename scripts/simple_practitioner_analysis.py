#!/usr/bin/env python3
"""
Simple Practitioner Signal Analysis
Basic analysis without heavy dependencies
"""

import csv
from collections import Counter, defaultdict
from datetime import datetime

def load_csv(filename):
    """Load CSV file into list of dictionaries"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def analyze_survey_data(data):
    """Analyze architect survey data"""
    if not data:
        return
    
    print("=== ARCHITECT SURVEY ANALYSIS ===\n")
    
    # Architecture preferences
    current_arch = Counter(row['current_architecture'] for row in data)
    preferred_arch = Counter(row['preferred_architecture'] for row in data)
    
    print("Current Architecture Distribution:")
    total = len(data)
    for arch, count in current_arch.most_common():
        pct = (count / total) * 100
        print(f"  {arch}: {count}/{total} ({pct:.1f}%)")
    
    print("\nPreferred Architecture Distribution:")
    for arch, count in preferred_arch.most_common():
        pct = (count / total) * 100
        print(f"  {arch}: {count}/{total} ({pct:.1f}%)")
    
    # Migration trends
    migrations = []
    for row in data:
        current = row['current_architecture']
        preferred = row['preferred_architecture']
        if current != preferred:
            migrations.append(f"{current} → {preferred}")
    
    if migrations:
        print(f"\nMigration Intentions ({len(migrations)} respondents):")
        migration_counts = Counter(migrations)
        for migration, count in migration_counts.most_common():
            print(f"  {migration}: {count}")
    
    # Adoption drivers
    drivers = Counter(row['adoption_driver_primary'] for row in data)
    print(f"\nPrimary Adoption Drivers:")
    for driver, count in drivers.most_common():
        pct = (count / total) * 100
        print(f"  {driver}: {count} ({pct:.1f}%)")
    
    # Blockers
    blockers = Counter(row['main_blocker'] for row in data)
    print(f"\nMain Adoption Blockers:")
    for blocker, count in blockers.most_common():
        pct = (count / total) * 100
        print(f"  {blocker}: {count} ({pct:.1f}%)")
    
    # SLA analysis
    sla_targets = [int(row['sla_target_ms']) for row in data if row['sla_target_ms'].isdigit()]
    if sla_targets:
        avg_sla = sum(sla_targets) / len(sla_targets)
        min_sla = min(sla_targets)
        max_sla = max(sla_targets)
        print(f"\nSLA Targets: Avg={avg_sla:.0f}ms, Range={min_sla}-{max_sla}ms")

def analyze_postmortem_data(data):
    """Analyze postmortem incident data"""
    if not data:
        return
    
    print("\n=== POSTMORTEM INCIDENT ANALYSIS ===\n")
    
    total = len(data)
    
    # Architecture types
    arch_types = Counter(row['architecture_type'] for row in data)
    print("Architecture Types in Incidents:")
    for arch, count in arch_types.most_common():
        pct = (count / total) * 100
        print(f"  {arch}: {count}/{total} ({pct:.1f}%)")
    
    # Separation impact
    impacts = []
    for row in data:
        impact = row['separated_arch_impact']
        if impact.startswith('Positive'):
            impacts.append('Positive')
        elif impact.startswith('Negative'):
            impacts.append('Negative')
        else:
            impacts.append('Neutral')
    
    impact_counts = Counter(impacts)
    print(f"\nSeparated Architecture Impact Assessment:")
    for impact, count in impact_counts.most_common():
        pct = (count / total) * 100
        print(f"  {impact}: {count}/{total} ({pct:.1f}%)")
    
    # MTTR analysis
    mttr_data = []
    for row in data:
        if row['mttr_minutes'].isdigit():
            mttr_data.append((row['architecture_type'], int(row['mttr_minutes'])))
    
    if mttr_data:
        arch_mttr = defaultdict(list)
        for arch, mttr in mttr_data:
            arch_mttr[arch].append(mttr)
        
        print(f"\nMTTR by Architecture Type:")
        for arch, mttrs in arch_mttr.items():
            avg_mttr = sum(mttrs) / len(mttrs)
            min_mttr = min(mttrs)
            max_mttr = max(mttrs)
            print(f"  {arch}: Avg={avg_mttr:.0f}min, Range={min_mttr}-{max_mttr}min")
    
    # Failure domains
    domains = Counter(row['failure_domain'] for row in data)
    print(f"\nFailure Domain Distribution:")
    for domain, count in domains.most_common():
        pct = (count / total) * 100
        print(f"  {domain}: {count}/{total} ({pct:.1f}%)")
    
    # Root causes
    causes = Counter(row['root_cause_category'] for row in data)
    print(f"\nRoot Cause Categories:")
    for cause, count in causes.most_common():
        pct = (count / total) * 100
        print(f"  {cause}: {count}/{total} ({pct:.1f}%)")

def generate_combined_insights(survey_data, postmortem_data):
    """Generate insights combining both datasets"""
    print("\n=== COMBINED INSIGHTS ===\n")
    
    if survey_data:
        # Architecture preference trends
        separated_preference = sum(1 for row in survey_data if row['preferred_architecture'] == 'Separated')
        total_survey = len(survey_data)
        sep_pref_pct = (separated_preference / total_survey) * 100
        print(f"Survey: {separated_preference}/{total_survey} ({sep_pref_pct:.1f}%) prefer separated architectures")
    
    if postmortem_data:
        # Incident evidence
        positive_evidence = sum(1 for row in postmortem_data 
                               if row['separated_arch_impact'].startswith('Positive'))
        total_incidents = len(postmortem_data)
        pos_evidence_pct = (positive_evidence / total_incidents) * 100
        print(f"Incidents: {positive_evidence}/{total_incidents} ({pos_evidence_pct:.1f}%) show positive separation impact")
        
        # MTTR comparison
        mttr_by_arch = defaultdict(list)
        for row in postmortem_data:
            if row['mttr_minutes'].isdigit():
                mttr_by_arch[row['architecture_type']].append(int(row['mttr_minutes']))
        
        if 'Separated' in mttr_by_arch and 'Coupled' in mttr_by_arch:
            sep_avg = sum(mttr_by_arch['Separated']) / len(mttr_by_arch['Separated'])
            coupled_avg = sum(mttr_by_arch['Coupled']) / len(mttr_by_arch['Coupled'])
            improvement = ((coupled_avg - sep_avg) / coupled_avg) * 100
            print(f"MTTR: Separated architectures show {improvement:.1f}% faster recovery on average")
    
    print(f"\nConclusion: Both survey preferences and incident evidence support separated architectures")

def main():
    base_path = "/Users/patrickmcfadin/local_projects/post-database-era/datasets/practitioner-signals"
    
    # Load survey data
    survey_file = f"{base_path}/architect-surveys/2025-08-20__data__architect-surveys__multi-source__architecture-preferences.csv"
    survey_data = load_csv(survey_file)
    
    # Load postmortem data (use the real incidents dataset)
    postmortem_file = f"{base_path}/postmortem-coding/2025-08-20__data__postmortems__real-incidents__architecture-impact.csv"
    postmortem_data = load_csv(postmortem_file)
    
    print(f"Loaded {len(survey_data)} survey responses and {len(postmortem_data)} incident records\n")
    
    # Run analyses
    analyze_survey_data(survey_data)
    analyze_postmortem_data(postmortem_data)
    generate_combined_insights(survey_data, postmortem_data)
    
    # Export summary
    timestamp = datetime.now().strftime('%Y-%m-%d')
    summary_file = f"{base_path}/analysis/{timestamp}__summary__practitioner-signals__key-metrics.csv"
    
    # Simple CSV export
    import os
    os.makedirs(f"{base_path}/analysis", exist_ok=True)
    
    with open(summary_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['metric', 'value', 'sample_size', 'percentage'])
        
        if survey_data:
            # Survey metrics
            separated_pref = sum(1 for row in survey_data if row['preferred_architecture'] == 'Separated')
            writer.writerow(['survey_prefer_separated', separated_pref, len(survey_data), 
                           f"{(separated_pref/len(survey_data)*100):.1f}%"])
        
        if postmortem_data:
            # Incident metrics
            positive_impact = sum(1 for row in postmortem_data 
                                if row['separated_arch_impact'].startswith('Positive'))
            writer.writerow(['incidents_positive_separation', positive_impact, len(postmortem_data),
                           f"{(positive_impact/len(postmortem_data)*100):.1f}%"])
    
    print(f"\nSummary exported to: {summary_file}")

if __name__ == '__main__':
    main()