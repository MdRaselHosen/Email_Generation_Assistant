from src.prompts import ADVANCED_PROMPT_TEMPLATE, NAIVE_PROMPT_TEMPLATE
from src.llm_client import call_llm
from src.config import SENDER_NAME, RECEIVER_NAME


def build_facts_bullets(facts: list[str]) -> str:
    return "\n".join(f"- {fact}" for fact in facts)


def generate_email(scenario: dict, model: str, strategy: str = "advanced", temperature: float = 0.7) -> str:
    """
    scenario: dict with keys "intent", "facts" (list[str]), "tone"
    model: OpenRouter model identifier, e.g. "meta-llama/llama-3.1-8b-instruct:free"
    strategy: "advanced" (role-play + few-shot + hidden CoT) or "naive" (baseline)
    """
    facts_bullets = build_facts_bullets(scenario["facts"])

    if strategy == "advanced":
        prompt = ADVANCED_PROMPT_TEMPLATE.format(
            intent=scenario["intent"],
            facts_bullets=facts_bullets,
            tone=scenario["tone"],
            SENDER_NAME=SENDER_NAME,
            RECEIVER_NAME=RECEIVER_NAME,
        )
    elif strategy == "naive":
        prompt = NAIVE_PROMPT_TEMPLATE.format(
            intent=scenario["intent"],
            facts_bullets=facts_bullets,
            tone=scenario["tone"],
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy!r}. Use 'advanced' or 'naive'.")

    return call_llm(prompt, model=model, temperature=temperature)
