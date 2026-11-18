import os
import sys
from typing import Optional
from groq import Groq

_client: Optional[Groq] = None


def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "").strip()


def is_groq_available() -> bool:
    return bool(get_groq_api_key())


def get_groq_client() -> Optional[Groq]:
    global _client
    api_key = get_groq_api_key()
    if not api_key:
        return None
    try:
        if _client is None or getattr(_client, "api_key", None) != api_key:
            _client = Groq(api_key=api_key)
        return _client
    except Exception as e:
        print(f"[GroqClient] Client initialization error: {e}", file=sys.stderr)
        return None


def call_groq_chat(prompt: str, temperature: float = 0.0) -> Optional[str]:
    """
    Safely executes a Groq chat completion with model fallback.
    Returns None if Groq is unavailable, unconfigured, or encounters an API error.
    """
    client = get_groq_client()
    if not client:
        return None

    # Supported Groq models in priority order
    models_to_try = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
    ]

    for model in models_to_try:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            content = completion.choices[0].message.content
            if content and content.strip():
                return content.strip()
        except Exception as e:
            print(f"[GroqClient] Model {model} attempt failed: {e}", file=sys.stderr)
            continue

    return None
