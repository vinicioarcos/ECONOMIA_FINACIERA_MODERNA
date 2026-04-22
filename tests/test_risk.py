"""Tests — Semana 4 & 12: Riesgo y VaR"""
import numpy as np
import pandas as pd
import pytest
from src.risk import volatility, var_historical, sharpe_ratio, rolling_volatility


def test_volatility_positive():
    returns = pd.Series(np.random.normal(0.001, 0.02, 252))
    vol = volatility(returns)
    assert vol > 0


def test_var_historical_negative():
    """El VaR al 95% debe ser negativo (pérdida)"""
    returns = pd.Series(np.random.normal(0, 0.02, 1000))
    var = var_historical(returns, confidence=0.95)
    assert var < 0, "VaR debe representar una pérdida potencial"


def test_sharpe_positive_for_high_returns():
    high_returns = pd.Series([0.005] * 252)
    sharpe = sharpe_ratio(high_returns, risk_free=0.02)
    assert sharpe > 0


def test_rolling_vol_shape():
    returns = pd.Series(np.random.normal(0, 0.01, 100))
    rv = rolling_volatility(returns, window=21)
    assert len(rv) == len(returns)
