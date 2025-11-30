#!/usr/bin/env python
# coding: utf-8

"""
Data Cleaning Script for Online Retail Dataset
Applies various cleaning techniques based on provided examples
"""

import pandas as pd
import numpy as np
import os

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

print("Loading dataset...")
# Load the dataset
data = pd.read_excel('Online Retail.xlsx')

print(f"Initial dataset shape: {data.shape}")
print(f"Initial missing values:\n{data.isnull().sum()}")

# Save initial statistics
initial_stats = {
    'total_rows': data.shape[0],
    'missing_description': data['Description'].isnull().sum(),
    'missing_customerid': data['CustomerID'].isnull().sum(),
    'negative_quantities': (data['Quantity'] < 0).sum(),
    'invalid_prices': (data['UnitPrice'] <= 0).sum(),
    'cancelled_invoices': data['InvoiceNo'].astype(str).str.startswith('C').sum()
}

# 1. Clean Incorrect Formats - Clean Description column
print("\n=== Cleaning Description Column ===")
initial_description_count = data['Description'].notna().sum()

# Remove leading/trailing whitespace and convert to string
data['Description'] = data['Description'].astype(str).str.strip()

# Replace common variations (similar to the pet example)
# Replace empty strings and 'nan' with actual NaN
data['Description'] = data['Description'].replace(['', 'nan', 'NaN'], np.nan)

final_description_count = data['Description'].notna().sum()
print(f"Descriptions before cleaning: {initial_description_count}")
print(f"Descriptions after cleaning: {final_description_count}")

# 2. Handle Missing Data - Identify missing values
print("\n=== Identifying Missing Data ===")
missing_description = data['Description'].isnull().sum()
missing_customerid = data['CustomerID'].isnull().sum()
total_rows = data.shape[0]

percentage_missing_description = (missing_description / total_rows) * 100
percentage_missing_customerid = (missing_customerid / total_rows) * 100

print(f"Missing Description values: {missing_description} ({percentage_missing_description:.2f}%)")
print(f"Missing CustomerID values: {missing_customerid} ({percentage_missing_customerid:.2f}%)")

# 3. Impute Missing Values from Internal Data
print("\n=== Imputing Missing CustomerID ===")
# For CustomerID, we'll use mode (most frequent customer ID) for imputation
# But first, let's check if we should drop rows with missing CustomerID for analysis
# For now, we'll create a flag and keep them for reference

# Create a flag for missing CustomerID
data['has_customerid'] = data['CustomerID'].notna().astype(int)

# For rows with missing CustomerID, we could impute with 0 or drop them
# Since CustomerID is critical for customer analysis, we'll keep a separate dataset
# For now, we'll impute with 0 (representing unknown customers)
data['CustomerID_imputed'] = data['CustomerID'].fillna(0).astype(int)

# For Description, we'll impute with 'UNKNOWN' since it's categorical
data['Description_imputed'] = data['Description'].fillna('UNKNOWN')

# 4. Remove Invalid Records
print("\n=== Removing Invalid Records ===")
# Remove cancelled invoices (InvoiceNo starting with 'C')
data_cleaned = data[~data['InvoiceNo'].astype(str).str.startswith('C')].copy()

# Remove rows with negative or zero quantities (returns/cancellations)
data_cleaned = data_cleaned[data_cleaned['Quantity'] > 0].copy()

# Remove rows with zero or negative prices
data_cleaned = data_cleaned[data_cleaned['UnitPrice'] > 0].copy()

print(f"Rows after removing cancelled invoices: {data_cleaned.shape[0]}")
print(f"Rows removed: {data.shape[0] - data_cleaned.shape[0]}")

# 5. Create Derived Variables
print("\n=== Creating Derived Variables ===")
# Calculate total revenue per transaction
data_cleaned['TotalRevenue'] = data_cleaned['Quantity'] * data_cleaned['UnitPrice']

# Extract date components
data_cleaned['InvoiceDate'] = pd.to_datetime(data_cleaned['InvoiceDate'])
data_cleaned['Year'] = data_cleaned['InvoiceDate'].dt.year
data_cleaned['Month'] = data_cleaned['InvoiceDate'].dt.month
data_cleaned['Day'] = data_cleaned['InvoiceDate'].dt.day
data_cleaned['DayOfWeek'] = data_cleaned['InvoiceDate'].dt.day_name()
data_cleaned['Hour'] = data_cleaned['InvoiceDate'].dt.hour
data_cleaned['Date'] = data_cleaned['InvoiceDate'].dt.date

# Create a categorical variable for time of day
def categorize_hour(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

data_cleaned['TimeOfDay'] = data_cleaned['Hour'].apply(categorize_hour)

# Create a boolean variable for high-value transactions (above median)
median_revenue = data_cleaned['TotalRevenue'].median()
data_cleaned['HighValueTransaction'] = (data_cleaned['TotalRevenue'] > median_revenue).astype(int)

# 6. Identify Extreme Data Values
print("\n=== Identifying Extreme Data Values ===")
# Check for extreme quantities
qty_5th = data_cleaned['Quantity'].quantile(0.05)
qty_95th = data_cleaned['Quantity'].quantile(0.95)
qty_99th = data_cleaned['Quantity'].quantile(0.99)

price_5th = data_cleaned['UnitPrice'].quantile(0.05)
price_95th = data_cleaned['UnitPrice'].quantile(0.95)
price_99th = data_cleaned['UnitPrice'].quantile(0.99)

revenue_5th = data_cleaned['TotalRevenue'].quantile(0.05)
revenue_95th = data_cleaned['TotalRevenue'].quantile(0.95)
revenue_99th = data_cleaned['TotalRevenue'].quantile(0.99)

print(f"Quantity - 5th percentile: {qty_5th}, 95th percentile: {qty_95th}, 99th percentile: {qty_99th}")
print(f"UnitPrice - 5th percentile: {price_5th}, 95th percentile: {price_95th}, 99th percentile: {price_99th}")
print(f"TotalRevenue - 5th percentile: {revenue_5th}, 95th percentile: {revenue_95th}, 99th percentile: {revenue_99th}")

# Flag extreme values (beyond 99th percentile)
data_cleaned['ExtremeQuantity'] = (data_cleaned['Quantity'] > qty_99th).astype(int)
data_cleaned['ExtremePrice'] = (data_cleaned['UnitPrice'] > price_99th).astype(int)
data_cleaned['ExtremeRevenue'] = (data_cleaned['TotalRevenue'] > revenue_99th).astype(int)

# 7. Clean StockCode and InvoiceNo formats
print("\n=== Cleaning StockCode and InvoiceNo ===")
# Ensure InvoiceNo is string
data_cleaned['InvoiceNo'] = data_cleaned['InvoiceNo'].astype(str).str.strip()

# Ensure StockCode is string
data_cleaned['StockCode'] = data_cleaned['StockCode'].astype(str).str.strip().str.upper()

# 8. Final data quality check
print("\n=== Final Data Quality Check ===")
print(f"Final dataset shape: {data_cleaned.shape}")
print(f"Final missing values:\n{data_cleaned[['Description_imputed', 'CustomerID_imputed']].isnull().sum()}")
print(f"Date range: {data_cleaned['InvoiceDate'].min()} to {data_cleaned['InvoiceDate'].max()}")
print(f"Unique customers: {data_cleaned[data_cleaned['CustomerID_imputed'] > 0]['CustomerID_imputed'].nunique()}")
print(f"Unique products: {data_cleaned['StockCode'].nunique()}")
print(f"Unique invoices: {data_cleaned['InvoiceNo'].nunique()}")

# Save cleaned dataset
output_file = 'output/online_retail_cleaned.csv'
data_cleaned.to_csv(output_file, index=False)
print(f"\nCleaned dataset saved to: {output_file}")

# Save cleaning summary statistics
summary_stats = {
    'initial_rows': initial_stats['total_rows'],
    'final_rows': data_cleaned.shape[0],
    'rows_removed': initial_stats['total_rows'] - data_cleaned.shape[0],
    'missing_description_initial': initial_stats['missing_description'],
    'missing_customerid_initial': initial_stats['missing_customerid'],
    'cancelled_invoices_removed': initial_stats['cancelled_invoices'],
    'negative_quantities_removed': initial_stats['negative_quantities'],
    'invalid_prices_removed': initial_stats['invalid_prices']
}

import json
with open('output/cleaning_summary.json', 'w') as f:
    summary_stats = {k: int(v) if hasattr(v, "__int__") else v for k, v in summary_stats.items()}
    json.dump(summary_stats, f, indent=2)

print("\n=== Data Cleaning Complete ===")
print("Summary statistics saved to: output/cleaning_summary.json")

