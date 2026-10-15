ETL PORTFOLIO PROJECT

# Project Overview

Organizations often collect data from multiple tools, such as CRMs, spreadsheets, exports and APIs.  Each source varies as to the format, naming conventions, and data quality.  Without proper care, this can lead to huge problems such as report conflicts across departments, KPIs becoming inaccurate and ultimately leadership unable to trust the information in dashboards or the insights they usually bring.

## The Goal

I'm going to solve this issue for a fictitious Retailer/E-Commerce Platform by building a repeatable, documented cleaning and integration workflow, and ETL pipeline (Extract, Transform, Load).  As is often the case in the real world, the company's data is scattered across multiple systems, is inconsistent, unreliable and impossible to properly analyze.

I build a complete data-cleaning and multi-source integration pipeline that extracts data from 3 different sources (CSV, Excel, API), cleans and standardizes each dataset and merges them into a single, analysis ready master table.
 

## The Data
 
In order to mimic reality as closely as possible, I picked datasets that were pulled from real world Brazilian E-Commerce company Olist, sourced from kaggle.

For the customer dataset:

* The Olist E-Commerce Customers (CSV) (source: GitHub "https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist")
    - it's one of the most widely used real world e-commerce datasets with customer IDs, locations, and purchase behavior

For the product dataset:

* The Olist Product dataset (Excel) (source: GitHub "https://github.com/rajtulluri/Olist-business-analysis")
    - it's part of the same ecosystem as the customer dataset but stored separately in Excel

For the Engagement dataset:

* FakeStoreAPI (JSON) (source: "https://fakestoreapi.com/")("https://github.com/nodewalker/fake-store-api")
    - provides real API endpoints with responses - perfect for extraction, normalization and integration

From here on, I'll be documenting as though the above situation were true.

# Executive ETL Overview

Goal: 
Extract customer (CSV), product (Excel), and engagement (API) data -> clean and standardize -> integrate into a single analytics ready dataset -> document the process.

Outcome:
A trustworthy master dataset that solves the problem of inconsistent, fragmented data


# E - Extract

Objective:
Pull raw data from 3 different sources and store them in a structured directory

Deliverables:
* /extract/extract_customers.py
* /extract/extract_products.py
* /extract/extract_api.py
* /data/raw directory


# T - Transform

Objective:
Clean, standardize, validate, and prepare each dataset for integration

## Cleaning Tasks

* Column Standardization
  - lowercase
  - replace spaces with underscores
  - remove special characters
* Data Type Correction
  - convert dates
  - ensure numeric fields are numeric
  - convert IDs to strings
* Missing Values
  - impute or drop based on business logic
  - document decisions
* Duplicate Removal
  - ID duplicates using customer_id or product_id
  - remove or consolidate
* Outlier Detection
  - use IQR or z score
  - document findings
* Data Validation
  - check referential integrity
  - validate unique keys
  - confirm expected ranges

Deliverables:
* /transform/clean_customers.py
* /transform/clean_products.py
* /transform/clean_engagement.py
* /data/clean directory
*profiling.md (data quality documentation)


# L - Load

Objective:
Load cleaned datasets into a database, join them, and produce master dataset

Deliverables:
* /load/load_to_sql.py
* /load/join_tables.sql
* /data/final/master_dataset.csv
* report.md (business insights)
_______________________


# Skill Demonstration

* Python/Pandas
* SQLite
* Data cleaning
* Multisource data integration
* ETL pipeline design
* Documentation
Business Communication
Problem Solving
