# Quick Start Guide

## Prerequisites
1. Install Python 3.7+
2. Install PostgreSQL 12+
3. Install Python packages: `pip install -r requirements.txt`

## Database Setup
1. Start PostgreSQL service
2. Create database:
   ```sql
   CREATE DATABASE online_retail_db;
   ```
3. Update credentials in `3_database_import.py` and `4_sql_queries.py` if needed

## Run Analysis
```bash
python run_all.py
```

This will:
1. Clean the data → `output/online_retail_cleaned.csv`
2. Create visualizations → `output/visualizations/`
3. Import to PostgreSQL → `online_retail_db.online_retail`
4. Run queries → `output/queries/`

## Output Structure
```
output/
├── online_retail_cleaned.csv      # Cleaned dataset
├── cleaning_summary.json          # Cleaning statistics
├── database_info.json             # Database info
├── visualizations/                # 12 PNG charts
└── queries/                       # CSV results + business_answers.json
```

## Business Questions Answered
1. **Best Customers**: See `queries/1_best_customers_by_revenue.csv` and `queries/2_best_customers_by_frequency.csv`
2. **Best Sales Time**: See `queries/3_sales_by_time_of_day.csv`, `queries/4_sales_by_day_of_week.csv`, `queries/5_sales_by_hour.csv`
3. **Products Bought Together**: See `queries/6_products_bought_together.csv`

Quick answers in: `queries/business_answers.json`

## Troubleshooting
- **Database connection error**: Check PostgreSQL is running and credentials are correct
- **Missing packages**: Run `pip install -r requirements.txt`
- **File not found**: Ensure `Online Retail.xlsx` is in the project root
- **Visualization errors**: Ensure plotnine is installed: `pip install plotnine`

