import csv
import json
import os
import time

from src.config import MODEL_A, MODEL_B, JUDGE_MODEL, SCENARIOS_PATH, RESULTS_DIR
from src.generator import generate_email
from src.metrics import fact_recall_score, tone_alignment_score, structural_quality_score
from src.llm_client import call_llm

SLEEP_BETWEEN_CALLS_SECONDS = 1.5


def judge_call(prompt: str) -> str:
    """Wrapper so metrics.py doesn't need to know which model is the judge."""
    return call_llm(prompt, model=JUDGE_MODEL, temperature=0.0, max_tokens=10)


def load_scenarios() -> list[dict]:
    with open(SCENARIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_evaluation(model_name: str, strategy: str = "advanced", label: str = "model") -> str:
    """
    Runs all scenarios through `model_name` using `strategy`, scores each
    output, writes results/results_<label>.csv, and returns the file path.
    """
    scenarios = load_scenarios()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, f"results_{label}.csv")

    rows = []
    for i, scenario in enumerate(scenarios, start=1):
        print(f"[{label}] Scenario {i}/{len(scenarios)}: {scenario['intent']}")

        email = generate_email(scenario, model=model_name, strategy=strategy)
        time.sleep(SLEEP_BETWEEN_CALLS_SECONDS)

        recall = fact_recall_score(email, scenario["facts"], judge_call)
        tone_score = tone_alignment_score(email, scenario["tone"], judge_call)
        struct_score, _components = structural_quality_score(email)

        rows.append(
            {
                "scenario_id": scenario["id"],
                "intent": scenario["intent"],
                "tone": scenario["tone"],
                "generated_email": email,
                "fact_recall_score": round(recall, 1),
                "tone_alignment_score": round(tone_score, 1),
                "structural_quality_score": struct_score,
            }
        )

    avg_recall = sum(r["fact_recall_score"] for r in rows) / len(rows)
    avg_tone = sum(r["tone_alignment_score"] for r in rows) / len(rows)
    avg_struct = sum(r["structural_quality_score"] for r in rows) / len(rows)

    rows.append(
        {
            "scenario_id": "AVERAGE",
            "intent": "",
            "tone": "",
            "generated_email": "",
            "fact_recall_score": round(avg_recall, 1),
            "tone_alignment_score": round(avg_tone, 1),
            "structural_quality_score": round(avg_struct, 1),
        }
    )

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"[{label}] Saved results to {out_path}\n")
    return out_path


if __name__ == "__main__":
    print(f"Running Model A: {MODEL_A}")
    run_evaluation(MODEL_A, strategy="advanced", label="model_a")

    print(f"Running Model B: {MODEL_B}")
    run_evaluation(MODEL_B, strategy="advanced", label="model_b")

    print("Done.You can check the comparison now")
