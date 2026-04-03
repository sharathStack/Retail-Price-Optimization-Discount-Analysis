"""
config.py — Retail Price Optimization & Discount Analysis
"""

# ── Data ───────────────────────────────────────────────────────────────────────
N_TRANSACTIONS = 2_000
RANDOM_SEED    = 42
SEGMENTS       = ["Budget", "Mid-Market", "Premium"]
CATEGORIES     = ["Electronics", "Apparel", "Home & Kitchen", "Beauty", "Sports"]

# ── Elasticity ─────────────────────────────────────────────────────────────────
# Higher = more price sensitive (demand rises more with discounts)
ELASTICITY_BY_SEGMENT = {
    "Budget":     2.0,
    "Mid-Market": 1.3,
    "Premium":    0.7,
}

# ── Optimisation ───────────────────────────────────────────────────────────────
BASE_PRICE      = 100.0    # reference price for optimal discount curves
BASE_UNITS      = 20       # reference daily units at base price
DISCOUNT_RANGE  = (0, 50)  # allowed discount % range

# ── Output ─────────────────────────────────────────────────────────────────────
CHART_EDA       = "price_eda.png"
CHART_OPT_CURVE = "price_optimization_curve.png"
CHART_DPI       = 150
