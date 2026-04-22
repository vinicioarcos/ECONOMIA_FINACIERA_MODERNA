"""valuation.py — Valoración de activos y proyectos"""
import numpy as np
from typing import List


def npv(cash_flows: List[float], discount_rate: float) -> float:
    """Valor Presente Neto"""
    return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows))


def irr(cash_flows: List[float], guess: float = 0.1) -> float:
    """Tasa Interna de Retorno (método Newton-Raphson)"""
    from scipy.optimize import brentq
    try:
        return brentq(lambda r: npv(cash_flows, r), -0.999, 10.0)
    except ValueError:
        return float('nan')


def bond_price(face_value: float, coupon_rate: float, ytm: float, periods: int) -> float:
    """Precio de un bono de cupón fijo"""
    coupon = face_value * coupon_rate
    price = sum(coupon / (1 + ytm) ** t for t in range(1, periods + 1))
    price += face_value / (1 + ytm) ** periods
    return round(price, 4)


def wacc(equity: float, debt: float, cost_equity: float, cost_debt: float, tax_rate: float = 0.25) -> float:
    """Costo Promedio Ponderado de Capital"""
    total = equity + debt
    return (equity / total) * cost_equity + (debt / total) * cost_debt * (1 - tax_rate)
