"""
data_gen.py — Synthetic retail transaction dataset with realistic price elasticity

Each segment responds differently to discounts:
  Budget     → high elasticity (demand jumps with discounts)
  Mid-Market → moderate elasticity
  Premium    → low elasticity (demand barely changes with discounts)
"""

import numpy as np
import pandas as pd
import config


def generate() -> pd.DataFrame:
    np.random.seed(config.RANDOM_SEED)
    n = config.N_TRANSACTIONS

    data = {
        "transaction_id": range(1, n + 1),
        "segment":        np.random.choice(config.SEGMENTS, n, p=[0.40, 0.40, 0.20]),
        "category":       np.random.choice(config.CATEGORIES, n),
        "base_price":     np.round(np.random.uniform(10, 500, n), 2),
        "discount_pct":   np.random.choice(range(0, 51, 5), n),
        "date":           pd.date_range("2023-01-01", periods=n, freq="3h")[:n],
    }

    df = pd.DataFrame(data)
    df["final_price"] = df["base_price"] * (1 - df["discount_pct"] / 100)

    # Units sold: base + elasticity effect + noise
    base_units = np.random.poisson(lam=20, size=n).astype(float)
    elasticity = df["segment"].map(config.ELASTICITY_BY_SEGMENT)
    df["units_sold"] = (
        base_units + df["discount_pct"] * elasticity + np.random.normal(0, 3, n)
    ).clip(1).round().astype(int)

    df["revenue"] = df["final_price"] * df["units_sold"]
    df["cost"]    = df["final_price"] * np.random.uniform(0.45, 0.65, n)
    df["profit"]  = df["revenue"] - df["cost"] * df["units_sold"]

    # Discount bucket labels
    df["discount_bucket"] = pd.cut(
        df["discount_pct"],
        bins=[-1, 5, 15, 25, 35, 50],
        labels=["0–5%", "6–15%", "16–25%", "26–35%", "36–50%"],
    )

    print(f"Generated {len(df):,} transactions")
    print(f"Revenue range: ${df['revenue'].min():.0f} – ${df['revenue'].max():.0f}")
    return df
