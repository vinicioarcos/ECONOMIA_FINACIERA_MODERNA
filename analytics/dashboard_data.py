"""
Econolab — Analytics Engine
Genera datos de rendimiento estudiantil para el dashboard docente.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime, timedelta


def simulate_cohort_data(
    n_students: int = 28,
    n_weeks: int = 16,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Simula datos de un semestre completo para demostración del dashboard.
    En producción, esto vendría de la base de datos de entregas.
    """
    np.random.seed(seed)

    students = [f"S{str(i).zfill(3)}" for i in range(1, n_students + 1)]
    names = [
        "Ana Torres", "Carlos Mora", "Sofía Vega", "Diego Rivas",
        "Valeria Cruz", "Andrés León", "Camila Ortiz", "Mateo Silva",
        "Isabella Ruiz", "Sebastián Paz", "Daniela Reyes", "Felipe Herrera",
        "Natalia Jiménez", "Emilio Vargas", "Lucía Mendoza", "Rodrigo Fuentes",
        "Paulina Castro", "Tomás Espinoza", "Renata Flores", "Ignacio Bravo",
        "Valentina Ríos", "Álvaro Peña", "Carolina Salinas", "Héctor Molina",
        "Gabriela Campos", "Javier Guerrero", "Fernanda Pinto", "Oscar Rojas",
    ][:n_students]

    records = []
    for i, (sid, name) in enumerate(zip(students, names)):
        # Perfil base de cada estudiante (algunos fuertes, algunos débiles)
        base_score = np.random.normal(72, 15)
        base_score = np.clip(base_score, 30, 100)
        trend = np.random.choice([-0.5, 0, 0.3, 0.8], p=[0.15, 0.40, 0.30, 0.15])

        for week in range(1, n_weeks + 1):
            if week > 8 and np.random.random() < 0.05:
                # 5% de probabilidad de no entregar después del parcial
                continue

            weekly_noise = np.random.normal(0, 8)
            score = base_score + trend * week + weekly_noise
            score = np.clip(score, 0, 100)

            records.append({
                "student_id": sid,
                "name": name,
                "week": week,
                "score": round(score, 1),
                "tests_passed": int(np.round(score / 100 * np.random.randint(8, 15))),
                "tests_total": np.random.randint(10, 16),
                "submitted": True,
                "submission_date": (datetime(2025, 1, 20) + timedelta(weeks=week)).strftime("%Y-%m-%d"),
            })

    return pd.DataFrame(records)


def compute_student_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen por estudiante: promedio, tendencia, riesgo."""
    summary = df.groupby(["student_id", "name"]).agg(
        avg_score=("score", "mean"),
        weeks_submitted=("week", "count"),
        last_score=("score", "last"),
        std_score=("score", "std"),
    ).reset_index()

    summary["avg_score"] = summary["avg_score"].round(1)
    summary["std_score"] = summary["std_score"].round(1)

    # Clasificación de riesgo
    def risk_level(row):
        if row["avg_score"] < 55 or row["weeks_submitted"] < 10:
            return "alto"
        elif row["avg_score"] < 65:
            return "medio"
        return "bajo"

    summary["risk"] = summary.apply(risk_level, axis=1)

    # Tendencia (pendiente de últimas 4 semanas)
    def compute_trend(sid):
        student_data = df[df["student_id"] == sid].tail(4)
        if len(student_data) < 2:
            return 0.0
        x = np.arange(len(student_data))
        slope = np.polyfit(x, student_data["score"].values, 1)[0]
        return round(slope, 2)

    summary["trend"] = summary["student_id"].apply(compute_trend)

    return summary.sort_values("avg_score", ascending=False)


def compute_weekly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Estadísticas por semana: media, mediana, tasa de aprobación."""
    stats = df.groupby("week").agg(
        avg_score=("score", "mean"),
        median_score=("score", "median"),
        min_score=("score", "min"),
        max_score=("score", "max"),
        submissions=("student_id", "count"),
        approval_rate=("score", lambda x: (x >= 60).mean()),
    ).reset_index()

    stats["avg_score"] = stats["avg_score"].round(1)
    stats["approval_rate"] = (stats["approval_rate"] * 100).round(1)

    return stats


def get_at_risk_students(summary: pd.DataFrame) -> pd.DataFrame:
    """Estudiantes en riesgo académico que requieren atención."""
    return summary[summary["risk"] == "alto"][
        ["student_id", "name", "avg_score", "weeks_submitted", "trend", "risk"]
    ].sort_values("avg_score")


def export_dashboard_data(output_path: Path = None) -> dict:
    """Genera todos los datos del dashboard en formato JSON."""
    df = simulate_cohort_data()
    summary = compute_student_summary(df)
    weekly = compute_weekly_stats(df)
    at_risk = get_at_risk_students(summary)

    data = {
        "cohort_size": int(df["student_id"].nunique()),
        "weeks_completed": int(df["week"].max()),
        "course_average": round(df["score"].mean(), 1),
        "approval_rate": round((df["score"] >= 60).mean() * 100, 1),
        "at_risk_count": len(at_risk),
        "students": summary.to_dict(orient="records"),
        "weekly_stats": weekly.to_dict(orient="records"),
        "at_risk": at_risk.to_dict(orient="records"),
        "score_distribution": {
            "bins": [0, 40, 55, 65, 75, 85, 100],
            "labels": ["< 40", "40–55", "55–65", "65–75", "75–85", "85–100"],
            "counts": [
                int((df["score"] < 40).sum()),
                int(((df["score"] >= 40) & (df["score"] < 55)).sum()),
                int(((df["score"] >= 55) & (df["score"] < 65)).sum()),
                int(((df["score"] >= 65) & (df["score"] < 75)).sum()),
                int(((df["score"] >= 75) & (df["score"] < 85)).sum()),
                int((df["score"] >= 85).sum()),
            ]
        },
        "generated_at": datetime.now().isoformat(),
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    return data


if __name__ == "__main__":
    data = export_dashboard_data(Path("analytics/dashboard_data.json"))
    print(f"Dashboard generado: {data['cohort_size']} estudiantes, "
          f"promedio {data['course_average']}, "
          f"{data['at_risk_count']} en riesgo.")
