# Email Generation Assistant -- Final Report

## 1. Prompt Template Used

**Advanced technique:** Role-playing + Few-shot examples + Hidden chain-of-thought.

```


ADVANCED_PROMPT_TEMPLATE = """You are a senior executive assistant with several years of experience writing precise, polished, and effective business correspondence. You have a strong command of tone, structure, and concision, and you never include unnecessary filter.

Before writing, silently think through which facts must appear and how they fit naturally into the flow of the email. Do NOT show this thinking - output only the final email.

Here are examples of the quality and style expected:

---
Example 1:
Intent: Follow up after a product demo
Facts:
- Demo took place last week
- Client asked about API rate limits
- Trail account expires in 2 weeks

Tone: Formal
Email:
Subject: Following Up on Last week's Product Demo
Dear {RECEIVER_NAME},

Thank you for joining the product demo last week. I wanted to follow up on your question about API rate limits - Happy to share more detail whenever convenient.

As a reminder, your trail account is active for 2 weeks more, so please let me know if you'd like help getting set up before then.

Best regards,
{SENDER_NAME}

---
Example 2:
Intent: Apologize for a missed deadline
Facts:
- Delivered was due Monday
- Delay caused by a vendor issue
- New delivery date is Thursday
Tone: empathetic

Email:
Subject: Update on Your Deliverable

Hi {RECEIVER_NAME},

I want to personally apologize that the deliverable due Monday wasn't completed on time. The delay was caused by an issue on our vendor's end that took longer than expected to resolve.

We now expect to deliver by Thursday, and I'll keep you posted on any changes. Thank you for your patience.

Best,
{SENDER_NAME}
---

Now write a new email the same level of quality, structure and tone-matching.

Intent: {intent}

Key Facts - all must be naturally included:
{facts_bullets}

Tone: {tone}

Write only the email. Use the provided recipient name `{RECEIVER_NAME}` and sender name `{SENDER_NAME}` where appropriate; do not replace them with generic placeholders like "[you name]". Do not include any explanation, preamble, headers, or notes outside the email itself.

"""
```

**Why this combination:** Role-playing anchors a consistent professional
voice, few-shot examples fix structure/length without needing explicit
formatting rules, and the hidden chain-of-thought step improves fact
coverage by forcing an internal planning pass -- without leaking visible
reasoning into the output.

---

## 2. Custom Metric Definitions and Logic

### Metric 1: Fact Recall Score
- **Type:** LLM-as-a-judge
- **Logic:** For each input fact, ask the judge model a strict YES/NO
  question: "Does the email clearly and accurately convey this fact?"
  Score = (facts confirmed / total facts) x 100.
- **Why this metric:** Missing or contradicted facts are the most costly
  failure mode for a real-world email assistant.

### Metric 2: Tone Alignment Score
- **Type:** LLM-as-a-judge, fixed 1-5 rubric
- **Logic:** Judge rates tone match on a 1-5 scale with explicit anchor
  descriptions at each point; rescaled to 0-100.
- **Why this metric:** Tone is one of the three explicit user inputs, so
  failing to match it is a direct failure of the core task.

### Metric 3: Structural Quality Score
- **Type:** Deterministic, pure Python (no LLM call)
- **Logic:** Average of four 0-100 sub-scores: word count within a
  50-200 word band, presence of a greeting, presence of a sign-off, and
  absence of duplicated sentences.
- **Why this metric:** Captures formatting/structure quality without
  depending on (or paying for) an LLM call, and complements the two
  judge-based metrics with a fully reproducible signal.

---


## 3. Comparative Analysis

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

