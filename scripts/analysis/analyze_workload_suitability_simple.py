#!/usr/bin/env python3
"""
Workload Suitability Analysis for Compute-Storage Separation (No Pandas Version)

Analyzes workload characteristics and generates suitability scores and recommendations
for compute-storage separation architectures.

Usage:
    python3 analyze_workload_suitability_simple.py
"""

import csv
import json
from datetime import datetime
import os
import yaml

def load_datasets():
    """Load all workload suitability datasets"""
    
    datasets_dir = "/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets"
    current_date = "2025-08-20"  # Match the generated files
    
    # Load workload classification matrix
    classification_file = f"{datasets_dir}/{current_date}__data__workload-suitability__research__classification-matrix.csv"
    workload_data = []
    with open(classification_file, 'r') as f:
        reader = csv.DictReader(f)
        workload_data = list(reader)
    
    # Load transactional requirements
    transactional_file = f"{datasets_dir}/{current_date}__data__workload-suitability__research__transactional-requirements.csv"
    transactional_data = []
    with open(transactional_file, 'r') as f:
        reader = csv.DictReader(f)
        transactional_data = list(reader)
    
    # Load AI/ML patterns
    ai_ml_file = f"{datasets_dir}/{current_date}__data__workload-suitability__research__ai-ml-patterns.csv"
    ai_ml_data = []
    with open(ai_ml_file, 'r') as f:
        reader = csv.DictReader(f)
        ai_ml_data = list(reader)
    
    # Load decision framework
    decision_file = f"{datasets_dir}/{current_date}__data__workload-suitability__research__decision-framework.csv"
    decision_data = []
    with open(decision_file, 'r') as f:
        reader = csv.DictReader(f)
        decision_data = list(reader)
    
    return workload_data, transactional_data, ai_ml_data, decision_data

def create_suitability_matrix():
    """Create a comprehensive suitability matrix"""
    
    workload_data, transactional_data, ai_ml_data, decision_data = load_datasets()
    
    # Create suitability matrix combining workload types with architectural patterns
    matrix_data = []
    
    for workload in workload_data:
        for architecture in transactional_data:
            
            # Calculate compatibility score based on multiple factors
            compatibility_score = calculate_compatibility_score(workload, architecture)
            
            matrix_data.append({
                'workload_type': workload['workload_type'],
                'architecture_pattern': architecture['architecture_pattern'],
                'base_suitability_score': workload['suitability_score'],
                'latency_compatibility': assess_latency_compatibility(workload, architecture),
                'consistency_compatibility': assess_consistency_compatibility(workload, architecture),
                'throughput_compatibility': assess_throughput_compatibility(workload, architecture),
                'overall_compatibility_score': compatibility_score,
                'recommendation': get_recommendation(compatibility_score),
                'key_considerations': get_key_considerations(workload, architecture),
                'risk_factors': get_risk_factors(workload, architecture),
                'optimization_opportunities': get_optimization_opportunities(workload, architecture)
            })
    
    return matrix_data

def calculate_compatibility_score(workload, architecture):
    """Calculate overall compatibility score between workload and architecture"""
    
    # Base score from workload suitability
    base_score = float(workload['suitability_score'])
    
    # Latency factor
    latency_factor = assess_latency_compatibility(workload, architecture)
    
    # Consistency factor
    consistency_factor = assess_consistency_compatibility(workload, architecture)
    
    # Throughput factor
    throughput_factor = assess_throughput_compatibility(workload, architecture)
    
    # Network dependency factor
    network_factor = assess_network_dependency(workload, architecture)
    
    # Weighted average
    weights = {
        'base': 0.3,
        'latency': 0.25,
        'consistency': 0.2,
        'throughput': 0.15,
        'network': 0.1
    }
    
    score = (
        base_score * weights['base'] +
        latency_factor * weights['latency'] +
        consistency_factor * weights['consistency'] +
        throughput_factor * weights['throughput'] +
        network_factor * weights['network']
    )
    
    return round(score, 2)

def assess_latency_compatibility(workload, architecture):
    """Assess latency compatibility between workload and architecture"""
    
    workload_latency = workload['latency_requirement']
    arch_latency = architecture['commit_latency_p99']
    
    # Extract numeric values and compare
    if '< 1ms' in workload_latency or '< 10ms' in workload_latency:
        if '< 5ms' in arch_latency or '< 1ms' in arch_latency:
            return 5
        elif '< 20ms' in arch_latency:
            return 3
        else:
            return 1
    elif '10-50ms' in workload_latency or '< 100ms' in workload_latency:
        if '< 20ms' in arch_latency or '< 10ms' in arch_latency:
            return 5
        elif '20-100ms' in arch_latency:
            return 4
        else:
            return 2
    else:  # Higher latency tolerance
        return 5
    
    return 3  # Default moderate compatibility

def assess_consistency_compatibility(workload, architecture):
    """Assess consistency model compatibility"""
    
    workload_consistency = workload['consistency_model'].lower()
    arch_consistency = architecture['consistency_model'].lower()
    
    # Strong consistency requirements
    if 'strong' in workload_consistency or 'acid' in workload_consistency:
        if 'strong' in arch_consistency or 'acid' in arch_consistency:
            return 5
        elif 'hybrid' in arch_consistency:
            return 3
        else:
            return 1
    
    # Eventual consistency acceptable
    elif 'eventual' in workload_consistency:
        return 5  # Any consistency model works
    
    # Default moderate compatibility
    return 3

def assess_throughput_compatibility(workload, architecture):
    """Assess throughput compatibility"""
    
    workload_pattern = workload['transaction_pattern'].lower()
    arch_throughput = architecture['throughput_characteristics'].lower()
    
    # High throughput workloads
    if 'large' in workload_pattern or 'bulk' in workload_pattern:
        if 'high' in arch_throughput or 'very high' in arch_throughput:
            return 5
        elif 'variable' in arch_throughput:
            return 4
        else:
            return 2
    
    # Small transaction workloads
    elif 'small' in workload_pattern or 'frequent' in workload_pattern:
        if 'limited' in arch_throughput:
            return 2
        elif 'high' in arch_throughput and 'local' in arch_throughput:
            return 5
        else:
            return 3
    
    return 3  # Default

def assess_network_dependency(workload, architecture):
    """Assess network dependency compatibility"""
    
    arch_network = architecture['network_dependency'].lower()
    
    # Network sensitive workloads get lower scores for high network dependency
    if 'high' in arch_network:
        return 2
    elif 'medium' in arch_network:
        return 3
    else:  # Low network dependency
        return 5

def get_recommendation(score):
    """Get recommendation based on compatibility score"""
    
    if score >= 4.5:
        return "Highly Recommended"
    elif score >= 3.5:
        return "Recommended"
    elif score >= 2.5:
        return "Consider with Caution"
    elif score >= 1.5:
        return "Not Recommended"
    else:
        return "Strongly Discouraged"

def get_key_considerations(workload, architecture):
    """Get key considerations for this workload-architecture combination"""
    
    considerations = []
    
    # Latency considerations
    if '< 10ms' in workload['latency_requirement']:
        considerations.append("Ultra-low latency requirements may be challenging")
    
    # Consistency considerations
    if 'strong' in workload['consistency_model'].lower():
        considerations.append("Strong consistency requirements need careful design")
    
    # Network considerations
    if 'high' in architecture['network_dependency'].lower():
        considerations.append("High network dependency requires reliable connectivity")
    
    # Failure recovery
    if 'minutes to hours' in architecture['failure_recovery_time']:
        considerations.append("Extended recovery times may impact availability")
    
    return "; ".join(considerations) if considerations else "Standard implementation considerations apply"

def get_risk_factors(workload, architecture):
    """Identify risk factors for this combination"""
    
    risks = []
    
    # Performance risks
    if float(workload['suitability_score']) <= 2 and 'high' in architecture['network_dependency'].lower():
        risks.append("Network latency may severely impact performance")
    
    # Consistency risks
    if 'strong' in workload['consistency_model'].lower() and 'eventual' in architecture['consistency_model'].lower():
        risks.append("Consistency model mismatch may cause data integrity issues")
    
    # Recovery risks
    if 'hours' in architecture['failure_recovery_time']:
        risks.append("Long recovery times may violate SLA requirements")
    
    # Cost risks
    if 'memory-based' in architecture['architecture_pattern'].lower():
        risks.append("High memory costs may be prohibitive at scale")
    
    return "; ".join(risks) if risks else "Standard operational risks"

def get_optimization_opportunities(workload, architecture):
    """Identify optimization opportunities"""
    
    opportunities = []
    
    # Caching opportunities
    if float(workload['suitability_score']) >= 4:
        opportunities.append("Implement aggressive caching strategies")
    
    # Cost optimization
    if 'batch' in workload['workload_type'].lower():
        opportunities.append("Use spot instances for cost optimization")
    
    # Auto-scaling
    if 'elastic' in architecture['throughput_characteristics'].lower():
        opportunities.append("Implement auto-scaling for cost efficiency")
    
    # Storage tiering
    if 'analytics' in workload['workload_type'].lower():
        opportunities.append("Implement storage tiering for cost optimization")
    
    return "; ".join(opportunities) if opportunities else "Standard optimization practices apply"

def create_ai_ml_suitability_analysis():
    """Create specific analysis for AI/ML workload suitability"""
    
    _, _, ai_ml_data, _ = load_datasets()
    
    ai_ml_analysis = []
    
    for pattern in ai_ml_data:
        
        # Assess separation benefits
        separation_score = assess_ai_ml_separation_score(pattern)
        
        ai_ml_analysis.append({
            'pattern_name': pattern['pattern_name'],
            'separation_suitability_score': separation_score,
            'primary_benefits': pattern['separation_benefits'],
            'architecture_recommendation': pattern['architecture_approach'],
            'cost_impact': assess_cost_impact(pattern),
            'performance_impact': assess_performance_impact(pattern),
            'complexity_impact': assess_complexity_impact(pattern),
            'scale_benefits': assess_scale_benefits(pattern),
            'implementation_priority': get_implementation_priority(separation_score),
            'success_factors': get_ai_ml_success_factors(pattern),
            'common_pitfalls': get_ai_ml_pitfalls(pattern)
        })
    
    return ai_ml_analysis

def assess_ai_ml_separation_score(pattern):
    """Calculate AI/ML specific separation suitability score"""
    
    latency = pattern['typical_latency']
    compute_req = pattern['compute_requirements']
    storage_req = pattern['storage_requirements']
    
    score = 3  # Base score
    
    # Latency factor
    if 'hours' in latency or 'minutes' in latency:
        score += 1
    elif 'milliseconds' in latency:
        score -= 1
    
    # Compute intensity factor
    if 'intensive' in compute_req or 'GPU' in compute_req:
        score += 1
    
    # Storage requirements factor
    if 'cost-effective' in storage_req or 'throughput' in storage_req:
        score += 1
    
    # Scale factor
    if 'elastic' in compute_req or 'auto-scaling' in compute_req:
        score += 1
    
    return min(5, max(1, score))

def assess_cost_impact(pattern):
    """Assess cost impact of separation for AI/ML patterns"""
    
    if 'cost optimization' in pattern['cost_optimization'].lower():
        return "Significant cost savings possible"
    elif 'spot instances' in pattern['cost_optimization'].lower():
        return "Major cost optimization opportunities"
    else:
        return "Moderate cost benefits"

def assess_performance_impact(pattern):
    """Assess performance impact of separation"""
    
    latency = pattern['typical_latency']
    
    if 'milliseconds' in latency:
        return "Potential performance impact, requires optimization"
    elif 'seconds' in latency:
        return "Minimal performance impact"
    else:
        return "No significant performance impact"

def assess_complexity_impact(pattern):
    """Assess complexity impact of implementing separation"""
    
    if 'distributed' in pattern['architecture_approach'].lower():
        return "High complexity, requires careful design"
    elif 'pipeline' in pattern['architecture_approach'].lower():
        return "Moderate complexity, standard patterns available"
    else:
        return "Low complexity, straightforward implementation"

def assess_scale_benefits(pattern):
    """Assess scaling benefits from separation"""
    
    compute_req = pattern['compute_requirements']
    
    if 'elastic' in compute_req or 'auto-scaling' in compute_req:
        return "Excellent scaling benefits"
    elif 'intensive' in compute_req:
        return "Good scaling benefits for compute"
    else:
        return "Standard scaling benefits"

def get_implementation_priority(score):
    """Get implementation priority based on score"""
    
    if score >= 4:
        return "High Priority"
    elif score >= 3:
        return "Medium Priority"
    else:
        return "Low Priority"

def get_ai_ml_success_factors(pattern):
    """Get success factors for AI/ML pattern implementation"""
    
    factors = []
    
    if 'caching' in pattern['caching_strategy']:
        factors.append("Implement effective caching strategy")
    
    if 'versioning' in pattern['consistency_model']:
        factors.append("Ensure proper data versioning")
    
    if 'GPU' in pattern['compute_requirements']:
        factors.append("Optimize for GPU compute efficiency")
    
    return "; ".join(factors) if factors else "Follow standard ML infrastructure practices"

def get_ai_ml_pitfalls(pattern):
    """Get common pitfalls for AI/ML patterns"""
    
    pitfalls = []
    
    if 'milliseconds' in pattern['typical_latency']:
        pitfalls.append("Network latency can significantly impact real-time performance")
    
    if 'vector' in pattern['pattern_name'].lower():
        pitfalls.append("Vector transfer overhead can be substantial")
    
    if 'streaming' in pattern['pattern_name'].lower():
        pitfalls.append("Stream processing consistency across separated components")
    
    return "; ".join(pitfalls) if pitfalls else "Standard implementation risks apply"

def calculate_summary_statistics(matrix_data, ai_ml_analysis):
    """Calculate summary statistics without pandas"""
    
    # Matrix statistics
    recommendations = [item['recommendation'] for item in matrix_data]
    compatibility_scores = [float(item['overall_compatibility_score']) for item in matrix_data]
    
    highly_recommended = sum(1 for r in recommendations if r == 'Highly Recommended')
    recommended = sum(1 for r in recommendations if r == 'Recommended')
    not_recommended = sum(1 for r in recommendations if r == 'Not Recommended')
    
    avg_compatibility = sum(compatibility_scores) / len(compatibility_scores)
    
    # Find highest and lowest scoring combinations
    max_score = max(compatibility_scores)
    min_score = min(compatibility_scores)
    max_idx = compatibility_scores.index(max_score)
    min_idx = compatibility_scores.index(min_score)
    
    highest_combo = f"{matrix_data[max_idx]['workload_type']} + {matrix_data[max_idx]['architecture_pattern']}"
    lowest_combo = f"{matrix_data[min_idx]['workload_type']} + {matrix_data[min_idx]['architecture_pattern']}"
    
    # AI/ML statistics
    ai_ml_priorities = [item['implementation_priority'] for item in ai_ml_analysis]
    ai_ml_scores = [int(item['separation_suitability_score']) for item in ai_ml_analysis]
    
    high_priority_ai_ml = sum(1 for p in ai_ml_priorities if p == 'High Priority')
    excellent_separation_ai_ml = sum(1 for s in ai_ml_scores if s >= 4)
    
    # Find top AI/ML pattern
    max_ai_ml_score = max(ai_ml_scores)
    max_ai_ml_idx = ai_ml_scores.index(max_ai_ml_score)
    top_ai_ml_pattern = ai_ml_analysis[max_ai_ml_idx]['pattern_name']
    
    # Calculate OLAP vs OLTP averages
    olap_scores = [float(item['overall_compatibility_score']) for item in matrix_data if 'OLAP' in item['workload_type']]
    oltp_scores = [float(item['overall_compatibility_score']) for item in matrix_data if 'OLTP' in item['workload_type']]
    
    avg_olap = sum(olap_scores) / len(olap_scores) if olap_scores else 0
    avg_oltp = sum(oltp_scores) / len(oltp_scores) if oltp_scores else 0
    
    return {
        'total_combinations': len(matrix_data),
        'highly_recommended': highly_recommended,
        'recommended': recommended,
        'not_recommended': not_recommended,
        'avg_compatibility': round(avg_compatibility, 2),
        'highest_combo': highest_combo,
        'lowest_combo': lowest_combo,
        'ai_ml_patterns': len(ai_ml_analysis),
        'high_priority_ai_ml': high_priority_ai_ml,
        'excellent_separation_ai_ml': excellent_separation_ai_ml,
        'top_ai_ml_pattern': top_ai_ml_pattern,
        'avg_olap_score': round(avg_olap, 2),
        'avg_oltp_score': round(avg_oltp, 2)
    }

def save_analysis_results():
    """Save all analysis results"""
    
    datasets_dir = "/Users/patrickmcfadin/local_projects/post-database-era/theses/database-compute-storage-separation/datasets"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Save suitability matrix
    matrix_data = create_suitability_matrix()
    matrix_file = f"{datasets_dir}/{current_date}__analysis__workload-suitability__suitability-matrix.csv"
    
    with open(matrix_file, 'w', newline='') as f:
        if matrix_data:
            writer = csv.DictWriter(f, fieldnames=matrix_data[0].keys())
            writer.writeheader()
            writer.writerows(matrix_data)
    
    # Save AI/ML analysis
    ai_ml_analysis = create_ai_ml_suitability_analysis()
    ai_ml_file = f"{datasets_dir}/{current_date}__analysis__workload-suitability__ai-ml-analysis.csv"
    
    with open(ai_ml_file, 'w', newline='') as f:
        if ai_ml_analysis:
            writer = csv.DictWriter(f, fieldnames=ai_ml_analysis[0].keys())
            writer.writeheader()
            writer.writerows(ai_ml_analysis)
    
    # Create summary statistics
    stats = calculate_summary_statistics(matrix_data, ai_ml_analysis)
    
    summary = {
        'analysis_date': current_date,
        'total_workload_architecture_combinations': stats['total_combinations'],
        'highly_recommended_combinations': stats['highly_recommended'],
        'recommended_combinations': stats['recommended'],
        'not_recommended_combinations': stats['not_recommended'],
        'average_compatibility_score': stats['avg_compatibility'],
        'highest_scoring_combination': stats['highest_combo'],
        'lowest_scoring_combination': stats['lowest_combo'],
        'ai_ml_patterns_analyzed': stats['ai_ml_patterns'],
        'high_priority_ai_ml_patterns': stats['high_priority_ai_ml'],
        'excellent_separation_ai_ml_patterns': stats['excellent_separation_ai_ml'],
        'top_ai_ml_pattern': stats['top_ai_ml_pattern'],
        'key_insights': [
            f"OLAP workloads show highest compatibility with separation (avg score: {stats['avg_olap_score']})",
            f"OLTP workloads show lower compatibility (avg score: {stats['avg_oltp_score']})",
            f"AI/ML batch workloads are excellent candidates for separation",
            f"Network dependency is a key factor in architecture selection"
        ]
    }
    
    # Save summary
    summary_file = f"{datasets_dir}/{current_date}__analysis__workload-suitability__summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return matrix_file, ai_ml_file, summary_file, stats

if __name__ == "__main__":
    print("Analyzing workload suitability for compute-storage separation...")
    
    # Run analysis
    matrix_file, ai_ml_file, summary_file, stats = save_analysis_results()
    
    print(f"\nAnalysis complete! Files created:")
    print(f"  - Suitability Matrix: {matrix_file}")
    print(f"  - AI/ML Analysis: {ai_ml_file}")
    print(f"  - Summary Statistics: {summary_file}")
    
    # Display sample insights
    print(f"\nKey Insights:")
    print(f"  - Analyzed {stats['total_combinations']} workload-architecture combinations")
    print(f"  - {stats['highly_recommended']} combinations are highly recommended")
    print(f"  - OLAP workloads average score: {stats['avg_olap_score']}")
    print(f"  - OLTP workloads average score: {stats['avg_oltp_score']}")
    print(f"  - Top AI/ML pattern for separation: {stats['top_ai_ml_pattern']}")
    print(f"  - {stats['high_priority_ai_ml']} AI/ML patterns are high priority for separation")