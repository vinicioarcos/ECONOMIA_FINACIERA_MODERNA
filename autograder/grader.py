"""
autograder/grader.py
Evalúa notebooks y tests automáticamente.
Genera grade_report.json con puntaje y feedback.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_test_results(results_path: str) -> dict:
    with open(results_path) as f:
        return json.load(f)


def load_rubric(rubric_path: str) -> dict:
    with open(rubric_path) as f:
        return json.load(f)


def calculate_grade(results: dict, rubric: dict) -> dict:
    passed = results.get("summary", {}).get("passed", 0)
    failed = results.get("summary", {}).get("failed", 0)
    total_tests = passed + failed

    if total_tests == 0:
        return {"score": 0, "feedback": "No se encontraron tests."}

    pass_rate = passed / total_tests
    max_score = rubric.get("max_score", 100)
    auto_weight = rubric.get("auto_weight", 0.70)

    auto_score = pass_rate * max_score * auto_weight

    # Feedback por tests fallidos
    failed_tests = [
        t["nodeid"] for t in results.get("tests", [])
        if t["outcome"] == "failed"
    ]

    feedback = []
    if failed_tests:
        feedback.append(f"Tests fallidos ({len(failed_tests)}):")
        for t in failed_tests[:5]:
            feedback.append(f"  - {t.split('::')[-1]}")
    else:
        feedback.append("¡Todos los tests automáticos pasaron!")

    return {
        "timestamp": datetime.now().isoformat(),
        "tests_passed": passed,
        "tests_failed": failed,
        "pass_rate": round(pass_rate, 3),
        "auto_score": round(auto_score, 2),
        "max_auto_score": round(max_score * auto_weight, 2),
        "interpretation_score": None,  # Evaluado por el profesor
        "total_score": None,
        "feedback": "\n".join(feedback),
        "status": "PASS" if pass_rate >= 0.7 else "FAIL"
    }


def main():
    if len(sys.argv) < 3:
        print("Uso: python grader.py test_results.json rubric.json")
        sys.exit(1)

    results = load_test_results(sys.argv[1])
    rubric = load_rubric(sys.argv[2])
    report = calculate_grade(results, rubric)

    output_path = "grade_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*50}")
    print(f"ECONOLAB AUTOGRADER REPORT")
    print(f"{'='*50}")
    print(f"Tests pasados : {report['tests_passed']}")
    print(f"Tests fallidos: {report['tests_failed']}")
    print(f"Tasa de éxito : {report['pass_rate']*100:.1f}%")
    print(f"Puntaje auto  : {report['auto_score']:.1f} / {report['max_auto_score']:.1f}")
    print(f"Estado        : {report['status']}")
    print(f"\nFeedback:\n{report['feedback']}")
    print(f"\nReporte guardado en: {output_path}")


if __name__ == "__main__":
    main()
