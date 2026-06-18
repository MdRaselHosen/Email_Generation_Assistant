

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

NAIVE_PROMPT_TEMPLATE = """Write a {tone} email about:{intent}.

Include these facts:
{facts_bullets}
"""

FACT_RECALL_JUDGE_PROMPT = """You are evaluating whether an email includes a specific fact. Respond with only one word: YES or NO.

Email:
\"\"\"
{email}
\"\"\"

Fact to check: "{fact}"

Does the email clearly and accurately convey this fact? It may be paraphrased rather than quoted word-for-word, but the meaning must be preserved and not contradicted. Answer YES or NO only, with no other text.
"""

TONE_ALIGNMENT_JUDGE_PROMPT = """You are a writing-quality evaluator. Rate how well the tone of the following email matches the target tone.

Target tone: {tone}

Email:
\"\"\"
{email}
\"\"\"

Rating scale:
1 = tone is opposite of or completely mismatched with the target
2 = tone is mostly mismatched
3 = tone is partially aligned but inconsistent
4 = tone is mostly well-aligned with only minor issues
5 = tone is strong, consistent match throughout

Respond with only a single digit from 1 to 5, with no other text.
"""