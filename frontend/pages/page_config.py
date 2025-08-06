from dotenv import load_dotenv
import os

load_dotenv()

# Module mapping (constant)
MODULE_MAP = {
    "Human Computer Interaction": "HCI",
    "Serious Games": "SG",
}

# API configuration (constants only)
API_KEY_URL = "https://aistudio.google.com/app/apikey"
DEFAULT_MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite-preview-06-17")

# Exam configuration (constants)
EXAM_TIME = 90  # minutes
SECONDS_BETWEEN_CALLS = 60.0 / 15.0  # Rate limit: max 15 calls per minute

def get_module_abbreviation(module: str) -> str | None:
    """Get module abbreviation for a given module name"""
    return MODULE_MAP.get(module)