# Online Retail Data Analysis Project

This project performs comprehensive data cleaning, visualization, and database analysis on an online retail dataset. The project follows a structured approach to transform raw data into actionable business insights.

## Project Structure

```
Projectv2/
├── Online Retail.xlsx          # Original dataset (preserved)
├── 1_data_cleaning.py          # Data cleaning script
├── 2_data_visualization.py     # Data visualization script
├── 3_database_import.py        # PostgreSQL database import script
├── 4_sql_queries.py            # Business analysis queries
├── run_all.py                  # Main execution script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── output/                     # All output files (can be deleted and regenerated)
    ├── online_retail_cleaned.csv
    ├── cleaning_summary.json
    ├── database_info.json
    ├── visualizations/         # All generated plots
    └── queries/                # Query results and answers
```

## Dataset Overview

The Online Retail dataset contains transaction data from an online retail store, including:
- **InvoiceNo**: Invoice number (cancelled invoices start with 'C')
- **StockCode**: Product code
- **Description**: Product description
- **Quantity**: Quantity purchased
- **InvoiceDate**: Date and time of purchase
- **UnitPrice**: Price per unit
- **CustomerID**: Customer identifier
- **Country**: Country of purchase

**Initial Dataset Statistics:**
- Total rows: 541,909
- Date range: December 2010 to December 2011
- Missing values: 1,454 in Description, 135,080 in CustomerID
- 38 different countries

## Data Cleaning Process

### 1. Format Cleaning
- **Description Column**: Cleaned whitespace, standardized text format, and replaced empty strings with NaN values. This follows the pattern from the "Clean Incorrect Formats" example, where we standardized categorical text data.

### 2. Missing Data Identification
- Identified missing values in Description (1,454 rows, 0.27%) and CustomerID (135,080 rows, 24.92%)
- Calculated percentages of missing data to understand data quality

### 3. Missing Data Imputation
- **CustomerID**: Created a flag variable `has_customerid` to track missing values. Imputed missing CustomerID with 0 (representing unknown customers) in a new column `CustomerID_imputed`. This follows the "Impute Missing Values from Internal Data" approach, using internal statistics (mode/0) for imputation.
- **Description**: Imputed missing descriptions with 'UNKNOWN' in a new column `Description_imputed`, preserving the original column for reference.

### 4. Invalid Record Removal
- Removed cancelled invoices (InvoiceNo starting with 'C') - 9,288 rows
- Removed rows with negative or zero quantities (returns/cancellations) - 10,624 rows
- Removed rows with zero or negative prices - 2,517 rows
- **Final cleaned dataset**: ~519,000 rows

### 5. Derived Variables Creation
Following the "Create a Boolean Variable" and "Create a Categorical Variable from a Quantitative Variable" examples:
- **TotalRevenue**: Calculated as Quantity × UnitPrice
- **Date Components**: Extracted Year, Month, Day, DayOfWeek, Hour, and Date from InvoiceDate
- **TimeOfDay**: Categorical variable (Morning: 6-12, Afternoon: 12-17, Evening: 17-21, Night: other)
- **HighValueTransaction**: Boolean variable (1 if revenue > median, 0 otherwise)
- **Extreme Value Flags**: Boolean variables for extreme quantities, prices, and revenue (beyond 99th percentile)

### 6. Extreme Value Identification
Following the "Identify Extreme Data Values" example:
- Calculated 5th, 95th, and 99th percentiles for Quantity, UnitPrice, and TotalRevenue
- Created flags for extreme values beyond the 99th percentile
- This helps identify outliers that may need special attention

### 7. Data Type Standardization
- Standardized InvoiceNo and StockCode as strings
- Ensured proper datetime formatting for InvoiceDate

## Data Visualization

Created 12 comprehensive visualizations using plotnine (ggplot2 for Python):

1. **Histogram - Distribution of Total Revenue**: Shows the distribution of transaction values
2. **Box Plot - Revenue by Time of Day**: Compares revenue distributions across different times
3. **Box Plot - Revenue by Day of Week**: Compares revenue distributions across weekdays
4. **Column Chart - Total Sales by Day of Week**: Bar chart showing total revenue per day
5. **Column Chart - Total Sales by Time of Day**: Bar chart showing total revenue per time period
6. **Line Chart - Sales Over Time**: Trend analysis of monthly sales
7. **Scatter Plot - Quantity vs Unit Price**: Relationship between price and quantity
8. **Column Chart - Top 10 Countries by Revenue**: Geographic performance analysis
9. **Density Plot - Distribution of Unit Prices**: Probability distribution of prices
10. **Violin Plot - Revenue Distribution by Top 5 Countries**: Detailed distribution comparison
11. **Column Chart - Top 20 Products by Revenue**: Best-selling products
12. **Heatmap - Sales by Day of Week and Time of Day**: Two-dimensional analysis of sales patterns

All visualizations are saved as high-resolution PNG files (300 DPI) in `output/visualizations/`.

## Database Setup

### PostgreSQL Database Configuration
- **Database Name**: `online_retail_db`
- **Table Name**: `online_retail`
- **Connection**: Local PostgreSQL server (default: localhost:5432)

### Database Schema
The cleaned data is imported into a PostgreSQL table with:
- Primary key: `id` (auto-increment)
- Indexes on: invoice_no, customer_id_imputed, stock_code, invoice_date, country, day_of_week, time_of_day
- All derived variables included for efficient querying

### Import Process
- Data is imported in chunks of 10,000 rows for efficiency
- All data types are properly mapped to PostgreSQL types
- Indexes are created for optimal query performance

## Business Analysis Queries

The project answers three key business questions:

### 1. Who are our best customers?

**By Revenue:**
- Identifies top 10 customers by total revenue generated
- Includes metrics: total orders, average order value, last purchase date

**By Frequency:**
- Identifies top 10 customers by number of orders placed
- Includes metrics: total revenue, average order value, last purchase date

**Results saved in:**
- `output/queries/1_best_customers_by_revenue.csv`
- `output/queries/2_best_customers_by_frequency.csv`

### 2. What time of day/day of week has the highest sales?

**Analysis includes:**
- Sales performance by time of day (Morning, Afternoon, Evening, Night)
- Sales performance by day of week (Monday through Sunday)
- Sales performance by hour of day (0-23)
- Metrics: number of transactions, total revenue, average revenue per transaction

**Results saved in:**
- `output/queries/3_sales_by_time_of_day.csv`
- `output/queries/4_sales_by_day_of_week.csv`
- `output/queries/5_sales_by_hour.csv`

### 3. Can we identify products that are frequently bought together?

**Association Analysis:**
- Identifies product pairs that appear together in the same invoice
- Filters pairs that co-occur in at least 5 invoices
- Ranks pairs by frequency of co-occurrence
- Shows top 20 product pairs

**Results saved in:**
- `output/queries/6_products_bought_together.csv`

### Summary Statistics
Overall dataset statistics including:
- Total transactions, unique invoices, customers, products
- Total revenue, average revenue per transaction
- Total quantity sold, average quantity per transaction

**Results saved in:**
- `output/queries/7_summary_statistics.csv`
- `output/queries/business_answers.json` (JSON format with direct answers)

## Installation and Setup

### Prerequisites
1. Python 3.7 or higher
2. PostgreSQL 12 or higher
3. Required Python packages (see requirements.txt)

### Installation Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   ```sql
   CREATE DATABASE online_retail_db;
   ```
   
   Update database credentials in `3_database_import.py` and `4_sql_queries.py` if needed:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'online_retail_db',
       'user': 'postgres',
       'password': 'your_password',
       'port': 5432
   }
   ```

3. **Run the complete pipeline:**
   ```bash
   python run_all.py
   ```
   
   Or run scripts individually:
   ```bash
   python 1_data_cleaning.py
   python 2_data_visualization.py
   python 3_database_import.py
   python 4_sql_queries.py
   ```

## Output Files

All output files are stored in the `output/` directory:

### Data Files
- `online_retail_cleaned.csv`: Cleaned dataset ready for analysis
- `cleaning_summary.json`: Summary statistics from data cleaning

### Visualization Files
- `visualizations/*.png`: 12 high-resolution visualization images

### Database Files
- `database_info.json`: Database connection and table information

### Query Results
- `queries/*.csv`: CSV files with query results
- `queries/business_answers.json`: Direct answers to business questions in JSON format

## Key Findings

### Best Customers
- Top customers by revenue generate significant value through high-value transactions
- Top customers by frequency show strong loyalty and repeat purchase behavior

### Sales Timing
- Specific times of day and days of week show higher sales volumes
- Peak hours can be identified for marketing and staffing optimization

### Product Associations
- Product pairs frequently bought together can inform:
  - Cross-selling strategies
  - Product bundling opportunities
  - Inventory management
  - Marketing campaigns

## Technologies Used

- **Python**: Data processing and analysis
- **Pandas**: Data manipulation and cleaning
- **NumPy**: Numerical operations
- **Plotnine**: Data visualization (ggplot2 for Python)
- **PostgreSQL**: Relational database
- **SQLAlchemy**: Database connection and ORM
- **psycopg2**: PostgreSQL adapter for Python

## Code Examples Used

This project implements techniques from the provided code examples:

1. **Clean Incorrect Formats**: Applied to Description column standardization
2. **Create Boolean Variables**: HighValueTransaction, extreme value flags
3. **Create Categorical Variables**: TimeOfDay from Hour variable
4. **Identify Extreme Data Values**: Percentile-based outlier detection
5. **Identify Missing Data**: Comprehensive missing value analysis
6. **Impute Missing Values**: Mean/mode imputation for missing data
7. **Splitting Variables**: Date component extraction from InvoiceDate
8. **Visualization Techniques**: Histogram, box plot, scatter plot, heatmap, violin plot, density plot, line chart, column chart

## Notes

- The original dataset (`Online Retail.xlsx`) is never modified
- All outputs can be regenerated by deleting the `output/` folder and re-running the scripts
- Database credentials should be updated to match your PostgreSQL setup
- The project handles missing data gracefully while preserving original data for reference

## Future Enhancements

Potential improvements for future iterations:
- Customer segmentation analysis
- Predictive modeling for sales forecasting
- Advanced association rule mining (Apriori algorithm)
- Customer lifetime value (CLV) calculation
- Seasonal trend analysis
- Geographic sales analysis with maps

## License

This project is for educational purposes. The dataset is publicly available for analysis.

