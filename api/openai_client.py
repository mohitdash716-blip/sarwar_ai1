"""
OpenAI API wrapper for Sarwar AI.
Supports GPT-4o and GPT-3.5-Turbo models.
"""

import os
from openai import OpenAI


def call_openai(prompt: str, model: str = "gpt-4o", history: list = None) -> str:
    """
    Send a prompt to the OpenAI API and return the response text.

    Args:
        prompt: The user's input message.
        model: The OpenAI model identifier (e.g., 'gpt-4o').
        history: List of prior messages in OpenAI format [{"role": ..., "content": ...}].

    Returns:
        The assistant's reply as a string.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file."

    client = OpenAI(api_key=api_key)

    messages = []
    messages.append({
        "role": "system",
        "content": (
            "You are Sarwar AI, a helpful, intelligent, and friendly assistant. "
            "Answer clearly and concisely."
        )
    })

    if history:
        for entry in history:
            messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI error: {str(e)}"
