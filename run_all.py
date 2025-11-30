#!/usr/bin/env python
# coding: utf-8

"""
Main execution script
Runs all analysis steps in sequence
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              check=True, 
                              capture_output=False)
        print(f"\n✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error in {description}")
        print(f"Error code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n✗ Script not found: {script_name}")
        return False

def main():
    """Main execution function"""
    print("="*60)
    print("Online Retail Data Analysis Pipeline")
    print("="*60)
    
    # Check if dataset exists
    if not os.path.exists('Online Retail.xlsx'):
        print("\n✗ Error: Online Retail.xlsx not found!")
        print("Please ensure the dataset is in the current directory.")
        return
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    scripts = [
        ('1_data_cleaning.py', 'Data Cleaning'),
        ('2_data_visualization.py', 'Data Visualization'),
        ('3_database_import.py', 'Database Import'),
        ('4_sql_queries.py', 'SQL Queries and Business Analysis')
    ]
    
    results = []
    for script, description in scripts:
        success = run_script(script, description)
        results.append((script, description, success))
        
        if not success:
            print(f"\n⚠ Warning: {description} failed. Continuing with next step...")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("\nPipeline stopped by user.")
                break
    
    # Summary
    print("\n" + "="*60)
    print("Pipeline Execution Summary")
    print("="*60)
    
    for script, description, success in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"{status}: {description} ({script})")
    
    print("\n" + "="*60)
    print("All output files are in the 'output/' directory")
    print("="*60)

if __name__ == "__main__":
    main()

