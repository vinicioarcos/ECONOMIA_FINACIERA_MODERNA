"""
Econolab Financial Economics
Dataset Generator — Datos simulados reproducibles para el curso
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_stock_prices(n_days=252, n_assets=4, asset_names=None, seed=42):
    np.random.seed(seed)
    if asset_names is None:
        asset_names = [f"Asset_{i+1}" for i in range(n_assets)]
    params = [
        (0.0008, 0.012),
        (0.0012, 0.020),
        (0.0005, 0.025),
        (0.0010, 0.015),
    ]
    dates = pd.bdate_range("2022-01-03", periods=n_days)
    data = {}
    for i, name in enumerate(asset_names[:n_assets]):
        mu, sigma = params[i % len(params)]
        price = 100.0
        prices = [price]
        for _ in range(n_days - 1):
            shock = np.random.normal(mu, sigma)
            price = price * np.exp(shock)
            prices.append(round(price, 4))
        data[name] = prices
    return pd.DataFrame(data, index=dates)


def generate_interest_rates(n_days=252, seed=42):
    np.random.seed(seed + 1)
    dates = pd.bdate_range("2022-01-03", periods=n_days)
    kappa, theta, sigma = 0.1, 0.05, 0.003
    rate = 0.04
    rates = [rate]
    for _ in range(n_days - 1):
        dr = kappa * (theta - rate) + sigma * np.random.normal()
        rate = max(0.001, rate + dr)
        rates.append(round(rate, 6))
    return pd.DataFrame({
        "nominal_rate": rates,
        "real_rate": [r - 0.02 for r in rates],
        "spread": np.random.uniform(0.01, 0.03, n_days)
    }, index=dates)


def generate_macro_indicators(n_quarters=20, seed=42):
    np.random.seed(seed + 2)
    dates = pd.period_range("2018Q1", periods=n_quarters, freq="Q")
    gdp_growth = np.random.normal(0.025, 0.01, n_quarters)
    inflation = np.random.normal(0.03, 0.008, n_quarters)
    unemployment = 0.05 + np.cumsum(np.random.normal(0, 0.002, n_quarters))
    return pd.DataFrame({
        "gdp_growth": gdp_growth.round(4),
        "inflation": inflation.round(4),
        "unemployment": np.clip(unemployment, 0.02, 0.15).round(4)
    }, index=dates.astype(str))


def generate_bond_data(n_bonds=5, seed=42):
    np.random.seed(seed + 3)
    bonds = []
    for i in range(n_bonds):
        face_value = 1000
        coupon_rate = round(np.random.uniform(0.03, 0.08), 3)
        maturity = np.random.choice([1, 2, 3, 5, 7, 10])
        ytm = round(np.random.uniform(0.02, 0.09), 3)
        price = sum([face_value * coupon_rate / (1 + ytm) ** t for t in range(1, maturity + 1)]) + face_value / (1 + ytm) ** maturity
        bonds.append({
            "bond_id": f"BOND_{i+1:02d}", "face_value": face_value,
            "coupon_rate": coupon_rate, "maturity_years": maturity,
            "ytm": ytm, "price": round(price, 2), "duration": round(maturity * 0.85, 2)
        })
    return pd.DataFrame(bonds)


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "raw"
    output_dir.mkdir(exist_ok=True)
    asset_names = ["TECH_A", "BANK_B", "ENERGY_C", "MARKET_IDX"]
    prices = generate_stock_prices(asset_names=asset_names)
    prices.to_csv(output_dir / "stocks.csv")
    generate_interest_rates().to_csv(output_dir / "interest_rates.csv")
    generate_macro_indicators().to_csv(output_dir / "macro_indicators.csv")
    generate_bond_data().to_csv(output_dir / "bonds.csv", index=False)
    print("Datasets generados en data/raw/")
