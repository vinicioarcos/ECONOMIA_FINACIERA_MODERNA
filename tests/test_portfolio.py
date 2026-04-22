"""Tests — Semana 5: Portafolios"""
import numpy as np
import pandas as pd
import pytest
from src.portfolio import portfolio_return, portfolio_risk, equal_weight_portfolio, portfolio_metrics


def test_portfolio_return_basic():
    weights = np.array([0.5, 0.5])
    mean_returns = pd.Series([0.10, 0.20])
    result = portfolio_return(weights, mean_returns)
    assert abs(result - 0.15) < 1e-6


def test_portfolio_risk_uncorrelated():
    """Con activos no correlacionados, la diversificación reduce el riesgo"""
    weights = np.array([0.5, 0.5])
    cov = np.array([[0.04, 0.0], [0.0, 0.04]])
    risk = portfolio_risk(weights, cov)
    assert abs(risk - 0.1414) < 0.001


def test_equal_weight():
    w = equal_weight_portfolio(4)
    assert len(w) == 4
    assert abs(sum(w) - 1.0) < 1e-9


def test_diversification_benefit():
    """El riesgo del portafolio < promedio de riesgos individuales cuando correlación < 1"""
    weights = np.array([0.5, 0.5])
    cov_corr = np.array([[0.04, 0.01], [0.01, 0.04]])
    portfolio_vol = portfolio_risk(weights, cov_corr)
    individual_avg = np.sqrt(0.04)
    assert portfolio_vol < individual_avg, "La diversificación debe reducir el riesgo"
