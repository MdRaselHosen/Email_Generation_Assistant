import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_A = os.environ.get("MODEL_A", "meta-llama/llama-3.1-8b-instruct")
MODEL_B = os.environ.get("MODEL_B", "mistralai/mistral-small-24b-instruct-2501")

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", MODEL_A)

# Data path
SCENARIOS_PATH = "data/scenarios.json"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

SENDER_NAME = "SG Service"
RECEIVER_NAME  = "Md. Rasel Hosen"



