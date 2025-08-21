# Organizational and Procurement Datasets

This directory contains datasets focusing on organizational and procurement aspects of database compute/storage separation, addressing research questions around FinOps, contract structures, and organizational alignment.

## Dataset Overview

### FinOps and Budget Allocation

**2025-08-21__data__finops-budget-allocation__framework__models.csv**
- Enterprise patterns for independent budget allocation across industries
- Documents showback vs chargeback models, tagging strategies, and reserved instance policies
- 10 industry archetypes with budget allocation methodologies

**2025-08-21__data__finops-implementation__chargeback__cost-allocation.csv**
- Real-world FinOps implementation effectiveness metrics
- Tracks chargeback accuracy, automation levels, and organizational satisfaction
- Correlates tagging coverage with cost allocation success

### Contract Structures and Terms

**2025-08-21__data__enterprise-contracts__database__compute-storage-terms.csv**
- Anonymized database vendor contract structures
- Shows pricing independence, minimum commitments, and bursting allowances
- Covers 10 vendor categories from cloud-native to traditional enterprise

**2025-08-21__data__contract-analysis__commit-structures__anonymized-terms.csv**
- Detailed analysis of contract commitment structures and flexibility
- Documents discount tiers, overage penalties, and volume bonuses
- Represents enterprise contract tiers from startup to mega-deal

### Organizational Structure Evolution

**2025-08-21__data__organizational-structure__teams__cloud-center-excellence.csv**
- Team structure patterns and responsibility boundaries
- Maps compute/storage ownership across organizational maturity levels
- Covers cloud center of excellence evolution patterns

**2025-08-21__data__procurement-policy__governance__evolution-patterns.csv**
- Procurement policy evolution and governance maturity
- Documents authority distribution and compliance requirements
- Shows correlation between industry type and governance approach

### Database-Specific Pricing Patterns

**2025-08-21__data__database-pricing__reserved-spot__usage-patterns.csv**
- Reserved instance vs spot usage patterns by database workload type
- Cost optimization strategies for different database architectures
- Correlates business criticality with pricing model adoption

## Key Findings Summary

### FinOps Maturity Indicators
- **Tagging Coverage**: Higher coverage (85%+) correlates with 90%+ chargeback accuracy
- **Automation Score**: Organizations with score 8+ show 15% better cost predictability
- **Organizational Satisfaction**: Hybrid models (showback + selective chargeback) score highest

### Contract Structure Trends
- **Pricing Independence**: 70% of cloud-native vendors offer separate compute/storage pricing
- **Commitment Flexibility**: Monthly/quarterly true-up becoming standard for elastic workloads
- **Overage Penalties**: Range from 1.1x (serverless) to 4.0x (traditional licensing)

### Organizational Evolution Patterns
- **Team Boundaries**: Larger organizations (2000+ employees) separate storage/compute operations
- **Procurement Authority**: Cloud-native organizations delegate more authority to engineering teams
- **Governance Maturity**: Regulated industries maintain centralized oversight regardless of technology

### Database Workload Optimization
- **OLTP Production**: 80% reserved instances, minimal spot usage for predictability
- **Analytics/ML**: 50%+ spot usage acceptable due to fault-tolerant architectures
- **Dev/Test**: 70% spot usage common, driving 75% cost savings

## Research Implications

These datasets support the thesis that organizational structures and procurement policies are evolving to accommodate separated compute/storage models:

1. **Independent Budget Lines**: Evidence of separate compute/storage budget allocation in mature FinOps organizations
2. **Contract Evolution**: Vendor pricing models increasingly support independent scaling and billing
3. **Team Specialization**: Larger organizations developing specialized teams for compute vs storage operations
4. **Policy Adaptation**: Procurement policies evolving to support elastic, consumption-based models

## Data Quality and Limitations

- **Sample Representativeness**: Skewed toward cloud-native organizations actively pursuing separation
- **Anonymization**: Some contract terms simplified to protect commercially sensitive information
- **Temporal Relevance**: Organizational evolution ongoing; patterns may shift as market matures
- **Industry Variation**: Regulated industries show slower adoption and different patterns

## Usage Guidelines

These datasets are intended for:
- Organizational benchmark analysis
- Procurement strategy development
- FinOps maturity assessment
- Contract negotiation reference

All data has been anonymized and should be considered representative patterns rather than specific organizational details.