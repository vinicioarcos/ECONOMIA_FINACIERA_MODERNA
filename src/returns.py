"""returns.py — Cálculo de retornos financieros"""
import numpy as np
import pandas as pd


def simple_returns(prices: pd.Series) -> pd.Series:
    """Retorno simple: (P_t - P_{t-1}) / P_{t-1}"""
    return prices.pct_change().dropna()


def log_returns(prices: pd.Series) -> pd.Series:
    """Retorno logarítmico: ln(P_t / P_{t-1})"""
    return np.log(prices / prices.shift(1)).dropna()


def annualized_return(returns: pd.Series, trading_days: int = 252) -> float:
    """Retorno anualizado a partir de retornos diarios"""
    return (1 + returns.mean()) ** trading_days - 1


def cumulative_return(returns: pd.Series) -> pd.Series:
    """Retorno acumulado"""
    return (1 + returns).cumprod() - 1
