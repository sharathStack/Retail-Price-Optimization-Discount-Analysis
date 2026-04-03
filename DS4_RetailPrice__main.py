"""
main.py — Retail Price Optimization entry point
"""

import config
from data_gen   import generate
from elasticity import estimate_elasticity
from optimizer  import find_optimal_discounts
from dashboard  import plot_eda, plot_optimization_curves


def main():
    print("=" * 55)
    print("  RETAIL PRICE OPTIMIZATION & DISCOUNT ANALYSIS")
    print("=" * 55)

    print("\n[1] Generating transaction data...")
    df = generate()

    print("\n[2] EDA visualisation...")
    plot_eda(df)

    print("\n[3] Estimating price elasticity per segment...")
    elasticity_df = estimate_elasticity(df)

    print("\n[4] Finding optimal discount rates...")
    opt_df = find_optimal_discounts(elasticity_df)

    print("\n[5] Plotting optimization curves...")
    plot_optimization_curves(elasticity_df, opt_df)

    print("\n  Done ✓")


if __name__ == "__main__":
    main()
