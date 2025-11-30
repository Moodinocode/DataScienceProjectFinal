#!/usr/bin/env python
# coding: utf-8

"""
Data Visualization Script for Online Retail Dataset
Creates various visualizations using plotnine
"""

import pandas as pd
import numpy as np
from plotnine import *
import os

# Create output directory if it doesn't exist
os.makedirs('output/visualizations', exist_ok=True)

print("Loading cleaned dataset...")
# Load the cleaned dataset
data = pd.read_csv('output/online_retail_cleaned.csv')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

print(f"Dataset shape: {data.shape}")

# 1. Histogram - Distribution of Total Revenue
print("\nCreating histogram: Distribution of Total Revenue...")
plot1 = (ggplot(data, aes(x='TotalRevenue')) +
         geom_histogram(bins=50, fill='#0072b2', color='black') +
         xlab('Total Revenue per Transaction ($)') +
         ylab('Frequency') +
         ggtitle('Distribution of Total Revenue per Transaction') +
         theme(figure_size=(10, 6))
        )
plot1.save('output/visualizations/1_histogram_revenue.png', dpi=300)
print("Saved: output/visualizations/1_histogram_revenue.png")

# 2. Box Plot - Revenue by Time of Day
print("\nCreating box plot: Revenue by Time of Day...")
plot2 = (ggplot(data, aes(x='TimeOfDay', y='TotalRevenue', fill='TimeOfDay')) +
         geom_boxplot() +
         xlab('Time of Day') +
         ylab('Total Revenue ($)') +
         ggtitle('Distribution of Revenue by Time of Day') +
         theme(figure_size=(10, 6))
        )
plot2.save('output/visualizations/2_boxplot_revenue_by_time.png', dpi=300)
print("Saved: output/visualizations/2_boxplot_revenue_by_time.png")

# 3. Box Plot - Revenue by Day of Week
print("\nCreating box plot: Revenue by Day of Week...")
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
data['DayOfWeek'] = pd.Categorical(data['DayOfWeek'], categories=day_order, ordered=True)

plot3 = (ggplot(data, aes(x='DayOfWeek', y='TotalRevenue', fill='DayOfWeek')) +
         geom_boxplot() +
         xlab('Day of Week') +
         ylab('Total Revenue ($)') +
         ggtitle('Distribution of Revenue by Day of Week') +
         theme(figure_size=(12, 6), axis_text_x=element_text(angle=45, hjust=1))
        )
plot3.save('output/visualizations/3_boxplot_revenue_by_day.png', dpi=300)
print("Saved: output/visualizations/3_boxplot_revenue_by_day.png")

# 4. Column Chart - Total Sales by Day of Week
print("\nCreating column chart: Total Sales by Day of Week...")
daily_sales = data.groupby('DayOfWeek')['TotalRevenue'].sum().reset_index()
daily_sales['DayOfWeek'] = pd.Categorical(daily_sales['DayOfWeek'], categories=day_order, ordered=True)
daily_sales = daily_sales.sort_values('DayOfWeek')

plot4 = (ggplot(daily_sales, aes(x='DayOfWeek', y='TotalRevenue', fill='DayOfWeek')) +
         geom_col() +
         geom_text(aes(label=daily_sales['TotalRevenue'].round(0)), nudge_y=daily_sales['TotalRevenue'].max() * 0.01) +
         xlab('Day of Week') +
         ylab('Total Revenue ($)') +
         labs(fill='Day of Week') +
         ggtitle('Total Sales Revenue by Day of Week') +
         theme(figure_size=(12, 6), axis_text_x=element_text(angle=45, hjust=1))
        )
plot4.save('output/visualizations/4_column_sales_by_day.png', dpi=300)
print("Saved: output/visualizations/4_column_sales_by_day.png")

# 5. Column Chart - Total Sales by Time of Day
print("\nCreating column chart: Total Sales by Time of Day...")
time_sales = data.groupby('TimeOfDay')['TotalRevenue'].sum().reset_index()
time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
time_sales['TimeOfDay'] = pd.Categorical(time_sales['TimeOfDay'], categories=time_order, ordered=True)
time_sales = time_sales.sort_values('TimeOfDay')

plot5 = (ggplot(time_sales, aes(x='TimeOfDay', y='TotalRevenue', fill='TimeOfDay')) +
         geom_col() +
         geom_text(aes(label=time_sales['TotalRevenue'].round(0)), nudge_y=time_sales['TotalRevenue'].max() * 0.01) +
         xlab('Time of Day') +
         ylab('Total Revenue ($)') +
         labs(fill='Time of Day') +
         ggtitle('Total Sales Revenue by Time of Day') +
         theme(figure_size=(10, 6))
        )
plot5.save('output/visualizations/5_column_sales_by_time.png', dpi=300)
print("Saved: output/visualizations/5_column_sales_by_time.png")

# 6. Line Chart - Sales Over Time
print("\nCreating line chart: Sales Over Time...")
monthly_sales = data.groupby(data['InvoiceDate'].dt.to_period('M'))['TotalRevenue'].sum().reset_index()
monthly_sales['InvoiceDate'] = monthly_sales['InvoiceDate'].astype(str)
monthly_sales = monthly_sales.sort_values('InvoiceDate')

plot6 = (ggplot(monthly_sales, aes(x='InvoiceDate', y='TotalRevenue', group=1)) +
         geom_line(color='blue', size=1) +
         geom_point(color='blue', size=2) +
         xlab('Month') +
         ylab('Total Revenue ($)') +
         ggtitle('Total Sales Revenue Over Time') +
         theme(figure_size=(12, 6), axis_text_x=element_text(angle=45, hjust=1))
        )
plot6.save('output/visualizations/6_line_sales_over_time.png', dpi=300)
print("Saved: output/visualizations/6_line_sales_over_time.png")

# 7. Scatter Plot - Quantity vs Unit Price
print("\nCreating scatter plot: Quantity vs Unit Price...")
# Sample data for better visualization (too many points)
data_sample = data.sample(min(10000, len(data)), random_state=42)

plot7 = (ggplot(data_sample, aes(x='UnitPrice', y='Quantity')) +
         geom_point(alpha=0.3, color='blue') +
         geom_smooth(method='lm', se=False, color='red') +
         xlab('Unit Price ($)') +
         ylab('Quantity') +
         ggtitle('Relationship Between Unit Price and Quantity') +
         theme(figure_size=(10, 6))
        )
plot7.save('output/visualizations/7_scatter_price_quantity.png', dpi=300)
print("Saved: output/visualizations/7_scatter_price_quantity.png")

# 8. Top 10 Countries by Revenue
print("\nCreating column chart: Top 10 Countries by Revenue...")
country_revenue = data.groupby('Country')['TotalRevenue'].sum().sort_values(ascending=False).head(10).reset_index()
# Sort for proper ordering in plot
country_revenue = country_revenue.sort_values('TotalRevenue', ascending=True)

plot8 = (ggplot(country_revenue, aes(x='Country', y='TotalRevenue', fill='Country')) +
         geom_col() +
         coord_flip() +
         xlab('Country') +
         ylab('Total Revenue ($)') +
         labs(fill='Country') +
         ggtitle('Top 10 Countries by Total Revenue') +
         theme(figure_size=(10, 6))
        )
plot8.save('output/visualizations/8_column_top_countries.png', dpi=300)
print("Saved: output/visualizations/8_column_top_countries.png")

# 9. Density Plot - Distribution of Unit Prices
print("\nCreating density plot: Distribution of Unit Prices...")
plot9 = (ggplot(data, aes(x='UnitPrice')) +
         geom_density(fill='blue', alpha=0.5) +
         xlab('Unit Price ($)') +
         ylab('Density') +
         ggtitle('Distribution of Unit Prices') +
         theme(figure_size=(10, 6))
        )
plot9.save('output/visualizations/9_density_unit_price.png', dpi=300)
print("Saved: output/visualizations/9_density_unit_price.png")

# 10. Violin Plot - Revenue Distribution by Country (Top 5)
print("\nCreating violin plot: Revenue Distribution by Top 5 Countries...")
top_5_countries = data.groupby('Country')['TotalRevenue'].sum().sort_values(ascending=False).head(5).index
data_top5 = data[data['Country'].isin(top_5_countries)]

plot10 = (ggplot(data_top5, aes(x='Country', y='TotalRevenue', fill='Country')) +
          geom_violin() +
          geom_boxplot(fill='white', width=0.1) +
          xlab('Country') +
          ylab('Total Revenue ($)') +
          labs(fill='Country') +
          ggtitle('Revenue Distribution by Top 5 Countries') +
          theme(figure_size=(12, 6), axis_text_x=element_text(angle=45, hjust=1))
         )
plot10.save('output/visualizations/10_violin_revenue_by_country.png', dpi=300)
print("Saved: output/visualizations/10_violin_revenue_by_country.png")

# 11. Top 20 Products by Revenue
print("\nCreating column chart: Top 20 Products by Revenue...")
product_revenue = data.groupby(['StockCode', 'Description_imputed'])['TotalRevenue'].sum().sort_values(ascending=False).head(20).reset_index()
product_revenue['Product'] = product_revenue['StockCode'] + ' - ' + product_revenue['Description_imputed'].str[:30]
# Sort for proper ordering in plot
product_revenue = product_revenue.sort_values('TotalRevenue', ascending=True)

plot11 = (ggplot(product_revenue, aes(x='Product', y='TotalRevenue', fill='TotalRevenue')) +
          geom_col() +
          coord_flip() +
          scale_fill_gradient(low='lightblue', high='darkblue') +
          xlab('Product') +
          ylab('Total Revenue ($)') +
          labs(fill='Revenue') +
          ggtitle('Top 20 Products by Total Revenue') +
          theme(figure_size=(12, 8))
         )
plot11.save('output/visualizations/11_column_top_products.png', dpi=300)
print("Saved: output/visualizations/11_column_top_products.png")

# 12. Heatmap - Sales by Day of Week and Time of Day
print("\nCreating heatmap: Sales by Day of Week and Time of Day...")
heatmap_data = data.groupby(['DayOfWeek', 'TimeOfDay'])['TotalRevenue'].sum().reset_index()
heatmap_data['DayOfWeek'] = pd.Categorical(heatmap_data['DayOfWeek'], categories=day_order, ordered=True)
heatmap_data['TimeOfDay'] = pd.Categorical(heatmap_data['TimeOfDay'], categories=time_order, ordered=True)

plot12 = (ggplot(heatmap_data, aes(x='DayOfWeek', y='TimeOfDay', fill='TotalRevenue')) +
          geom_tile() +
          geom_text(aes(label=heatmap_data['TotalRevenue'].round(0)), size=8) +
          scale_fill_gradient(low='deepskyblue', high='darksalmon') +
          xlab('Day of Week') +
          ylab('Time of Day') +
          labs(fill='Total Revenue ($)') +
          ggtitle('Heatmap of Sales Revenue by Day of Week and Time of Day') +
          theme(figure_size=(12, 6), axis_text_x=element_text(angle=45, hjust=1))
         )
plot12.save('output/visualizations/12_heatmap_day_time.png', dpi=300)
print("Saved: output/visualizations/12_heatmap_day_time.png")

print("\n=== All Visualizations Complete ===")
print(f"All visualizations saved to: output/visualizations/")

