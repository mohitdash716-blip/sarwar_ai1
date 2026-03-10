"""
AI Tools utility functions for Sarwar AI.
Each tool builds a task-specific system prompt and delegates to the chat handler.
"""

from utils.chat_handler import handle_chat


def run_summarizer(text: str, selected_model: str) -> str:
    """
    Summarize the provided text using the selected AI model.

    Args:
        text: The text to summarize.
        selected_model: Model display name.

    Returns:
        Summarized text string.
    """
    prompt = (
        f"Please provide a clear and concise summary of the following text. "
        f"Highlight the key points and main ideas:\n\n{text}"
    )
    return handle_chat(prompt, selected_model, history=None)


def run_email_generator(context: str, tone: str, selected_model: str) -> str:
    """
    Generate a professional email based on the given context and tone.

    Args:
        context: Brief description of what the email should communicate.
        tone: Email tone (e.g., 'professional', 'friendly', 'formal').
        selected_model: Model display name.

    Returns:
        Generated email as a string.
    """
    prompt = (
        f"Write a complete, well-structured email with the following details:\n"
        f"Context: {context}\n"
        f"Tone: {tone}\n\n"
        f"Include a subject line, greeting, body, and closing signature."
    )
    return handle_chat(prompt, selected_model, history=None)


def run_rewriter(text: str, style: str, selected_model: str) -> str:
    """
    Rewrite the provided text in a given style.

    Args:
        text: Original text to rewrite.
        style: Rewriting style (e.g., 'formal', 'casual', 'simpler', 'more detailed').
        selected_model: Model display name.

    Returns:
        Rewritten text as a string.
    """
    prompt = (
        f"Rewrite the following text in a {style} style while preserving the "
        f"original meaning and key information:\n\n{text}"
    )
    return handle_chat(prompt, selected_model, history=None)


def run_content_generator(topic: str, content_type: str, selected_model: str) -> str:
    """
    Generate content on a given topic.

    Args:
        topic: The subject to write about.
        content_type: Type of content (e.g., 'blog post', 'social media caption',
                      'product description', 'LinkedIn post').
        selected_model: Model display name.

    Returns:
        Generated content as a string.
    """
    prompt = (
        f"Create a high-quality {content_type} about the following topic:\n\n"
        f"Topic: {topic}\n\n"
        f"Make it engaging, well-structured, and appropriate for the content type."
    )
    return handle_chat(prompt, selected_model, history=None)
