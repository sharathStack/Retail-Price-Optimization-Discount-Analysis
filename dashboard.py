"""
dashboard.py — EDA charts + revenue optimisation curves
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import config

COLORS = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"]
SEG_COLORS = {"Budget": "#3498db", "Mid-Market": "#2ecc71", "Premium": "#e74c3c"}


def plot_eda(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Retail Price Optimization — EDA", fontsize=14, fontweight="bold")

    # Revenue by segment
    seg_rev = df.groupby("segment")["revenue"].sum()
    axes[0, 0].bar(seg_rev.index, seg_rev.values / 1e6,
                   color=[SEG_COLORS[s] for s in seg_rev.index], alpha=0.85)
    axes[0, 0].set_title("Total Revenue by Segment ($M)")
    axes[0, 0].set_ylabel("Revenue ($M)")

    # Discount vs avg units sold per segment
    for seg, col in SEG_COLORS.items():
        sub = df[df["segment"] == seg]
        avg = sub.groupby("discount_pct")["units_sold"].mean()
        axes[0, 1].plot(avg.index, avg.values, label=seg, color=col,
                        marker="o", markersize=4, linewidth=1.8)
    axes[0, 1].set_title("Avg Units Sold vs Discount %")
    axes[0, 1].set_xlabel("Discount (%)")
    axes[0, 1].set_ylabel("Avg Units Sold")
    axes[0, 1].legend()

    # Avg revenue by discount bucket
    rev_by_disc = df.groupby("discount_bucket", observed=True)["revenue"].mean()
    axes[1, 0].bar(rev_by_disc.index, rev_by_disc.values,
                   color="#9b59b6", alpha=0.85)
    axes[1, 0].set_title("Avg Revenue per Transaction by Discount Bucket")
    axes[1, 0].set_ylabel("Avg Revenue ($)")
    axes[1, 0].tick_params(axis="x", rotation=15)

    # Revenue heatmap: segment × category
    pivot = df.pivot_table(values="revenue", index="segment",
                           columns="category", aggfunc="sum")
    sns.heatmap(pivot / 1e3, ax=axes[1, 1], cmap="YlGnBu",
                annot=True, fmt=".0f")
    axes[1, 1].set_title("Revenue Heatmap ($K): Segment × Category")
    axes[1, 1].tick_params(axis="x", rotation=20)

    plt.tight_layout()
    plt.savefig(config.CHART_EDA, dpi=config.CHART_DPI, bbox_inches="tight")
    plt.close()
    print(f"EDA saved → {config.CHART_EDA}")


def plot_optimization_curves(elasticity_df: pd.DataFrame,
                              opt_df: pd.DataFrame) -> None:
    disc_range = np.linspace(0, 50, 300)
    fig, ax    = plt.subplots(figsize=(10, 6))

    for _, row in elasticity_df.iterrows():
        seg   = row["Segment"]
        elast = abs(row["Elasticity"])
        col   = SEG_COLORS[seg]
        revs  = [
            config.BASE_PRICE * (1 - d/100)
            * config.BASE_UNITS * (1 + elast * d/100)
            for d in disc_range
        ]
        ax.plot(disc_range, revs, label=seg, color=col, linewidth=2.2)

        # Vertical line at optimal discount
        opt_row = opt_df[opt_df["Segment"] == seg]
        if not opt_row.empty:
            od = opt_row["Optimal Discount (%)"].values[0]
            ax.axvline(od, color=col, linestyle="--", alpha=0.65,
                       label=f"{seg} optimal: {od}%")

    ax.set_title("Revenue vs Discount % — Optimal Point by Segment",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Discount (%)", fontsize=11)
    ax.set_ylabel("Expected Revenue ($)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(config.CHART_OPT_CURVE, dpi=config.CHART_DPI, bbox_inches="tight")
    plt.close()
    print(f"Optimization curve saved → {config.CHART_OPT_CURVE}")
