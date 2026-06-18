import re


def fact_recall_score(email: str, facts: list[str], judge_call_fn) -> float:
    """Returns a 0-100 score: percentage of facts confirmed present by the judge."""
    if not facts:
        return 100.0

    from src.prompts import FACT_RECALL_JUDGE_PROMPT

    hits = 0
    for fact in facts:
        judge_prompt = FACT_RECALL_JUDGE_PROMPT.format(email=email, fact=fact)
        response = judge_call_fn(judge_prompt)
        if response.strip().upper().startswith("YES"):
            hits += 1

    return 100.0 * hits / len(facts)


def tone_alignment_score(email: str, tone: str, judge_call_fn) -> float:
    """Returns a 0-100 score derived from a 1-5 LLM judge rating."""
    from src.prompts import TONE_ALIGNMENT_JUDGE_PROMPT

    judge_prompt = TONE_ALIGNMENT_JUDGE_PROMPT.format(tone=tone, email=email)
    response = judge_call_fn(judge_prompt)

    match = re.search(r"[1-5]", response)
    rating = int(match.group()) if match else 3

    return (rating - 1) / 4 * 100.0


def structural_quality_score(email: str) -> tuple[float, dict]:
    """
    Returns (overall_score, components_dict). No LLM call.
    """
    components = {}

    word_count = len(email.split())
    if 50 <= word_count <= 200:
        wc_score = 100.0
    elif word_count < 50:
        wc_score = max(0.0, 100.0 - (50 - word_count) * 4)
    else:
        wc_score = max(0.0, 100.0 - (word_count - 200) * 2)
    components["word_count_score"] = round(wc_score, 1)

    has_greeting = bool(re.search(r"(?im)^\s*(dear|hi|hello|hey)\b", email))
    components["greeting_score"] = 100.0 if has_greeting else 0.0

    has_signoff = bool(
        re.search(r"(?im)\b(regards|sincerely|best|thanks|thank you|cheers|warm(ly)?)\b", email)
    )
    components["signoff_score"] = 100.0 if has_signoff else 0.0

    sentences = [s.strip().lower() for s in re.split(r"[.!?]", email) if s.strip()]
    duplicate_count = max(0, len(sentences) - len(set(sentences)))
    no_dup_score = max(0.0, 100.0 - duplicate_count * 25)
    components["no_duplicate_score"] = round(no_dup_score, 1)

    overall = sum(components.values()) / len(components)
    return round(overall, 1), components
