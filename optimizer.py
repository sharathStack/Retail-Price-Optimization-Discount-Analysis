"""
optimizer.py — Find revenue-maximising discount rate per segment

Uses scipy.optimize.minimize_scalar (bounded Brent's method) to find the
discount % that maximises expected revenue: R(d) = P(d) * Q(d)
  P(d) = base_price * (1 - d/100)          final price after discount
  Q(d) = base_units * (1 + |elasticity| * d/100)   demand response
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
import config


def expected_revenue(discount_pct: float, elasticity_abs: float,
                     base_price: float = None,
                     base_units: float = None) -> float:
    """Return NEGATIVE expected revenue (for minimisation)."""
    p = (base_price or config.BASE_PRICE) * (1 - discount_pct / 100)
    q = (base_units or config.BASE_UNITS) * (1 + elasticity_abs * discount_pct / 100)
    return -(p * q)


def find_optimal_discounts(elasticity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Find the revenue-maximising discount for each segment.
    """
    rows = []
    for _, row in elasticity_df.iterrows():
        seg      = row["Segment"]
        elast    = abs(row["Elasticity"])

        res = minimize_scalar(
            lambda d: expected_revenue(d, elast),
            bounds=config.DISCOUNT_RANGE,
            method="bounded",
        )
        opt_disc = round(res.x, 1)
        opt_rev  = round(-res.fun, 2)

        rows.append({
            "Segment":                  seg,
            "Optimal Discount (%)":     opt_disc,
            "Expected Revenue ($)":     opt_rev,
            "|Elasticity|":             round(elast, 3),
        })

    df_out = pd.DataFrame(rows)
    print("\n── Optimal Discount per Segment ─────────────────────")
    print(df_out.to_string(index=False))
    return df_out
