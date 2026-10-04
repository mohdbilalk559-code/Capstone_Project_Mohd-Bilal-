import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)

orders_file = DATA_DIR / "orders.csv"
products_file = DATA_DIR / "Product.CSV"

# --------------------------------------------------
# 2. Load data
# --------------------------------------------------

orders = pd.read_csv(orders_file)
products = pd.read_csv(products_file)

# --------------------------------------------------
# 3. Clean column names
# --------------------------------------------------

orders.columns = orders.columns.str.strip().str.lower()
products.columns = products.columns.str.strip().str.lower()

# --------------------------------------------------
# 4. Standardize payment method
# --------------------------------------------------

orders["payment_method"] = (
    orders["payment_method"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# --------------------------------------------------
# 5. Remove duplicate orders
# --------------------------------------------------

orders = orders.drop_duplicates(subset=["order_id"], keep="first")

# --------------------------------------------------
# 6. Convert data types
# --------------------------------------------------

orders["order_date"] = pd.to_datetime(orders["order_date"])

orders["quantity"] = pd.to_numeric(
    orders["quantity"], errors="coerce"
).fillna(0)

orders["discount_pct"] = pd.to_numeric(
    orders["discount_pct"], errors="coerce"
).fillna(0)

# --------------------------------------------------
# 7. Merge product price
# --------------------------------------------------

orders = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

# --------------------------------------------------
# 8. Calculate revenue
# --------------------------------------------------

orders["revenue"] = (
    orders["quantity"]
    * orders["price"]
    * (1 - orders["discount_pct"] / 100)
)

# --------------------------------------------------
# 9. Monthly Revenue Trend
# --------------------------------------------------

orders["year_month"] = orders["order_date"].dt.to_period("M").astype(str)

monthly_revenue = (
    orders.groupby("year_month")["revenue"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_revenue["year_month"],
    monthly_revenue["revenue"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Year Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Add revenue labels
for x, y in zip(
    monthly_revenue["year_month"],
    monthly_revenue["revenue"]
):
    plt.annotate(
        f"₹{y:,.2f}",
        (x, y),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# 10. Return Rate by Payment Method
# --------------------------------------------------

return_rate = (
    orders.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .reset_index()
)

plt.figure(figsize=(8, 5))

plt.bar(
    return_rate["payment_method"],
    return_rate["returned"]
)

plt.title("Return Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")

# Add percentage labels
for i, value in enumerate(return_rate["returned"]):
    plt.text(
        i,
        value + 1,
        f"{value:.1f}%",
        ha="center"
    )

plt.ylim(0, max(return_rate["returned"]) + 10)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Visualizations created successfully!")
print("Saved:")
print(OUTPUT_DIR / "monthly_revenue_trend.png")
print(OUTPUT_DIR / "return_rate_by_payment.png")
