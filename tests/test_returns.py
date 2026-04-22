"""Tests — Semana 2: Retornos financieros"""
import numpy as np
import pandas as pd
import pytest
from src.returns import simple_returns, log_returns, annualized_return, cumulative_return


def test_simple_returns_basic():
    prices = pd.Series([100.0, 110.0, 121.0])
    returns = simple_returns(prices)
    assert len(returns) == 2
    assert abs(returns.iloc[0] - 0.10) < 1e-6, "Retorno simple incorrecto"


def test_log_returns_basic():
    prices = pd.Series([100.0, 110.0])
    r = log_returns(prices)
    expected = np.log(110 / 100)
    assert abs(r.iloc[0] - expected) < 1e-6


def test_simple_vs_log_returns():
    """Los retornos logarítmicos siempre son menores que los simples (para r > 0)"""
    prices = pd.Series([100.0, 120.0])
    r_simple = simple_returns(prices).iloc[0]
    r_log = log_returns(prices).iloc[0]
    assert r_log < r_simple


def test_annualized_return():
    daily_ret = pd.Series([0.001] * 252)
    ann = annualized_return(daily_ret)
    assert ann > 0


def test_cumulative_return_shape():
    returns = pd.Series([0.01, -0.01, 0.02])
    cum = cumulative_return(returns)
    assert len(cum) == len(returns)
