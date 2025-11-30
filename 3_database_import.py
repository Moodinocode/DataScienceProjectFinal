#!/usr/bin/env python
# coding: utf-8

"""
PostgreSQL Database Import Script
Creates database, tables, and imports cleaned data
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from sqlalchemy import create_engine, text
import json

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'online_retail_db',
    'user': 'postgres',  # Change as needed
    'password': '123456',  # Change as needed
    'port': 5432
}

print("Loading cleaned dataset...")
# Load the cleaned dataset
data = pd.read_csv('output/online_retail_cleaned.csv')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

print(f"Dataset shape: {data.shape}")

# Create SQLAlchemy engine for easier data import
try:
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(connection_string)
    
    print("\n=== Creating Database Tables ===")
    
    # Drop existing table if it exists (for re-running)
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS online_retail CASCADE;"))
        conn.commit()
    
    # Create table with appropriate schema
    create_table_sql = """
    CREATE TABLE online_retail (
        id SERIAL PRIMARY KEY,
        invoice_no VARCHAR(50),
        stock_code VARCHAR(50),
        description TEXT,
        quantity INTEGER,
        invoice_date TIMESTAMP,
        unit_price DECIMAL(10, 2),
        customer_id INTEGER,
        country VARCHAR(100),
        description_imputed TEXT,
        customer_id_imputed INTEGER,
        total_revenue DECIMAL(10, 2),
        year INTEGER,
        month INTEGER,
        day INTEGER,
        day_of_week VARCHAR(20),
        hour INTEGER,
        date DATE,
        time_of_day VARCHAR(20),
        high_value_transaction INTEGER,
        extreme_quantity INTEGER,
        extreme_price INTEGER,
        extreme_revenue INTEGER,
        has_customerid INTEGER
    );
    
    CREATE INDEX idx_invoice_no ON online_retail(invoice_no);
    CREATE INDEX idx_customer_id ON online_retail(customer_id_imputed);
    CREATE INDEX idx_stock_code ON online_retail(stock_code);
    CREATE INDEX idx_invoice_date ON online_retail(invoice_date);
    CREATE INDEX idx_country ON online_retail(country);
    CREATE INDEX idx_day_of_week ON online_retail(day_of_week);
    CREATE INDEX idx_time_of_day ON online_retail(time_of_day);
    """
    
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
    
    print("Table created successfully!")
    
    # Prepare data for import
    print("\n=== Preparing Data for Import ===")
    # Rename columns to match database schema
    data_db = data.copy()
    data_db.columns = [col.lower().replace(' ', '_') for col in data_db.columns]
    
    # Select only columns that exist in the table
    columns_to_import = [
        'invoice_no', 'stock_code', 'description', 'quantity', 'invoice_date',
        'unit_price', 'customerid', 'country', 'description_imputed',
        'customerid_imputed', 'totalrevenue', 'year', 'month', 'day',
        'dayofweek', 'hour', 'date', 'timeofday', 'highvaluetransaction',
        'extremequantity', 'extremeprice', 'extreverevenue', 'has_customerid'
    ]
    
    # Map column names
    column_mapping = {
        'invoiceno': 'invoice_no',
        'stockcode': 'stock_code',
        'invoicedate': 'invoice_date',
        'unitprice': 'unit_price',
        'customerid': 'customer_id',
        'customerid_imputed': 'customer_id_imputed',
        'totalrevenue': 'total_revenue',
        'dayofweek': 'day_of_week',
        'timeofday': 'time_of_day',
        'highvaluetransaction': 'high_value_transaction',
        'extremequantity': 'extreme_quantity',
        'extremeprice': 'extreme_price',
        'extremerevenue': 'extreme_revenue'
    }
    
    data_db = data_db.rename(columns=column_mapping)
    
    # Ensure date column is properly formatted
    data_db['date'] = pd.to_datetime(data_db['date']).dt.date
    
    # Select and reorder columns to match table schema
    db_columns = [
        'invoice_no', 'stock_code', 'description', 'quantity', 'invoice_date',
        'unit_price', 'customer_id', 'country', 'description_imputed',
        'customer_id_imputed', 'total_revenue', 'year', 'month', 'day',
        'day_of_week', 'hour', 'date', 'time_of_day', 'high_value_transaction',
        'extreme_quantity', 'extreme_price', 'extreme_revenue', 'has_customerid'
    ]
    
    data_db = data_db[db_columns]
    
    print(f"Data prepared: {data_db.shape}")
    print(f"Columns: {list(data_db.columns)}")
    
    # Import data in chunks
    print("\n=== Importing Data to Database ===")
    chunk_size = 10000
    total_chunks = len(data_db) // chunk_size + (1 if len(data_db) % chunk_size else 0)
    
    for i in range(0, len(data_db), chunk_size):
        chunk = data_db.iloc[i:i+chunk_size]
        chunk_num = i // chunk_size + 1
        print(f"Importing chunk {chunk_num}/{total_chunks} ({len(chunk)} rows)...")
        
        chunk.to_sql('online_retail', engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
    print("\n=== Verifying Import ===")
    # Verify the import
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM online_retail;"))
        row_count = result.fetchone()[0]
        print(f"Total rows in database: {row_count}")
        
        result = conn.execute(text("SELECT MIN(invoice_date), MAX(invoice_date) FROM online_retail;"))
        date_range = result.fetchone()
        print(f"Date range: {date_range[0]} to {date_range[1]}")
        
        result = conn.execute(text("SELECT COUNT(DISTINCT customer_id_imputed) FROM online_retail WHERE customer_id_imputed > 0;"))
        unique_customers = result.fetchone()[0]
        print(f"Unique customers: {unique_customers}")
        
        result = conn.execute(text("SELECT COUNT(DISTINCT stock_code) FROM online_retail;"))
        unique_products = result.fetchone()[0]
        print(f"Unique products: {unique_products}")
    
    # Save database configuration (without password) for reference
    db_info = {
        'host': DB_CONFIG['host'],
        'database': DB_CONFIG['database'],
        'port': DB_CONFIG['port'],
        'user': DB_CONFIG['user'],
        'table_name': 'online_retail',
        'total_rows': int(row_count)
    }
    
    with open('output/database_info.json', 'w') as f:
        json.dump(db_info, f, indent=2)
    
    print("\n=== Database Import Complete ===")
    print("Database information saved to: output/database_info.json")
    print("\nNOTE: Please update the database credentials in this script if needed.")
    
except Exception as e:
    print(f"\nError: {e}")
    print("\nPlease ensure:")
    print("1. PostgreSQL is installed and running")
    print("2. Database 'online_retail_db' exists (or create it manually)")
    print("3. User credentials are correct")
    print("4. Required Python packages are installed: psycopg2, sqlalchemy, pandas")
    print("\nTo create the database manually, run:")
    print("  CREATE DATABASE online_retail_db;")

