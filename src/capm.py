"""capm.py — Capital Asset Pricing Model"""
import numpy as np
import pandas as pd
import statsmodels.api as sm


def estimate_beta(asset_returns: pd.Series, market_returns: pd.Series) -> dict:
    """
    Estima beta de un activo usando regresión OLS.
    beta > 1: más volátil que el mercado
    beta < 1: menos volátil que el mercado
    """
    X = sm.add_constant(market_returns.values)
    model = sm.OLS(asset_returns.values, X).fit()

    return {
        "alpha": round(model.params[0], 6),
        "beta": round(model.params[1], 4),
        "r_squared": round(model.rsquared, 4),
        "p_value_beta": round(model.pvalues[1], 4)
    }


def capm_expected_return(beta: float, risk_free: float = 0.02, market_premium: float = 0.06) -> float:
    """E(R) = Rf + beta * (E(Rm) - Rf)"""
    return risk_free + beta * market_premium


def security_market_line(betas: np.ndarray, risk_free: float = 0.02, market_premium: float = 0.06) -> np.ndarray:
    """Línea del Mercado de Valores (SML)"""
    return risk_free + betas * market_premium
