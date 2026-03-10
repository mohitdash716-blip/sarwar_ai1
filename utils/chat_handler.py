"""
Chat handler for Sarwar AI.
Routes prompts to the correct API based on the selected model key.
"""

from api.openai_client import call_openai
from api.claude_client import call_claude
from api.gemini_client import call_gemini

# Mapping of display model names to (provider_key, api_model_id)
MODEL_MAP = {
    "GPT-4o": ("openai", "gpt-4o"),
    "GPT-3.5-Turbo": ("openai", "gpt-3.5-turbo"),
    "Claude 3 Opus": ("claude", "claude-3-opus-20240229"),
    "Claude 3 Sonnet": ("claude", "claude-3-sonnet-20240229"),
    "Gemini 1.5 Pro": ("gemini", "gemini-1.5-pro"),
    "Gemini 1.5 Flash": ("gemini", "gemini-1.5-flash"),
}


def get_available_models() -> list:
    """Return all supported model display names."""
    return list(MODEL_MAP.keys())


def handle_chat(prompt: str, selected_model: str, history: list = None) -> str:
    """
    Route a user prompt to the appropriate AI API based on the selected model.

    Args:
        prompt: User's input text.
        selected_model: Display name from MODEL_MAP keys.
        history: Prior conversation messages [{"role": ..., "content": ...}].

    Returns:
        AI-generated response string.
    """
    if selected_model not in MODEL_MAP:
        return f"⚠️ Unknown model: {selected_model}"

    provider, model_id = MODEL_MAP[selected_model]

    if provider == "openai":
        return call_openai(prompt, model_id, history)
    elif provider == "claude":
        return call_claude(prompt, model_id, history)
    elif provider == "gemini":
        return call_gemini(prompt, model_id, history)
    else:
        return "⚠️ Unsupported provider."
