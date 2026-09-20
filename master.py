# %%
!pip install pandas
import pandas as pd
import numpy as np

# %%
# import customers
def extract_customers(path="olist_customers_dataset.csv"):
    customers = pd.read_csv(path)
    print(f"Customers extracted: {customers.shape}")
    return customers

# %%
if __name__ == "__main__":
    extract_customers()

# %%
# import products
def extract_products(path="olist_products_dataset.xlsx"):
    products = pd.read_excel(path)
    print(f"Products extracted: {products.shape}")
    return products

# %%
!pip install openpyxl

# %%
if __name__ == "__main__":
    extract_products()

# %%
!pip install requests
import requests

# %%
# import engagement
def extract_engagement(url="https://fakestoreapi.com/carts"):
  try:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/json" not in content_type.lower():
      raise ValueError(f"Unexpected content-type: {content_type}")

    data = response.json()
  except (requests.RequestException, ValueError, TypeError) as exc:
    print(f"API unavailable ({exc}); using fallback sample data instead.")
    data = [
      {"id": 1, "userId": 1, "date": "2024-01-15", "products": [{"productId": 1, "quantity": 1}]},
      {"id": 2, "userId": 2, "date": "2024-01-16", "products": [{"productId": 2, "quantity": 2}]},
      {"id": 3, "userId": 3, "date": "2024-01-17", "products": [{"productId": 3, "quantity": 1}]}
    ]

  engagement = pd.DataFrame(data)
  print(f"Engagement extracted: {engagement.shape}")
  return engagement

# %%
if __name__ == "__main__":
  extract_engagement()

# %%
# clean customers

def clean_customers(df):
  df.columns = df.columns.str.lower().str.replace(" ", "_")

  df["customer_id"] = df["customer_id"].astype(str)
  df["customer_unique_id"] = df["customer_unique_id"].astype(str)

  df.fillna("unknown", inplace=True)

  df.drop_duplicates(subset="customer_id", inplace=True)

  print(f"Customers cleaned.")
  return df


# %%
import os

if __name__ == "__main__":
    raw = extract_customers()  # Use the defined function to extract customers without an explicit path
    clean = clean_customers(raw)

    # Ensure the output directory exists
    output_dir = "data/clean"
    os.makedirs(output_dir, exist_ok=True)

    clean.to_csv(os.path.join(output_dir, "customers_clean.csv"), index=False)

# %%
def clean_products(df):
  df.columns = df.columns.str.lower().str.replace(" ", "_")

  df["product_id"] = df["product_id"].astype(str)

  numeric_cols = df.select_dtypes(include=["float64","int64"]).columns
  df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

  df.drop_duplicates(subset="product_id", inplace=True)

  print(f"Products cleaned.")
  return df

# %%
import os

if __name__ == "__main__":
    # The file 'data/raw/products.xlsx' does not exist.
    # Instead, use the extract_products function which correctly reads 'olist_products_dataset.xlsx'.
    raw = extract_products()
    clean = clean_products(raw)

    # Ensure the output directory exists
    output_dir = "data/clean"
    os.makedirs(output_dir, exist_ok=True)

    clean.to_csv(os.path.join(output_dir, "products_clean.csv"), index=False)

# %%
# clean engagement

def clean_engagement(df):
  df.columns = df.columns.str.lower().str.replace(" ", "_")

  if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

  if 'products' in df.columns:
    df['parsed_products'] = df['products'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    df['product_id'] = df['parsed_products'].apply(
        lambda x: x[0]['productId'] if isinstance(x, list) and len(x) > 0 and 'productId' in x[0] else None
    )
    df.drop(columns=['products', 'parsed_products'], inplace=True, errors='ignore')

  df.fillna("unknown", inplace=True)

  print(f"Engagement cleaned.")
  return df


# %%
import os

if __name__ == "__main__":
    # The file 'data/raw/engagement.json' does not exist.
    # Use the extract_engagement function which fetches data from the API.
    raw = extract_engagement()
    clean = clean_engagement(raw)

    # Ensure the output directory exists
    output_dir = "data/clean"
    os.makedirs(output_dir, exist_ok=True)

    clean.to_csv(os.path.join(output_dir, "engagement_clean.csv"), index=False)

# %%
# load scripts (SQL)

import sqlite3

# %%
import os

def load_to_sql():
  # Ensure the directory for the database exists
  db_dir = "data/final"
  os.makedirs(db_dir, exist_ok=True)
  conn = sqlite3.connect(os.path.join(db_dir, "master.db"))

  customers = pd.read_csv("data/clean/customers_clean.csv")
  products = pd.read_csv("data/clean/products_clean.csv")
  engagement = pd.read_csv("data/clean/engagement_clean.csv")

  customers.to_sql("customers", conn, if_exists="replace", index=False)
  products.to_sql("products", conn, if_exists="replace", index=False)
  engagement.to_sql("engagement", conn, if_exists="replace", index=False)

  print("Data loaded to SQL.")
  return conn

# %%
if __name__ == "__main__":
    load_to_sql()

# %%
query = """
SELECT
  e.id AS engagement_id,
  e.userid AS customer_id,
  p.product_id,
  p.product_category_name,
  c.customer_city,
  c.customer_state
FROM engagement e
LEFT JOIN customers c ON e.userid = c.customer_id
LEFT JOIN products p ON e.product_id = p.product_id
"""

# %%
import os
import sqlite3
import pandas as pd

# export master dataset

def export_master():
  os.makedirs("data/final", exist_ok=True)
  db_path = os.path.join("data", "final", "master.db")

  if not os.path.exists(db_path):
    print("Database not found; creating it first.")
    load_to_sql()

  conn = sqlite3.connect(db_path)
  master = pd.read_sql_query(query, conn)
  master.to_csv("data/final/master_dataset.csv", index=False)
  conn.close()
  print("Master dataset exported.")

# %%
if __name__ == "__main__":
    export_master()

# %%



