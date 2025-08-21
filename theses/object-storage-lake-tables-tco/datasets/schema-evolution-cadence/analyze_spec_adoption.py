#!/usr/bin/env python3
"""
Analyze collected specification adoption data to identify trends and patterns.
"""

import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def load_datasets():
    """Load all collected datasets."""
    datasets = {}
    
    try:
        datasets['releases'] = pd.read_csv('2025-08-21__data__spec-adoption__multi-format__version-releases.csv')
        datasets['production'] = pd.read_csv('2025-08-21__data__spec-adoption__production__usage-patterns.csv')
        datasets['migrations'] = pd.read_csv('2025-08-21__data__spec-adoption__migration__timeline-patterns.csv')
        datasets['feature_flags'] = pd.read_csv('2025-08-21__data__spec-adoption__feature-flags__adoption-patterns.csv')
        
        print("Successfully loaded all datasets:")
        for name, df in datasets.items():
            print(f"  {name}: {len(df)} records")
            
    except Exception as e:
        print(f"Error loading datasets: {e}")
    
    return datasets

def analyze_version_adoption_patterns(datasets):
    """Analyze version adoption patterns across formats."""
    analysis = {}
    
    # Release velocity analysis
    releases_df = datasets['releases']
    releases_df['release_date'] = pd.to_datetime(releases_df['release_date'])
    releases_df['year'] = releases_df['release_date'].dt.year
    
    # Releases per year by format
    releases_by_year = releases_df.groupby(['year', 'format']).size().reset_index(name='release_count')
    analysis['release_velocity'] = releases_by_year.to_dict('records')
    
    # Feature adoption patterns
    feature_flags_df = datasets['feature_flags']
    
    # Average adoption rate by format
    avg_adoption = feature_flags_df.groupby('format')['adoption_rate'].agg(['mean', 'std']).reset_index()
    analysis['average_adoption_rates'] = avg_adoption.to_dict('records')
    
    # Most adopted features by format
    top_features = feature_flags_df.nlargest(10, 'adoption_rate')[['format', 'features', 'adoption_rate', 'stability_level']]
    analysis['top_adopted_features'] = top_features.to_dict('records')
    
    # Migration timeline patterns
    migrations_df = datasets['migrations']
    
    # Average migration duration by strategy
    migration_duration = migrations_df.groupby('migration_strategy')['phase_duration_weeks'].sum().reset_index()
    analysis['migration_durations'] = migration_duration.to_dict('records')
    
    # Migration strategy by organization type
    strategy_org = migrations_df.groupby(['organization_type', 'migration_strategy']).size().reset_index(name='count')
    analysis['strategy_by_org_type'] = strategy_org.to_dict('records')
    
    return analysis

def analyze_production_adoption(datasets):
    """Analyze production adoption patterns."""
    production_df = datasets['production']
    
    analysis = {}
    
    # Adoption by organization type
    org_adoption = production_df.groupby(['format', 'org_type']).size().reset_index(name='count')
    analysis['adoption_by_org_type'] = org_adoption.to_dict('records')
    
    # Source type distribution
    source_dist = production_df['source_type'].value_counts().to_dict()
    analysis['source_distribution'] = source_dist
    
    # GitHub repository analysis
    github_data = production_df[production_df['source_type'] == 'github-repository']
    if not github_data.empty:
        # Extract stars from metadata
        github_data = github_data.copy()
        github_data['stars'] = github_data['metadata'].str.extract(r'stars:(\d+)').astype(int)
        
        # Top repositories by stars
        top_repos = github_data.nlargest(5, 'stars')[['format', 'metadata', 'stars']]
        analysis['top_github_repos'] = top_repos.to_dict('records')
        
        # Average stars by format
        avg_stars = github_data.groupby('format')['stars'].mean().reset_index()
        analysis['average_stars_by_format'] = avg_stars.to_dict('records')
    
    return analysis

def identify_migration_blockers(datasets):
    """Identify common migration blockers and success patterns."""
    migrations_df = datasets['migrations']
    
    analysis = {}
    
    # Most common blockers
    all_blockers = []
    for blockers_str in migrations_df['blockers_encountered'].dropna():
        if blockers_str and blockers_str != '':
            all_blockers.extend([b.strip() for b in blockers_str.split(';')])
    
    blocker_counts = pd.Series(all_blockers).value_counts().head(10)
    analysis['common_blockers'] = blocker_counts.to_dict()
    
    # Success criteria patterns
    all_criteria = []
    for criteria_str in migrations_df['success_criteria'].dropna():
        if criteria_str and criteria_str != '':
            all_criteria.extend([c.strip() for c in criteria_str.split(';')])
    
    criteria_counts = pd.Series(all_criteria).value_counts().head(10)
    analysis['success_criteria'] = criteria_counts.to_dict()
    
    # Migration duration by format
    duration_by_format = migrations_df.groupby('format')['phase_duration_weeks'].sum().reset_index()
    analysis['total_duration_by_format'] = duration_by_format.to_dict('records')
    
    return analysis

def generate_recommendations(analysis_results):
    """Generate recommendations based on analysis."""
    recommendations = []
    
    # Release velocity recommendations
    release_velocity = analysis_results['version_patterns']['release_velocity']
    velocity_df = pd.DataFrame(release_velocity)
    
    if not velocity_df.empty:
        avg_velocity = velocity_df.groupby('format')['release_count'].mean()
        fastest_format = avg_velocity.idxmax()
        slowest_format = avg_velocity.idxmin()
        
        recommendations.append({
            'category': 'release_velocity',
            'insight': f'{fastest_format} has the highest release velocity, while {slowest_format} has the lowest',
            'recommendation': f'Organizations requiring rapid feature access should consider {fastest_format}'
        })
    
    # Feature adoption recommendations
    top_features = analysis_results['version_patterns']['top_adopted_features']
    if top_features:
        most_adopted = top_features[0]
        recommendations.append({
            'category': 'feature_adoption',
            'insight': f"Most adopted feature: {most_adopted['features']} in {most_adopted['format']} ({most_adopted['adoption_rate']*100:.1f}%)",
            'recommendation': 'Focus on stable, high-adoption features for production deployments'
        })
    
    # Migration strategy recommendations
    migration_patterns = analysis_results['migration_analysis']
    strategy_org = migration_patterns['strategy_by_org_type']
    
    if strategy_org:
        strategy_df = pd.DataFrame(strategy_org)
        enterprise_strategies = strategy_df[strategy_df['organization_type'] == 'enterprise']
        if not enterprise_strategies.empty:
            preferred_strategy = enterprise_strategies.loc[enterprise_strategies['count'].idxmax(), 'migration_strategy']
            recommendations.append({
                'category': 'migration_strategy',
                'insight': f'Enterprises prefer {preferred_strategy} migration strategy',
                'recommendation': f'Large organizations should consider {preferred_strategy} for lower risk'
            })
    
    # Common blocker recommendations
    common_blockers = migration_patterns['common_blockers']
    if common_blockers:
        top_blocker = list(common_blockers.keys())[0]
        recommendations.append({
            'category': 'migration_planning',
            'insight': f'Most common migration blocker: {top_blocker}',
            'recommendation': f'Plan extra time and resources for {top_blocker} during migrations'
        })
    
    return recommendations

def main():
    """Main analysis function."""
    print("Loading and analyzing specification adoption data...")
    
    # Load datasets
    datasets = load_datasets()
    
    if not datasets:
        print("No datasets loaded. Exiting.")
        return
    
    # Perform analyses
    print("\nAnalyzing version adoption patterns...")
    version_patterns = analyze_version_adoption_patterns(datasets)
    
    print("Analyzing production adoption...")
    production_analysis = analyze_production_adoption(datasets)
    
    print("Analyzing migration patterns...")
    migration_analysis = identify_migration_blockers(datasets)
    
    # Combine results
    analysis_results = {
        'version_patterns': version_patterns,
        'production_analysis': production_analysis,
        'migration_analysis': migration_analysis,
        'generated_at': datetime.now().isoformat()
    }
    
    # Generate recommendations
    print("Generating recommendations...")
    recommendations = generate_recommendations(analysis_results)
    analysis_results['recommendations'] = recommendations
    
    # Save results
    output_file = '2025-08-21__analysis__spec-adoption__comprehensive-analysis.json'
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    print(f"\nAnalysis complete. Results saved to {output_file}")
    
    # Print summary
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Total releases analyzed: {len(datasets['releases'])}")
    print(f"Production usage patterns: {len(datasets['production'])}")
    print(f"Migration phases tracked: {len(datasets['migrations'])}")
    print(f"Feature flags analyzed: {len(datasets['feature_flags'])}")
    
    print("\n=== KEY INSIGHTS ===")
    for rec in recommendations:
        print(f"• {rec['category'].title()}: {rec['insight']}")
    
    print("\n=== RECOMMENDATIONS ===")
    for rec in recommendations:
        print(f"• {rec['recommendation']}")

if __name__ == "__main__":
    main()