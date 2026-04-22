"""Tests — Semana 7: CAPM"""
import numpy as np
import pandas as pd
import pytest
from src.capm import estimate_beta, capm_expected_return, security_market_line


def test_beta_market_equals_one():
    """El beta del mercado contra sí mismo debe ser ~1"""
    np.random.seed(42)
    market = pd.Series(np.random.normal(0.001, 0.01, 200))
    result = estimate_beta(market, market)
    assert abs(result["beta"] - 1.0) < 0.05


def test_capm_risk_free_asset():
    """Un activo sin riesgo (beta=0) debe tener retorno = Rf"""
    expected = capm_expected_return(beta=0.0, risk_free=0.02, market_premium=0.06)
    assert abs(expected - 0.02) < 1e-6


def test_capm_market_portfolio():
    """El portafolio de mercado (beta=1) tiene retorno = Rf + premium"""
    expected = capm_expected_return(beta=1.0, risk_free=0.02, market_premium=0.06)
    assert abs(expected - 0.08) < 1e-6


def test_sml_shape():
    betas = np.linspace(0, 2, 10)
    sml = security_market_line(betas)
    assert len(sml) == 10
    assert sml[0] < sml[-1], "SML debe ser creciente en beta"
