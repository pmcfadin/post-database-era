#!/usr/bin/env python3
"""
Dataset Validation Script for Organizational and Procurement Data
Validates data integrity, relationships, and statistical consistency
"""

import pandas as pd
import os
import sys
from pathlib import Path

def validate_csv_files(directory):
    """Validate all CSV files in the directory"""
    
    csv_files = list(Path(directory).glob("*.csv"))
    print(f"Found {len(csv_files)} CSV files to validate")
    
    validation_results = {}
    
    for csv_file in csv_files:
        print(f"\nValidating {csv_file.name}...")
        
        try:
            df = pd.read_csv(csv_file)
            
            # Basic validation
            validation_results[csv_file.name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'missing_values': df.isnull().sum().sum(),
                'duplicate_rows': df.duplicated().sum(),
                'data_types': df.dtypes.to_dict()
            }
            
            # Check for reasonable value ranges
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                if 'percent' in col.lower():
                    # Percentage columns should be 0-100
                    invalid_pct = ((df[col] < 0) | (df[col] > 100)).sum()
                    if invalid_pct > 0:
                        print(f"  WARNING: {col} has {invalid_pct} values outside 0-100 range")
                
                if 'usd' in col.lower() or 'commit' in col.lower():
                    # Currency columns should be positive
                    negative_values = (df[col] < 0).sum()
                    if negative_values > 0:
                        print(f"  WARNING: {col} has {negative_values} negative values")
            
            print(f"  ✓ {len(df)} rows, {len(df.columns)} columns")
            print(f"  ✓ {df.isnull().sum().sum()} missing values")
            
        except Exception as e:
            print(f"  ✗ Error reading {csv_file.name}: {e}")
            validation_results[csv_file.name] = {'error': str(e)}
    
    return validation_results

def check_metadata_coverage(directory):
    """Check that all CSV files have corresponding metadata files"""
    
    csv_files = set(f.stem for f in Path(directory).glob("*.csv"))
    meta_files = set(f.stem.replace('.meta', '') for f in Path(directory).glob("*.meta.yaml"))
    
    missing_metadata = csv_files - meta_files
    orphaned_metadata = meta_files - csv_files
    
    print(f"\nMetadata Coverage Check:")
    print(f"  CSV files: {len(csv_files)}")
    print(f"  Metadata files: {len(meta_files)}")
    
    if missing_metadata:
        print(f"  ✗ Missing metadata: {missing_metadata}")
    else:
        print(f"  ✓ All CSV files have metadata")
    
    if orphaned_metadata:
        print(f"  ⚠ Orphaned metadata: {orphaned_metadata}")

def analyze_cross_dataset_relationships(directory):
    """Analyze relationships between datasets"""
    
    print(f"\nCross-Dataset Relationship Analysis:")
    
    # Load key datasets for relationship analysis
    try:
        finops_df = pd.read_csv(directory / "2025-08-21__data__finops-budget-allocation__framework__models.csv")
        contracts_df = pd.read_csv(directory / "2025-08-21__data__enterprise-contracts__database__compute-storage-terms.csv")
        org_structure_df = pd.read_csv(directory / "2025-08-21__data__organizational-structure__teams__cloud-center-excellence.csv")
        
        # Check organization type consistency
        finops_orgs = set(finops_df['organization_type'])
        structure_industries = set(org_structure_df['industry'])
        
        print(f"  Organization types in FinOps data: {len(finops_orgs)}")
        print(f"  Industries in structure data: {len(structure_industries)}")
        
        # Analyze contract vs organization patterns
        independent_pricing = contracts_df[
            (contracts_df['compute_pricing_independence'] == 'yes') & 
            (contracts_df['storage_pricing_independence'] == 'yes')
        ]
        print(f"  Vendors with full pricing independence: {len(independent_pricing)}")
        
        # Check for logical consistency
        mature_ccoe = org_structure_df[org_structure_df['ccoe_maturity'].isin(['mature', 'advanced'])]
        print(f"  Organizations with mature CCOE: {len(mature_ccoe)}")
        
    except Exception as e:
        print(f"  ✗ Error in cross-dataset analysis: {e}")

def main():
    """Main validation function"""
    
    directory = Path(__file__).parent
    print(f"Validating datasets in: {directory}")
    
    # Validate CSV files
    validation_results = validate_csv_files(directory)
    
    # Check metadata coverage
    check_metadata_coverage(directory)
    
    # Analyze cross-dataset relationships
    analyze_cross_dataset_relationships(directory)
    
    # Summary
    total_files = len(validation_results)
    error_files = sum(1 for v in validation_results.values() if 'error' in v)
    
    print(f"\nValidation Summary:")
    print(f"  Total files: {total_files}")
    print(f"  Successful: {total_files - error_files}")
    print(f"  Errors: {error_files}")
    
    if error_files == 0:
        print("  ✓ All datasets passed validation")
        return 0
    else:
        print("  ✗ Some datasets failed validation")
        return 1

if __name__ == "__main__":
    sys.exit(main())