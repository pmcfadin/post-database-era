# Practitioner Signals - Section 9 Research Data

This directory contains structured datasets supporting Section 9 research on practitioner signals and qualitative-to-quantitative data conversion for database architecture adoption patterns.

## Overview

The research focuses on two primary methodologies:
1. **Architect Survey Panel (9.1)** - Industry survey data on database architecture preferences
2. **Postmortem Coding Study (9.2)** - Systematic analysis of incident postmortems to assess separation impact

## Dataset Structure

### Architect Surveys (`architect-surveys/`)

#### Core Dataset
- `2025-08-20__data__architect-surveys__multi-source__architecture-preferences.csv` (5 responses)
  - Initial survey synthesis from Stack Overflow, CNCF, and Gartner research
  - Basic qualitative-to-quantitative conversion methodology

#### Expanded Dataset  
- `2025-08-20__data__industry-surveys__multi-source__expanded-preferences.csv` (11 responses)
  - Comprehensive synthesis across 6 major industry surveys
  - Enhanced quantitative scaling and validation

**Key Metrics:**
- 72.7% prefer separated architectures (vs 27.3% currently using)
- Net migration intention: +5 toward separated, -3 from coupled
- Primary drivers: Reliability (18%), Scalability (18%), Performance (18%)
- Main blockers: Operational complexity, learning curve, latency concerns

### Postmortem Coding (`postmortem-coding/`)

#### Template Dataset
- `2025-08-20__data__postmortems__multi-source__incident-coding.csv` (3 incidents)
  - Initial coding framework and methodology

#### Real Incidents Dataset
- `2025-08-20__data__postmortems__real-incidents__architecture-impact.csv` (10 incidents)
  - Analysis of actual public postmortems from AWS, GitHub, GCP, Azure, MongoDB, etc.
  - Systematic coding of separation impact on incident resolution

**Key Findings:**
- 80% of incidents show positive separation impact
- 53.3% faster average recovery (105min vs 225min MTTR)
- Storage failures most benefit from compute/storage separation
- Only 1 incident showed negative impact (S3 2017 cascade failure)

## Methodology

### Qualitative-to-Quantitative Conversion

#### Adoption Readiness Scale (1-5)
- **5**: No significant blockers
- **4**: Technical concerns (latency, performance)  
- **3**: Operational concerns (complexity, integration)
- **2**: Resource concerns (skills, tooling)
- **1**: Fundamental barriers (budget, mandate)

#### Architecture Complexity Preference (1-5)
- **5**: Very Complex (Multi-model, Federated)
- **4**: Complex (Separated, Microservices)
- **3**: Moderate (Hybrid, Tiered)
- **2**: Simple (Coupled, Monolithic)
- **1**: Very Simple (Single-instance)

#### Incident Impact Assessment
- **Positive**: Separation helped or would have reduced impact/MTTR
- **Neutral**: Separation would not significantly change outcome
- **Negative**: Separation increased complexity or hindered recovery

### Evidence Extraction Guidelines
- Key evidence phrases limited to ≤15 words
- Focus on technical details supporting impact assessment
- Conservative coding approach (when in doubt, mark as Neutral)

## Analysis Scripts

### Data Collection
- `scripts/collect_architect_surveys.py` - Survey data synthesis
- `scripts/collect_real_postmortems.py` - Real incident collection
- `scripts/collect_industry_surveys.py` - Expanded industry survey data

### Analysis  
- `scripts/simple_practitioner_analysis.py` - Basic analysis without dependencies
- `scripts/analyze_practitioner_signals.py` - Comprehensive analysis (requires pandas)

### Usage
```bash
# Collect fresh data
python3 scripts/collect_industry_surveys.py
python3 scripts/collect_real_postmortems.py

# Run analysis
python3 scripts/simple_practitioner_analysis.py
```

## Quality Assessment

### Survey Data
- **Sample Size**: 11 responses across 6 major industry surveys
- **Representativeness**: Covers major developer/architect communities
- **Limitations**: Synthesized from public sources, not direct survey
- **Bias Considerations**: Early adopter bias, conference attendee skew

### Incident Data  
- **Sample Size**: 10 major incidents from 8 different providers
- **Sources**: Official provider status pages and postmortems
- **Credibility**: Tier A - Official incident communications
- **Limitations**: Public incidents only, potential minimization bias

### Inter-rater Reliability
- **Status**: Single coder (initial study)
- **Target**: κ > 0.75 for production study
- **Validation**: Cross-reference with technical incident details

## Key Research Findings

### Convergent Evidence
Both survey preferences and incident evidence support separated architectures:

1. **Practitioner Preference**: 72.7% prefer separated architectures
2. **Incident Evidence**: 80% of incidents show positive separation impact  
3. **Performance**: 53% faster average recovery with separated architectures
4. **Migration Intent**: Net +5 shift toward separated architectures

### Adoption Patterns
- **Drivers**: Reliability, scalability, performance optimization
- **Blockers**: Operational complexity, latency concerns, team skills
- **Timeline**: 6-24 month adoption timelines typical
- **SLA Targets**: 25-200ms range, with separated architectures targeting mid-range

### Incident Patterns
- **Storage Failures**: Most benefit from separation (isolation effect)
- **Compute Failures**: Separation already provides isolation
- **Network Failures**: Generally architecture-agnostic
- **Cascade Failures**: Rare but can be exacerbated by dependencies

## Future Research Directions

### Expand Sample Sizes
- Target 200+ survey responses for statistical significance
- Collect 100+ incident postmortems across more providers
- Include regional and industry vertical analysis

### Methodological Improvements
- Implement dual coding for inter-rater reliability
- Validate quantitative scales with practitioner review
- Add longitudinal tracking of architecture migrations

### Additional Data Sources
- Private incident data from enterprise practitioners
- Migration case studies with before/after metrics
- Cost-benefit analysis of separation adoption

## Citation

When using this data, please cite:
```
Database Compute Storage Separation - Practitioner Signals Research
Post-Database Era Project, 2025
https://github.com/patrickmcfadin/post-database-era
```