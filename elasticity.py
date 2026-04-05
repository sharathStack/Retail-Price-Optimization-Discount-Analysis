"""
elasticity.py — Price elasticity estimation via log-log OLS regression

Price elasticity of demand (PED):
  log(units) = alpha + beta * log(price)
  beta = price elasticity (negative = normal good; more negative = more elastic)
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import config


def estimate_elasticity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate price elasticity per customer segment via log-log OLS.
    Returns a DataFrame with segment, elasticity, and interpretation.
    """
    results = []
    for seg in config.SEGMENTS:
        sub = df[df["segment"] == seg].copy()
        sub = sub[sub["units_sold"] > 0]

        log_price = np.log(sub["final_price"].clip(0.01)).values.reshape(-1, 1)
        log_units = np.log(sub["units_sold"].clip(1)).values

        reg = LinearRegression().fit(log_price, log_units)
        elasticity = reg.coef_[0]

        # Correlation between log(price) and log(units)
        corr = np.corrcoef(log_price.flatten(), log_units)[0, 1]

        results.append({
            "Segment":    seg,
            "Elasticity": round(elasticity, 3),
            "Correlation":round(corr, 3),
            "Interpretation": (
                "Highly elastic — discounts drive strong demand"
                if abs(elasticity) > 1.5 else
                "Moderately elastic — discounts moderately effective"
                if abs(elasticity) > 0.8 else
                "Inelastic — price changes have limited demand impact"
            ),
        })

    df_out = pd.DataFrame(results)
    print("\n── Price Elasticity by Segment ──────────────────────")
    print(df_out.to_string(index=False))
    return df_out
