import json
from pathlib import Path

# File paths
BASE_DIR = Path("narrator")

FINDINGS_FILE = BASE_DIR / "findings.json"
OUTPUT_FILE = BASE_DIR / "sample_output.txt"

# Load findings
with open(FINDINGS_FILE, "r", encoding="utf-8") as f:
    findings = json.load(f)

# Extract values
cleaned_revenue = findings["cleaned_total_revenue_inr"]
raw_revenue = findings["raw_total_revenue_inr"]
duplicate_delta = findings["duplicate_reconciliation_delta_inr"]

return_rates = findings["return_rate_by_payment"]
risk = findings["highest_risk_segment"]
peak = findings["true_peak_month"]
outlier = findings["outlier_inflated_month"]

# Generate business narrative
narrative = f"""
Mamaearth Returns & Growth Intelligence – Business Narrative

1. Revenue Overview
The cleaned total revenue is ₹{cleaned_revenue:,.1f}, compared with
raw revenue of ₹{raw_revenue:,.1f}. The difference of ₹{duplicate_delta:,.1f}
was identified during duplicate-order reconciliation.

2. Return Risk by Payment Method
COD has the highest return rate at {return_rates["COD"]}%.
CARD has a return rate of {return_rates["CARD"]}%, while UPI has a
return rate of {return_rates["UPI"]}%.

3. Highest-Risk Customer Segment
The highest-risk segment is customers using {risk["payment_method"]}
in City Tier {risk["city_tier"]}, with a return rate of
{risk["return_rate_pct"]}%.

4. Revenue Peak
The true peak revenue month was {peak["month"]}, with revenue of
₹{peak["revenue_inr"]:,.1f}.

5. Outlier Correction
January 2026 appeared to generate ₹{outlier["apparent_revenue_inr"]:,.1f}
in revenue. After correcting the identified outlier/duplicate effect,
the corrected revenue was ₹{outlier["corrected_revenue_inr"]:,.1f}.

6. Business Recommendation
The business should focus on reducing COD-related returns, particularly
within Tier 2 cities. Duplicate-order controls and regular data-quality
checks should also be maintained to ensure accurate revenue reporting.
"""

# Save narrative
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(narrative.strip())

print("Narrative generated successfully.")
print(f"Output saved to: {OUTPUT_FILE}")
