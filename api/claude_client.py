"""
Anthropic Claude API wrapper for Sarwar AI.
Supports Claude 3 Opus and Claude 3 Sonnet models.
"""

import os
import anthropic


def call_claude(prompt: str, model: str = "claude-3-opus-20240229", history: list = None) -> str:
    """
    Send a prompt to the Anthropic Claude API and return the response text.

    Args:
        prompt: The user's input message.
        model: The Anthropic model identifier.
        history: List of prior messages [{"role": ..., "content": ...}].

    Returns:
        The assistant's reply as a string.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "⚠️ Anthropic API key not found. Please set ANTHROPIC_API_KEY in your .env file."

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are Sarwar AI, a helpful, intelligent, and friendly assistant. "
        "Answer clearly and concisely."
    )

    messages = []
    if history:
        for entry in history:
            messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"⚠️ Claude error: {str(e)}"
