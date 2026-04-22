# Econolab Financial Economics

> Curso completo de Economía Financiera · Python + datos + evaluación automática

[![Tests](https://img.shields.io/badge/tests-22%20passed-22c55e?style=flat-square)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%2B-3b82f6?style=flat-square)](requirements.txt)

Un repositorio listo para clonar que convierte la Economía Financiera en un laboratorio de decisiones con datos reales. Diseñado para 7mo semestre de Economía.

## Inicio rápido

```bash
git clone https://github.com/vinicioarcos/ECONOMIA_FINACIERA_MODERNA.git
cdECONOMIA_FINACIERA_MODERNA
pip install -r requirements.txt
python data/generate_data.py
pytest tests/ -v                  # 22 tests, todos deben pasar
jupyter notebook
```

## Estructura

```
src/            módulos Python reutilizables (returns, portfolio, capm, risk, fixed_income)
notebooks/      clases prácticas semanas 1–16
data/           generador de datasets simulados reproducibles
tests/          22 tests automáticos con propiedades económicas
autograder/     evaluador de entregas de estudiantes
rubric/         rúbricas JSON por semana y proyecto final
analytics/      engine de datos para el dashboard docente
frontend/       dashboard.html — panel docente interactivo
.github/        GitHub Actions para evaluación automática
```

## Módulos principales

```python
from src.returns     import log_returns, sharpe_ratio, rolling_volatility
from src.portfolio   import min_variance_portfolio, max_sharpe_portfolio, efficient_frontier
from src.capm        import estimate_beta, rolling_beta, multi_asset_betas
from src.risk        import historical_var, conditional_var, risk_dashboard
from src.fixed_income import npv, irr, bond_price, compare_projects
```

## Evaluación automática

`.github/workflows/autograding.yml` corre en cada push del estudiante:
evalúa tests, calcula puntaje y publica resultado en el PR.

| Componente | Peso |
|---|---|
| Tests automáticos | 50% |
| Interpretación económica | 20% |
| Proyecto aplicado | 30% |

## Dashboard docente

Abrir `frontend/dashboard.html` en el navegador: KPIs, evolución semanal, tabla de estudiantes con búsqueda, alertas de riesgo académico.
