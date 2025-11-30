#!/usr/bin/env python
# coding: utf-8

"""
SQL Queries Script for Business Analysis
Answers key business questions about the online retail dataset
"""

import pandas as pd
from sqlalchemy import create_engine
import json
import os

# Database configuration (should match 3_database_import.py)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'online_retail_db',
    'user': 'postgres',
    'password': '123456',
    'port': 5432
}

# Create output directory
os.makedirs('output/queries', exist_ok=True)

try:
    # Create connection
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(connection_string)
    
    print("=== Running Business Analysis Queries ===\n")
    
    # Query 1: Best Customers by Revenue
    print("1. Best Customers by Revenue (Top 10)")
    print("-" * 50)
    query1 = """
    SELECT 
        customer_id_imputed AS customer_id,
        COUNT(DISTINCT invoice_no) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_order_value,
        MAX(invoice_date) AS last_purchase_date
    FROM online_retail
    WHERE customer_id_imputed > 0
    GROUP BY customer_id_imputed
    ORDER BY total_revenue DESC
    LIMIT 10;
    """
    
    df1 = pd.read_sql(query1, engine)
    print(df1.to_string(index=False))
    df1.to_csv('output/queries/1_best_customers_by_revenue.csv', index=False)
    print(f"\nResults saved to: output/queries/1_best_customers_by_revenue.csv\n")
    
    # Query 2: Best Customers by Frequency
    print("2. Best Customers by Frequency (Top 10)")
    print("-" * 50)
    query2 = """
    SELECT 
        customer_id_imputed AS customer_id,
        COUNT(DISTINCT invoice_no) AS total_orders,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_order_value,
        MAX(invoice_date) AS last_purchase_date
    FROM online_retail
    WHERE customer_id_imputed > 0
    GROUP BY customer_id_imputed
    ORDER BY total_orders DESC
    LIMIT 10;
    """
    
    df2 = pd.read_sql(query2, engine)
    print(df2.to_string(index=False))
    df2.to_csv('output/queries/2_best_customers_by_frequency.csv', index=False)
    print(f"\nResults saved to: output/queries/2_best_customers_by_frequency.csv\n")
    
    # Query 3: Sales by Time of Day
    print("3. Sales Performance by Time of Day")
    print("-" * 50)
    query3 = """
    SELECT 
        time_of_day,
        COUNT(DISTINCT invoice_no) AS number_of_transactions,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_revenue_per_transaction,
        SUM(quantity) AS total_quantity_sold
    FROM online_retail
    GROUP BY time_of_day
    ORDER BY 
        CASE time_of_day
            WHEN 'Morning' THEN 1
            WHEN 'Afternoon' THEN 2
            WHEN 'Evening' THEN 3
            WHEN 'Night' THEN 4
        END;
    """
    
    df3 = pd.read_sql(query3, engine)
    print(df3.to_string(index=False))
    df3.to_csv('output/queries/3_sales_by_time_of_day.csv', index=False)
    print(f"\nResults saved to: output/queries/3_sales_by_time_of_day.csv\n")
    
    # Query 4: Sales by Day of Week
    print("4. Sales Performance by Day of Week")
    print("-" * 50)
    query4 = """
    SELECT 
        day_of_week,
        COUNT(DISTINCT invoice_no) AS number_of_transactions,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_revenue_per_transaction,
        SUM(quantity) AS total_quantity_sold
    FROM online_retail
    GROUP BY day_of_week
    ORDER BY 
        CASE day_of_week
            WHEN 'Monday' THEN 1
            WHEN 'Tuesday' THEN 2
            WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4
            WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6
            WHEN 'Sunday' THEN 7
        END;
    """
    
    df4 = pd.read_sql(query4, engine)
    print(df4.to_string(index=False))
    df4.to_csv('output/queries/4_sales_by_day_of_week.csv', index=False)
    print(f"\nResults saved to: output/queries/4_sales_by_day_of_week.csv\n")
    
    # Query 5: Best Hour of Day for Sales
    print("5. Sales Performance by Hour of Day (Top 10)")
    print("-" * 50)
    query5 = """
    SELECT 
        hour,
        COUNT(DISTINCT invoice_no) AS number_of_transactions,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_revenue_per_transaction
    FROM online_retail
    GROUP BY hour
    ORDER BY total_revenue DESC
    LIMIT 10;
    """
    
    df5 = pd.read_sql(query5, engine)
    print(df5.to_string(index=False))
    df5.to_csv('output/queries/5_sales_by_hour.csv', index=False)
    print(f"\nResults saved to: output/queries/5_sales_by_hour.csv\n")
    
    # Query 6: Products Frequently Bought Together (Association Analysis)
    print("6. Products Frequently Bought Together (Top 20 Pairs)")
    print("-" * 50)
    query6 = """
    WITH invoice_products AS (
        SELECT DISTINCT
            invoice_no,
            stock_code,
            description_imputed
        FROM online_retail
        WHERE customer_id_imputed > 0
    ),
    product_pairs AS (
        SELECT 
            ip1.stock_code AS product1_code,
            ip1.description_imputed AS product1_desc,
            ip2.stock_code AS product2_code,
            ip2.description_imputed AS product2_desc,
            COUNT(DISTINCT ip1.invoice_no) AS co_occurrence_count
        FROM invoice_products ip1
        INNER JOIN invoice_products ip2 
            ON ip1.invoice_no = ip2.invoice_no
            AND ip1.stock_code < ip2.stock_code
        GROUP BY 
            ip1.stock_code, ip1.description_imputed,
            ip2.stock_code, ip2.description_imputed
        HAVING COUNT(DISTINCT ip1.invoice_no) >= 5
    )
    SELECT 
        product1_code,
        LEFT(product1_desc, 40) AS product1_description,
        product2_code,
        LEFT(product2_desc, 40) AS product2_description,
        co_occurrence_count
    FROM product_pairs
    ORDER BY co_occurrence_count DESC
    LIMIT 20;
    """
    
    df6 = pd.read_sql(query6, engine)
    print(df6.to_string(index=False))
    df6.to_csv('output/queries/6_products_bought_together.csv', index=False)
    print(f"\nResults saved to: output/queries/6_products_bought_together.csv\n")
    
    # Query 7: Summary Statistics
    print("7. Overall Summary Statistics")
    print("-" * 50)
    query7 = """
    SELECT 
        COUNT(*) AS total_transactions,
        COUNT(DISTINCT invoice_no) AS unique_invoices,
        COUNT(DISTINCT customer_id_imputed) AS unique_customers,
        COUNT(DISTINCT stock_code) AS unique_products,
        SUM(total_revenue) AS total_revenue,
        AVG(total_revenue) AS avg_revenue_per_transaction,
        SUM(quantity) AS total_quantity_sold,
        AVG(quantity) AS avg_quantity_per_transaction
    FROM online_retail
    WHERE customer_id_imputed > 0;
    """
    
    df7 = pd.read_sql(query7, engine)
    print(df7.to_string(index=False))
    df7.to_csv('output/queries/7_summary_statistics.csv', index=False)
    print(f"\nResults saved to: output/queries/7_summary_statistics.csv\n")
    
    # Create a summary document with answers to business questions
    print("=== Business Questions Answers ===")
    print("-" * 50)
    
    # Answer 1: Best Customers
    best_customer_revenue = df1.iloc[0]
    best_customer_freq = df2.iloc[0]
    
    # Answer 2: Best Time/Day
    best_time = df3.loc[df3['total_revenue'].idxmax()]
    best_day = df4.loc[df4['total_revenue'].idxmax()]
    best_hour_row = df5.iloc[0]
    
    # Answer 3: Products bought together
    top_pair = df6.iloc[0] if len(df6) > 0 else None
    
    answers = {
        "question_1_best_customers": {
            "by_revenue": {
                "customer_id": int(best_customer_revenue['customer_id']),
                "total_revenue": float(best_customer_revenue['total_revenue']),
                "total_orders": int(best_customer_revenue['total_orders'])
            },
            "by_frequency": {
                "customer_id": int(best_customer_freq['customer_id']),
                "total_orders": int(best_customer_freq['total_orders']),
                "total_revenue": float(best_customer_freq['total_revenue'])
            }
        },
        "question_2_best_time_for_sales": {
            "time_of_day": str(best_time['time_of_day']),
            "total_revenue": float(best_time['total_revenue']),
            "day_of_week": str(best_day['day_of_week']),
            "day_total_revenue": float(best_day['total_revenue']),
            "hour_of_day": int(best_hour_row['hour']),
            "hour_total_revenue": float(best_hour_row['total_revenue'])
        },
        "question_3_products_bought_together": {
            "top_pair": {
                "product1": f"{top_pair['product1_code']} - {top_pair['product1_description']}" if top_pair is not None else "N/A",
                "product2": f"{top_pair['product2_code']} - {top_pair['product2_description']}" if top_pair is not None else "N/A",
                "co_occurrence_count": int(top_pair['co_occurrence_count']) if top_pair is not None else 0
            } if top_pair is not None else "No significant pairs found"
        }
    }
    
    # Save answers
    with open('output/queries/business_answers.json', 'w') as f:
        json.dump(answers, f, indent=2)
    
    # Print answers
    print("\nANSWERS TO BUSINESS QUESTIONS:")
    print("=" * 50)
    print("\n1. Who are our best customers?")
    print(f"   By Revenue: Customer ID {best_customer_revenue['customer_id']} with ${best_customer_revenue['total_revenue']:,.2f} in total revenue")
    print(f"   By Frequency: Customer ID {best_customer_freq['customer_id']} with {best_customer_freq['total_orders']} orders")
    
    print("\n2. What time of day/day of week has the highest sales?")
    print(f"   Time of Day: {best_time['time_of_day']} with ${best_time['total_revenue']:,.2f} in total revenue")
    print(f"   Day of Week: {best_day['day_of_week']} with ${best_day['total_revenue']:,.2f} in total revenue")
    print(f"   Hour of Day: {best_hour_row['hour']}:00 with ${best_hour_row['total_revenue']:,.2f} in total revenue")
    
    print("\n3. Can we identify products that are frequently bought together?")
    if top_pair is not None:
        print(f"   Top Pair: {top_pair['product1_code']} & {top_pair['product2_code']}")
        print(f"   Co-occurred in {top_pair['co_occurrence_count']} invoices together")
    else:
        print("   No significant product pairs found")
    
    print("\n=== All Queries Complete ===")
    print("All query results saved to: output/queries/")
    print("Business answers saved to: output/queries/business_answers.json")
    
except Exception as e:
    print(f"\nError: {e}")
    print("\nPlease ensure:")
    print("1. Database is set up and data is imported (run 3_database_import.py first)")
    print("2. Database credentials are correct")
    print("3. Required Python packages are installed: pandas, sqlalchemy")

