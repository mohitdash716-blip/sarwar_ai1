"""
Google Gemini API wrapper for Sarwar AI.
Supports Gemini 1.5 Pro and Gemini 1.5 Flash models.
"""

import os
import google.generativeai as genai


def call_gemini(prompt: str, model: str = "gemini-1.5-pro", history: list = None) -> str:
    """
    Send a prompt to the Google Gemini API and return the response text.

    Args:
        prompt: The user's input message.
        model: The Gemini model identifier (e.g., 'gemini-1.5-pro').
        history: List of prior messages [{"role": ..., "content": ...}].

    Returns:
        The assistant's reply as a string.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        return "⚠️ Google API key not found. Please set GOOGLE_API_KEY in your .env file."

    genai.configure(api_key=api_key)

    generation_config = genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=2048,
    )

    gemini_model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
        system_instruction=(
            "You are Sarwar AI, a helpful, intelligent, and friendly assistant. "
            "Answer clearly and concisely."
        ),
    )

    # Build Gemini-format history (alternating user/model turns)
    chat_history = []
    if history:
        for entry in history:
            role = "model" if entry["role"] == "assistant" else "user"
            chat_history.append({"role": role, "parts": [entry["content"]]})

    chat = gemini_model.start_chat(history=chat_history)

    try:
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"
