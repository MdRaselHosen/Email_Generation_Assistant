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