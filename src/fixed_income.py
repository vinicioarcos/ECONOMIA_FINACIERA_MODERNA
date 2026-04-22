"""
Econolab — Módulo de Renta Fija y Valor del Dinero en el Tiempo
Valoración de bonos, VPN, TIR y análisis de flujos de caja.
"""

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from typing import Union


# ─────────────────────────────────────────────
# VALOR DEL DINERO EN EL TIEMPO
# ─────────────────────────────────────────────

def present_value(future_value: float, rate: float, periods: int) -> float:
    """
    Valor presente de un monto futuro.
    PV = FV / (1 + r)^n
    """
    return future_value / (1 + rate) ** periods


def future_value(present_value: float, rate: float, periods: int) -> float:
    """
    Valor futuro de un monto presente.
    FV = PV * (1 + r)^n
    """
    return present_value * (1 + rate) ** periods


def real_rate(nominal_rate: float, inflation_rate: float) -> float:
    """
    Tasa real (ecuación de Fisher).
    (1 + r_real) = (1 + r_nominal) / (1 + π)
    
    La tasa real es lo que importa para decisiones de ahorro e inversión real.
    """
    return (1 + nominal_rate) / (1 + inflation_rate) - 1


# ─────────────────────────────────────────────
# ANÁLISIS DE FLUJOS DE CAJA
# ─────────────────────────────────────────────

def npv(cashflows: Union[list, np.ndarray], rate: float) -> float:
    """
    Valor Presente Neto.
    VPN = Σ CF_t / (1+r)^t
    
    Regla de decisión:
    - VPN > 0: proyecto crea valor → aceptar
    - VPN < 0: proyecto destruye valor → rechazar
    - VPN = 0: proyecto indiferente
    
    Args:
        cashflows: flujos del periodo 0 al T (incluye inversión inicial negativa en [0])
        rate: tasa de descuento por periodo
    """
    t = np.arange(len(cashflows))
    return np.sum(np.array(cashflows) / (1 + rate) ** t)


def irr(cashflows: Union[list, np.ndarray]) -> float:
    """
    Tasa Interna de Retorno.
    TIR: tasa r* tal que VPN(r*) = 0.
    
    Regla: aceptar si TIR > costo de capital (WACC).
    
    Limitación: puede no existir o ser múltiple con flujos no convencionales.
    """
    try:
        return brentq(lambda r: npv(cashflows, r), -0.999, 10.0)
    except ValueError:
        return np.nan


def payback_period(cashflows: list) -> float:
    """
    Período de recuperación: ¿en cuántos periodos se recupera la inversión?
    
    Métrica simple pero ignora el valor del dinero en el tiempo.
    Útil como criterio secundario de liquidez.
    """
    cumulative = 0
    for i, cf in enumerate(cashflows):
        cumulative += cf
        if cumulative >= 0:
            return i
    return np.inf  # no se recupera


def npv_profile(
    cashflows: list,
    rates: np.ndarray = None,
) -> pd.DataFrame:
    """
    Perfil del VPN: VPN en función de la tasa de descuento.
    Útil para visualizar la sensibilidad del proyecto a cambios en el costo de capital.
    """
    if rates is None:
        rates = np.linspace(0.01, 0.40, 100)

    return pd.DataFrame({
        "tasa": rates,
        "VPN": [npv(cashflows, r) for r in rates],
    })


def compare_projects(projects: dict, wacc: float) -> pd.DataFrame:
    """
    Compara múltiples proyectos de inversión.
    
    Args:
        projects: {"Proyecto A": [flujos], "Proyecto B": [flujos], ...}
        wacc: costo de capital para todos los proyectos
    """
    rows = []
    for name, cfs in projects.items():
        project_npv = npv(cfs, wacc)
        project_irr = irr(cfs)
        pb = payback_period(cfs)

        rows.append({
            "Proyecto": name,
            "Inversión Inicial": abs(cfs[0]),
            "VPN": round(project_npv, 2),
            "TIR (%)": round(project_irr * 100, 2) if not np.isnan(project_irr) else "N/A",
            "Payback (períodos)": pb if pb != np.inf else "No recupera",
            "Decisión": "✓ Aceptar" if project_npv > 0 else "✗ Rechazar",
        })

    return pd.DataFrame(rows).set_index("Proyecto")


# ─────────────────────────────────────────────
# VALORACIÓN DE BONOS
# ─────────────────────────────────────────────

def bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    maturity_years: int,
    freq: int = 2,
) -> float:
    """
    Precio de un bono cupón fijo.
    
    P = Σ [C/(1+y/f)^t] + VF/(1+y/f)^T
    
    Relación inversa precio-tasa: cuando ytm sube, precio baja.
    
    Args:
        face_value: valor nominal
        coupon_rate: tasa cupón anual
        ytm: yield to maturity anual
        maturity_years: años al vencimiento
        freq: frecuencia de pagos por año (2 = semestral)
    """
    n = maturity_years * freq
    coupon = face_value * coupon_rate / freq
    y = ytm / freq

    periods = np.arange(1, n + 1)
    pv_coupons = coupon / (1 + y) ** periods
    pv_principal = face_value / (1 + y) ** n

    return pv_coupons.sum() + pv_principal


def bond_ytm(
    price: float,
    face_value: float,
    coupon_rate: float,
    maturity_years: int,
    freq: int = 2,
) -> float:
    """
    Yield to Maturity: tasa que iguala el precio de mercado con el valor presente de flujos.
    Resolución numérica (no tiene forma cerrada).
    """
    objective = lambda ytm: bond_price(face_value, coupon_rate, ytm, maturity_years, freq) - price
    try:
        return brentq(objective, 0.0001, 0.50)
    except ValueError:
        return np.nan


def bond_duration(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    maturity_years: int,
    freq: int = 2,
) -> dict:
    """
    Duration de Macaulay y Duration Modificada.
    
    Duration: vida media ponderada de los flujos de caja.
    Mide la sensibilidad del precio al cambio en las tasas.
    
    ΔP/P ≈ -D_mod * Δy
    """
    n = maturity_years * freq
    coupon = face_value * coupon_rate / freq
    y = ytm / freq

    periods = np.arange(1, n + 1)
    cashflows = np.full(n, coupon)
    cashflows[-1] += face_value

    pv_flows = cashflows / (1 + y) ** periods
    price = pv_flows.sum()

    macaulay_d = np.sum(periods * pv_flows) / price / freq
    modified_d = macaulay_d / (1 + ytm / freq)

    return {
        "price": round(price, 4),
        "macaulay_duration": round(macaulay_d, 4),
        "modified_duration": round(modified_d, 4),
        "dv01": round(-modified_d * price * 0.0001, 4),  # $ cambio por 1bp
    }
