# Email Generation Assistant

A prototype that generates professional emails from three inputs
(**Intent**, **Key Facts**, **Tone**), evaluated with three custom metrics
and compared across two free LLMs via [OpenRouter](https://openrouter.ai).

## How it works

1. `src/generator.py` fills a prompt template with the scenario and calls
   the chosen model through OpenRouter.
2. `src/evaluate.py` runs all 10 scenarios in `data/scenarios.json` through
   **meta-llama/llama-3.1-8b-instruct** and **mistralai/mistral-small-24b-instruct-2501**, scores every output with the 3 custom
   metrics in `src/metrics.py`, and writes `results/results_model_a.csv`
   and `results/results_model_b.csv`.
3. `src/compare.py` prints a side-by-side summary of the two result files.

## Prompting technique used

The generation prompt (`ADVANCED_PROMPT_TEMPLATE` in `src/prompts.py`)
combines three techniques:

- **Role-playing** -- the model is anchored to a "senior executive
  assistant" persona for consistent, professional tone.
- **Few-shot examples** -- two worked examples (different tones) show the
  expected structure and length.
- **Hidden chain-of-thought** -- the model is told to privately plan which
  facts map to which sentences, but to output only the final email.

A `NAIVE_PROMPT_TEMPLATE` baseline is also included if you want to compare
"advanced prompt vs naive prompt" on the same model as an additional
experiment.

## Custom metrics

| Metric | Type | What it measures |
|---|---|---|
| Fact Recall Score | LLM-as-judge | % of input facts clearly conveyed in the email |
| Tone Alignment Score | LLM-as-judge (1-5 rubric) | How well the email's tone matches the requested tone |
| Structural Quality Score | Deterministic (pure Python) | Word count band, greeting present, sign-off present, no duplicated sentences |

Full definitions and logic are documented in the docstring at the top of
`src/metrics.py`.

## Setup

```bash
git clone <https://github.com/MdRaselHosen/Email_Generation_Assistant.git>
cd Email_Generation_Assistant
python -m venv emailenv
source emailenv/bin/activate
pip install -r requirements.txt
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys) (no
credit card needed) and paste it into `.env`.

> **Note:** free model availability on OpenRouter changes over time. If a
> model in `.env` returns an error, check
> [openrouter.ai/models?max_price=0](https://openrouter.ai/models?max_price=0)
> for current free options and update `MODEL_A` / `MODEL_B` / `JUDGE_MODEL`.

## Run the evaluation

```bash
python -m src.evaluate
```

This runs all 10 scenarios through Model A, then through Model B (each
takes a few minutes on free-tier rate limits), and writes:

- `results/results_model_a.csv`
- `results/results_model_b.csv`

Each CSV contains one row per scenario (intent, tone, the generated email,
and the 3 metric scores) plus a final `AVERAGE` row.

## Compare the two models

```bash
python -m src.compare
```

Prints average scores side by side and flags the scenario with the
biggest fact-recall gap between the two models -- a good starting point
for the report's failure-mode analysis.

## Project structure

```
email-assistant/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── scenarios.json       # 10 test scenarios + human reference emails
├── src/
│   ├── config.py             # model names, API key loading
│   ├── llm_client.py         # OpenRouter API wrapper (with retries)
│   ├── prompts.py            # advanced + naive templates, judge prompts
│   ├── generator.py          # email generation logic
│   ├── metrics.py            # 3 custom metrics
│   ├── evaluate.py           # main harness
│   └── compare.py            # Model A vs Model B summary
├── results/                  # CSV outputs land here after running evaluate.py
└── report/
    └── REPORT_TEMPLATE.md    # skeleton for the final report deliverable
```

## Writing the final report

`report/REPORT_TEMPLATE.md` already contains the prompt template and
metric definitions. After running `evaluate.py` and `compare.py`, paste
your CSV data and fill in the analysis section, then export to PDF or
Google Docs.
