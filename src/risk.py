"""risk.py — Métricas de riesgo financiero"""
import numpy as np
import pandas as pd


def volatility(returns: pd.Series, annualize: bool = True, trading_days: int = 252) -> float:
    """Volatilidad (desviación estándar de retornos)"""
    vol = returns.std()
    return vol * np.sqrt(trading_days) if annualize else vol


def var_historical(returns: pd.Series, confidence: float = 0.95) -> float:
    """Value at Risk histórico"""
    return np.percentile(returns, (1 - confidence) * 100)


def var_parametric(returns: pd.Series, confidence: float = 0.95) -> float:
    """VaR paramétrico (distribución normal)"""
    from scipy import stats
    return returns.mean() + stats.norm.ppf(1 - confidence) * returns.std()


def sharpe_ratio(returns: pd.Series, risk_free: float = 0.02, trading_days: int = 252) -> float:
    """Ratio de Sharpe anualizado"""
    excess = returns - risk_free / trading_days
    return (excess.mean() / excess.std()) * np.sqrt(trading_days)


def rolling_volatility(returns: pd.Series, window: int = 21) -> pd.Series:
    """Volatilidad móvil (ventana de 21 días = ~1 mes)"""
    return returns.rolling(window).std() * np.sqrt(252)
