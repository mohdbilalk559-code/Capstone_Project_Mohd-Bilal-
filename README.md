# Mamaearth Returns & Growth Intelligence Pipeline

## Project Overview

This is a Data Analytics Capstone Project developed as part of the Data Analytics with AI & Generative AI program.

The project analyzes Mamaearth's e-commerce order data to understand revenue performance, product returns, payment-method risks, duplicate orders, and business growth patterns.

## Objectives

- Analyze order and customer data
- Clean and prepare raw data for analysis
- Identify duplicate orders and reconcile revenue
- Calculate return rates by payment method
- Identify high-risk customer segments
- Analyze monthly revenue trends
- Generate business insights using AI-assisted narrative generation

## Dataset

The project uses three main datasets:

- `Data/CUSTOMER.CSV` - Customer information
- `Data/Product.CSV` - Product information
- `Data/orders.csv` - Order transactions

## Project Structure

```text
Capstone_Project_Mohd-Bilal/
│
├── Data/
│   ├── CUSTOMER.CSV
│   ├── Product.CSV
│   └── orders.csv
│
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
│
├── narrator/
│   ├── findings.json
│   ├── generate_narrative.py
│   └── sample_output.txt
│
├── sql/
│   ├── reports.sql
│   ├── schema.sql
│   └── seed_data.sql
│
├── visualizations/
│   ├── monthly_revenue_trend.png
│   └── return_rate_by_payment.png
│
└── README.md 
