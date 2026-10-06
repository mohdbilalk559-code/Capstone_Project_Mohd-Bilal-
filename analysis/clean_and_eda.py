import pandas as pd
import json
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
NARRATOR_DIR = BASE_DIR / "narrator"

orders_file = DATA_DIR / "orders.csv"
products_file = DATA_DIR / "Product.CSV"
customers_file = DATA_DIR / "CUSTOMER.CSV"

# --------------------------------------------------
# 2. Load CSV files
# --------------------------------------------------

orders = pd.read_csv(orders_file)
products = pd.read_csv(products_file)
customers = pd.read_csv(customers_file)

print("Orders:", orders.shape)
print("Products:", products.shape)
print("Customers:", customers.shape)

# --------------------------------------------------
# 3. Clean column names
# --------------------------------------------------

orders.columns = orders.columns.str.strip()
products.columns = products.columns.str.strip()
customers.columns = customers.columns.str.strip()

# --------------------------------------------------
# 4. Calculate RAW revenue before removing duplicates
# --------------------------------------------------

raw_order_count = len(orders)

raw_revenue_df = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

raw_revenue_df["discount_pct"] = pd.to_numeric(
    raw_revenue_df["discount_pct"],
    errors="coerce"
).fillna(0)

raw_revenue_df["quantity"] = pd.to_numeric(
    raw_revenue_df["quantity"],
    errors="coerce"
).fillna(0)

raw_revenue_df["raw_revenue"] = (
    raw_revenue_df["quantity"]
    * raw_revenue_df["price"]
    * (1 - raw_revenue_df["discount_pct"] / 100)
)

raw_total_revenue = round(
    raw_revenue_df["raw_revenue"].sum(),
    2
)

# --------------------------------------------------
#  Remove duplicate orders
# --------------------------------------------------

orders = orders.drop_duplicates(subset="order_id")

clean_order_count = len(orders)

duplicate_count = raw_order_count - clean_order_count
# --------------------------------------------------
# 5. Standardize payment method
# --------------------------------------------------

orders["payment_method"] = (
    orders["payment_method"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# --------------------------------------------------
# 6. Handle missing discount
# --------------------------------------------------

orders["discount_pct"] = pd.to_numeric(
    orders["discount_pct"],
    errors="coerce"
)

orders["discount_pct"] = orders["discount_pct"].fillna(0)

# --------------------------------------------------
# 7. Convert dates and numeric columns
# --------------------------------------------------

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders["quantity"] = pd.to_numeric(
    orders["quantity"],
    errors="coerce"
).fillna(0)

orders["rating"] = pd.to_numeric(
    orders["rating"],
    errors="coerce"
)

# --------------------------------------------------
# 8. Join orders with products
# --------------------------------------------------

df = orders.merge(
    products[["product_id", "product_name", "category", "price"]],
    on="product_id",
    how="left"
)

# --------------------------------------------------
# 9. Join customer information
# --------------------------------------------------

df = df.merge(
    customers[
        [
            "customer_id",
            "name",
            "city",
            "city_tier",
            "signup_date",
            "acquisition_source"
        ]
    ],
    on="customer_id",
    how="left"
)

# --------------------------------------------------
# 10. Calculate revenue
# --------------------------------------------------

df["gross_revenue"] = df["quantity"] * df["price"]

df["revenue"] = (
    df["quantity"]
    * df["price"]
    * (1 - df["discount_pct"] / 100)
)

# --------------------------------------------------
# 11. Return flag
# --------------------------------------------------

df["returned"] = pd.to_numeric(
    df["returned"],
    errors="coerce"
).fillna(0)

df["is_returned"] = df["returned"].astype(int)

# --------------------------------------------------
# 12. Date fields
# --------------------------------------------------

df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

# --------------------------------------------------
# 13. Key metrics
# --------------------------------------------------

cleaned_total_revenue = round(
    df["revenue"].sum(), 2
)


duplicate_reconciliation_delta = round(
    raw_total_revenue - cleaned_total_revenue,
    2
)

# --------------------------------------------------
# 14. Return rate by payment method
# --------------------------------------------------

return_rate = (
    df.groupby("payment_method")["is_returned"]
    .mean()
    .mul(100)
    .round(1)
    .to_dict()
)

# --------------------------------------------------
# 15. Highest-risk segment
# --------------------------------------------------

risk_segment = (
    df.groupby(["payment_method", "city_tier"])
    .agg(
        total_orders=("order_id", "count"),
        returned_orders=("is_returned", "sum")
    )
    .reset_index()
)

risk_segment["return_rate_pct"] = (
    risk_segment["returned_orders"]
    / risk_segment["total_orders"]
    * 100
)

highest_risk = risk_segment.loc[
    risk_segment["return_rate_pct"].idxmax()
]

# --------------------------------------------------
# 16. Monthly revenue
# --------------------------------------------------

monthly_revenue = (
    df.groupby("year_month")["revenue"]
    .sum()
    .round(2)
)

true_peak_month = monthly_revenue.idxmax()
true_peak_revenue = round(
    monthly_revenue.max(), 2
)

# --------------------------------------------------
# 17. Save findings.json
# --------------------------------------------------

findings = {
    "cleaned_total_revenue_inr": cleaned_total_revenue,
    "raw_total_revenue_inr": raw_total_revenue,
    "duplicate_reconciliation_delta_inr":
        duplicate_reconciliation_delta,

    "duplicate_orders_removed":
        duplicate_count,

    "return_rate_by_payment": return_rate,

    "highest_risk_segment": {
        "payment_method":
            highest_risk["payment_method"],
        "city_tier":
            int(highest_risk["city_tier"]),
        "return_rate_pct":
            round(float(highest_risk["return_rate_pct"]), 1)
    },

    "true_peak_month": {
        "month": true_peak_month,
        "revenue_inr": true_peak_revenue
    }
}

NARRATOR_DIR.mkdir(exist_ok=True)

with open(
    NARRATOR_DIR / "findings.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        findings,
        f,
        indent=2,
        ensure_ascii=False
    )

# --------------------------------------------------
# 18. Save cleaned dataset
# --------------------------------------------------

df.to_csv(
    DATA_DIR / "cleaned_orders.csv",
    index=False
)

print("\nCleaning and EDA completed successfully.")
print("Duplicate orders removed:", duplicate_count)
print("Cleaned revenue:", cleaned_total_revenue)
print("Peak month:", true_peak_month)
print("Findings saved to narrator/findings.json")
