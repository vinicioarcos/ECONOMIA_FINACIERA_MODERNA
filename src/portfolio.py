"""portfolio.py — Construcción y análisis de portafolios"""
import numpy as np
import pandas as pd
from typing import Union


def portfolio_return(weights: np.ndarray, mean_returns: pd.Series) -> float:
    """Retorno esperado del portafolio"""
    return float(np.dot(weights, mean_returns))


def portfolio_risk(weights: np.ndarray, cov_matrix: pd.DataFrame) -> float:
    """Riesgo (volatilidad) del portafolio"""
    return float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))


def equal_weight_portfolio(n_assets: int) -> np.ndarray:
    """Portafolio equi-ponderado"""
    return np.array([1 / n_assets] * n_assets)


def portfolio_metrics(returns: pd.DataFrame, weights: np.ndarray = None) -> dict:
    """Calcula métricas completas de un portafolio"""
    if weights is None:
        weights = equal_weight_portfolio(len(returns.columns))

    mean_ret = returns.mean() * 252
    cov = returns.cov() * 252

    p_return = portfolio_return(weights, mean_ret)
    p_risk = portfolio_risk(weights, cov)
    sharpe = (p_return - 0.02) / p_risk if p_risk > 0 else 0

    return {
        "return": round(p_return, 4),
        "risk": round(p_risk, 4),
        "sharpe": round(sharpe, 4),
        "weights": dict(zip(returns.columns, weights.round(4)))
    }
