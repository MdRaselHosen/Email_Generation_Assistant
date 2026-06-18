import csv
import os

from src.config import RESULTS_DIR, MODEL_A, MODEL_B


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compare(path_a: str, path_b: str, label_a: str = "Model A", label_b: str = "Model B") -> None:
    rows_a = load_csv(path_a)
    rows_b = load_csv(path_b)

    avg_a = next(r for r in rows_a if r["scenario_id"] == "AVERAGE")
    avg_b = next(r for r in rows_b if r["scenario_id"] == "AVERAGE")

    metrics = ["fact_recall_score", "tone_alignment_score", "structural_quality_score"]

    print("\n=== Average Scores (0-100) ===")
    print(f"{'Metric':30s} {label_a:>15s} {label_b:>15s}")
    for metric in metrics:
        print(f"{metric:30s} {avg_a[metric]:>15s} {avg_b[metric]:>15s}")

    scenarios_a = {r["scenario_id"]: r for r in rows_a if r["scenario_id"] != "AVERAGE"}
    scenarios_b = {r["scenario_id"]: r for r in rows_b if r["scenario_id"] != "AVERAGE"}

    biggest_gap_id = None
    biggest_gap_value = -1.0
    for scenario_id in scenarios_a:
        if scenario_id not in scenarios_b:
            continue
        gap = abs(float(scenarios_a[scenario_id]["fact_recall_score"]) - float(scenarios_b[scenario_id]["fact_recall_score"]))
        if gap > biggest_gap_value:
            biggest_gap_value = gap
            biggest_gap_id = scenario_id

    if biggest_gap_id is not None:
        sa = scenarios_a[biggest_gap_id]
        sb = scenarios_b[biggest_gap_id]
        print(f"\nBiggest fact-recall gap: Scenario {biggest_gap_id} ({sa['intent']})")
        print(f"  {label_a}: {sa['fact_recall_score']}   {label_b}: {sb['fact_recall_score']}")


if __name__ == "__main__":
    path_a = os.path.join(RESULTS_DIR, "results_model_a.csv")
    path_b = os.path.join(RESULTS_DIR, "results_model_b.csv")
    compare(path_a, path_b, label_a=f"A ({MODEL_A})", label_b=f"B ({MODEL_B})")
