"""Tests — Semana 3 & 13: Valoración"""
import pytest
from src.valuation import npv, irr, bond_price, wacc


def test_npv_simple():
    cash_flows = [-1000, 300, 400, 500, 200]
    result = npv(cash_flows, 0.10)
    assert result > 0, "Este proyecto debería ser rentable"


def test_npv_zero_discount():
    cash_flows = [-100, 50, 50, 50]
    result = npv(cash_flows, 0.0)
    assert abs(result - 50.0) < 1e-6


def test_irr_basic():
    cash_flows = [-1000, 400, 400, 400, 400]
    result = irr(cash_flows)
    assert 0.20 < result < 0.25, f"IRR esperado ~22%, obtenido {result:.3f}"


def test_bond_price_par():
    """Un bono con coupon = ytm debe cotizar a la par"""
    price = bond_price(face_value=1000, coupon_rate=0.05, ytm=0.05, periods=5)
    assert abs(price - 1000.0) < 0.01


def test_wacc_reasonable():
    w = wacc(equity=600, debt=400, cost_equity=0.12, cost_debt=0.06, tax_rate=0.25)
    assert 0.05 < w < 0.15
