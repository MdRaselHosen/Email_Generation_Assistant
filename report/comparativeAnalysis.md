##  Comparative Analysis

**Which model/strategy performed better according to the 3 custom metrics?**

[Fill in using the averages printed by `python -m src.compare`.]

Model Comparison Results

Average Scores (0–100)

Metric	A (meta-llama/llama-3.1-8b-instruct)	B (mistralai/mistral-small-24b-instruct-2501)
Fact Recall Score	90.0	83.3
Tone Alignment Score	77.5	77.5
Structural Quality Score	97.5	96.7

Key Observation

Biggest fact-recall gap: Scenario 8 — Brief thank-you note after an interview

Model	Fact Recall Score
A (meta-llama/llama-3.1-8b-instruct)	0.0
B (mistralai/mistral-small-24b-instruct-2501)	100.0

Summary

* Model A achieved the highest overall Fact Recall Score (90.0 vs. 83.3).
* Both models performed identically on Tone Alignment (77.5).
* Model A slightly outperformed Model B on Structural Quality (97.5 vs. 96.7).
* The largest performance difference occurred in Scenario 8, where Model B captured all required facts while Model A failed to include them.

