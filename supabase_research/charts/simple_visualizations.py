#!/usr/bin/env python3
"""
Simple Data Visualization Script for Supabase Research
Creates charts without pandas to avoid NumPy compatibility issues
"""

import matplotlib.pyplot as plt
import numpy as np
import csv
from pathlib import Path

# Set style for professional-looking charts
plt.style.use('default')

# Define paths
data_dir = Path("../")
charts_dir = Path("./")

def read_csv_simple(filename):
    """Read CSV file without pandas"""
    data = []
    try:
        with open(data_dir / filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        print(f"✅ Loaded {filename}: {len(data)} rows")
        return data
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return []
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return []

def create_github_comparison():
    """Create GitHub metrics comparison"""
    data = read_csv_simple('2025-08-21__data__github-metrics__comparison__repository-stats.csv')
    if not data:
        return
    
    # Extract GitHub data
    companies = []
    stars = []
    forks = []
    
    company_totals = {}
    for row in data:
        company = row['company']
        if company not in company_totals:
            company_totals[company] = {'stars': 0, 'forks': 0}
        
        try:
            company_totals[company]['stars'] += int(row['stars'])
            company_totals[company]['forks'] += int(row['forks'])
        except ValueError:
            continue
    
    companies = list(company_totals.keys())
    stars = [company_totals[c]['stars'] for c in companies]
    forks = [company_totals[c]['forks'] for c in companies]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('GitHub Community Engagement: Supabase vs SingleStore', fontsize=16, fontweight='bold')
    
    # Stars comparison
    colors = ['#3ECF8E', '#AA6C39']
    bars1 = ax1.bar(companies, stars, color=colors)
    ax1.set_title('GitHub Stars', fontweight='bold')
    ax1.set_ylabel('Stars')
    
    for bar, value in zip(bars1, stars):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(stars)*0.02,
                f'{value:,}', ha='center', fontweight='bold')
    
    # Forks comparison
    bars2 = ax2.bar(companies, forks, color=colors)
    ax2.set_title('GitHub Forks', fontweight='bold')
    ax2.set_ylabel('Forks')
    
    for bar, value in zip(bars2, forks):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(forks)*0.02,
                f'{value:,}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'github_metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: github_metrics_comparison.png")

def create_market_growth():
    """Create market growth projections"""
    data = read_csv_simple('2025-08-21__data__market-analysis__predictions__growth-forecasts.csv')
    if not data:
        return
    
    # Extract market data
    segments = []
    values_2024 = []
    values_2028 = []
    cagrs = []
    
    relevant_segments = ['Backend-as-a-Service (BaaS)', 'Database-as-a-Service (DBaaS)', 
                        'Vector Database', 'HTAP (Hybrid Transactional/Analytical Processing)']
    
    for row in data:
        if row['market_segment'] in relevant_segments:
            segments.append(row['market_segment'])
            try:
                values_2024.append(float(row['value_2024']))
                values_2028.append(float(row['value_2028_projected']))
                cagrs.append(float(row['cagr_percent']))
            except ValueError:
                continue
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Database Market Growth Projections (2024-2028)', fontsize=16, fontweight='bold')
    
    # Market size evolution
    x = np.arange(len(segments))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, values_2024, width, label='2024', alpha=0.8, color='#4ECDC4')
    bars2 = ax1.bar(x + width/2, values_2028, width, label='2028', alpha=0.8, color='#FF6B6B')
    
    ax1.set_title('Market Size Evolution (USD Billions)', fontweight='bold')
    ax1.set_ylabel('Market Size (USD Billions)')
    ax1.set_xticks(x)
    ax1.set_xticklabels([s.replace(' (', '\n(') for s in segments], rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # CAGR comparison
    colors = plt.cm.viridis(np.linspace(0, 1, len(cagrs)))
    bars3 = ax2.bar(range(len(segments)), cagrs, color=colors)
    ax2.set_title('Compound Annual Growth Rate (CAGR)', fontweight='bold')
    ax2.set_ylabel('CAGR (%)')
    ax2.set_xticks(range(len(segments)))
    ax2.set_xticklabels([s.replace(' (', '\n(') for s in segments], rotation=45, ha='right')
    
    for bar, value in zip(bars3, cagrs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'market_growth_projections.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: market_growth_projections.png")

def create_funding_comparison():
    """Create funding and valuation comparison"""
    data = read_csv_simple('2025-08-21__data__funding-market__comparison__investment-valuation.csv')
    if not data:
        return
    
    # Extract funding data
    valuations = {'Supabase': 2.0, 'SingleStore': 0.94}  # Billions from the data
    
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle('Company Valuations Comparison', fontsize=16, fontweight='bold')
    
    companies = list(valuations.keys())
    values = list(valuations.values())
    colors = ['#3ECF8E', '#AA6C39']
    
    bars = ax.bar(companies, values, color=colors, alpha=0.8)
    ax.set_ylabel('Valuation (USD Billions)')
    ax.set_title('Latest Company Valuations', fontweight='bold')
    
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'${value}B', ha='center', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'funding_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: funding_comparison.png")

def create_adoption_patterns():
    """Create adoption patterns visualization"""
    data = read_csv_simple('2025-08-21__data__adoption-patterns__comparison__use-cases-industries.csv')
    if not data:
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Adoption Patterns: Supabase vs SingleStore', fontsize=16, fontweight='bold')
    
    # Company size analysis
    supabase_sizes = []
    singlestore_sizes = []
    
    for row in data:
        if row['company'] == 'Supabase':
            supabase_sizes.append(row['typical_company_size'])
        elif row['company'] == 'SingleStore':
            singlestore_sizes.append(row['typical_company_size'])
    
    # Time to value comparison
    time_mapping = {
        '1-7 days': 4, '1-10 days': 5.5, '1-14 days': 7.5, '7-30 days': 18.5,
        '14-60 days': 37, '30-90 days': 60, '30-120 days': 75, '60-180 days': 120
    }
    
    supabase_times = []
    singlestore_times = []
    
    for row in data:
        time_val = time_mapping.get(row['time_to_value'], 0)
        if row['company'] == 'Supabase':
            supabase_times.append(time_val)
        elif row['company'] == 'SingleStore':
            singlestore_times.append(time_val)
    
    # Plot time to value
    if supabase_times:
        avg_supabase = sum(supabase_times) / len(supabase_times)
    else:
        avg_supabase = 0
        
    if singlestore_times:
        avg_singlestore = sum(singlestore_times) / len(singlestore_times)
    else:
        avg_singlestore = 0
    
    companies = ['Supabase', 'SingleStore']
    avg_times = [avg_supabase, avg_singlestore]
    colors = ['#3ECF8E', '#AA6C39']
    
    bars = ax1.bar(companies, avg_times, color=colors, alpha=0.8)
    ax1.set_ylabel('Average Time to Value (Days)')
    ax1.set_title('Time to Value Comparison', fontweight='bold')
    ax1.set_yscale('log')
    
    for bar, value in zip(bars, avg_times):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.1,
                f'{value:.0f} days', ha='center', fontweight='bold')
    
    # Implementation complexity distribution
    complexity_counts = {}
    for row in data:
        complexity = row['implementation_complexity']
        if complexity not in complexity_counts:
            complexity_counts[complexity] = 0
        complexity_counts[complexity] += 1
    
    ax2.pie(complexity_counts.values(), labels=complexity_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax2.set_title('Implementation Complexity Distribution', fontweight='bold')
    
    # Use cases
    use_cases = {}
    for row in data:
        use_case = row['use_case']
        if use_case not in use_cases:
            use_cases[use_case] = 0
        use_cases[use_case] += 1
    
    ax3.pie(use_cases.values(), labels=use_cases.keys(), autopct='%1.1f%%', startangle=90)
    ax3.set_title('Use Case Distribution', fontweight='bold')
    
    # Industries
    industries = {}
    for row in data:
        industry = row['industry_vertical']
        if industry not in industries:
            industries[industry] = 0
        industries[industry] += 1
    
    industry_names = list(industries.keys())
    industry_counts = list(industries.values())
    
    ax4.barh(range(len(industry_names)), industry_counts)
    ax4.set_yticks(range(len(industry_names)))
    ax4.set_yticklabels(industry_names)
    ax4.set_xlabel('Count')
    ax4.set_title('Industry Vertical Distribution', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(charts_dir / 'adoption_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: adoption_patterns.png")

def create_summary_infographic():
    """Create a comprehensive summary infographic"""
    fig = plt.figure(figsize=(20, 16))
    
    # Main title
    fig.suptitle('Supabase vs SingleStore: Research Summary\n"Post-Database Era" Analysis', 
                fontsize=24, fontweight='bold', y=0.95)
    
    # Create grid layout
    gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.3)
    
    # Key metrics comparison
    ax1 = fig.add_subplot(gs[0, :2])
    metrics = ['GitHub Stars', 'Valuation ($B)', 'Avg Time to Value (Days)']
    supabase_vals = [87463, 2.0, 7]
    singlestore_vals = [2, 0.94, 75]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    ax1.bar(x - width/2, supabase_vals, width, label='Supabase', color='#3ECF8E', alpha=0.8)
    ax1.bar(x + width/2, singlestore_vals, width, label='SingleStore', color='#AA6C39', alpha=0.8)
    ax1.set_title('Key Metrics Comparison', fontweight='bold', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics)
    ax1.legend()
    ax1.set_yscale('log')
    
    # Market growth projections
    ax2 = fig.add_subplot(gs[0, 2:])
    market_types = ['BaaS', 'DBaaS', 'Vector DB']
    cagr_values = [18.5, 24.2, 52.8]
    colors = ['#3ECF8E', '#AA6C39', '#4ECDC4']
    
    bars = ax2.bar(market_types, cagr_values, color=colors, alpha=0.8)
    ax2.set_title('Market Growth Rates (CAGR %)', fontweight='bold', fontsize=14)
    ax2.set_ylabel('CAGR (%)')
    
    for bar, value in zip(bars, cagr_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value}%', ha='center', fontweight='bold')
    
    # Target market comparison
    ax3 = fig.add_subplot(gs[1, :])
    ax3.axis('off')
    
    # Create comparison table
    table_data = [
        ['Aspect', 'Supabase', 'SingleStore'],
        ['Primary Market', 'Developers & Startups', 'Enterprise Analytics'],
        ['Database Type', 'PostgreSQL BaaS', 'Distributed SQL HTAP'],
        ['Target Company Size', '1-200 employees', '200+ employees'],
        ['Time to Value', '1-14 days', '30-180 days'],
        ['Implementation', 'Low complexity', 'High complexity'],
        ['Key Strength', 'Developer Experience', 'Real-time Analytics']
    ]
    
    table = ax3.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.375, 0.375])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(3):
        table[(0, i)].set_facecolor('#E8E8E8')
        table[(0, i)].set_text_props(weight='bold')
    
    # Style company columns
    for i in range(1, len(table_data)):
        table[(i, 1)].set_facecolor('#E8F5E8')  # Light green for Supabase
        table[(i, 2)].set_facecolor('#F5E8E8')  # Light red for SingleStore
    
    ax3.set_title('Market Positioning Comparison', fontweight='bold', fontsize=16, pad=20)
    
    # Key insights
    ax4 = fig.add_subplot(gs[2:, :])
    ax4.axis('off')
    
    insights_text = """
🎯 RESEARCH CONCLUSIONS

THESIS VALIDATION: 72% confidence that BaaS model will capture 40-50% of new application development by 2030

📊 KEY FINDINGS:
   • Supabase dominates developer mindshare (87K+ GitHub stars vs <10 for SingleStore)
   • Different market segments: BaaS targets developers/startups, HTAP targets enterprise analytics  
   • Vector database capabilities crucial for both (52.8% CAGR market growth)

⏱️ ADOPTION PATTERNS:
   • Supabase: Days to MVP, low complexity, developer-focused
   • SingleStore: Months to enterprise-scale, high complexity, analytics-focused

💰 MARKET DYNAMICS:
   • Supabase: $2B valuation (2022) - Community-driven growth
   • SingleStore: $940M valuation (2021) - Enterprise-focused positioning
   • BaaS market: 18.5% CAGR vs HTAP market: 26.4% CAGR

🔮 2030 PREDICTIONS:
   • BaaS platforms will dominate new application development (45% market share)
   • HTAP systems will own enterprise real-time analytics (35% market share)  
   • Parallel evolution more likely than universal platform dominance

💡 STRATEGIC INSIGHTS:
   The "Post-Database Era" represents specialized integration optimized for distinct use cases,
   not universal platform consolidation. Organizations should prepare for multi-platform
   architectures with clear integration strategies.
   
   Different approaches serve different needs:
   - Supabase model: Optimized for developer productivity and rapid application development
   - SingleStore model: Optimized for enterprise analytics and real-time data processing
   - Both models are complementary rather than directly competitive
    """
    
    ax4.text(0.05, 0.95, insights_text, transform=ax4.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8F8F8', alpha=0.9))
    
    plt.savefig(charts_dir / 'comprehensive_research_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Created: comprehensive_research_summary.png")

def main():
    """Main execution function"""
    print("🚀 Starting Simple Supabase Research Visualization")
    print("=" * 50)
    
    # Create individual charts
    create_github_comparison()
    create_market_growth()
    create_funding_comparison()
    create_adoption_patterns()
    
    # Create comprehensive summary
    create_summary_infographic()
    
    print("\n✅ All visualizations completed!")
    print(f"📁 Charts saved in: {charts_dir.absolute()}")
    print("\nGenerated files:")
    print("• github_metrics_comparison.png")
    print("• market_growth_projections.png") 
    print("• funding_comparison.png")
    print("• adoption_patterns.png")
    print("• comprehensive_research_summary.png")

if __name__ == "__main__":
    main()