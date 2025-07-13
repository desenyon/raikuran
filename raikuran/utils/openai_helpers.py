# raikuran/utils/openai_helpers.py

import os
from openai import OpenAI
from openai.types.chat import ChatCompletion
from typing import List, Dict
import typer

# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    typer.echo("❌ OPENAI_API_KEY not set. Please export it in your shell or .env.")
    raise typer.Exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def run_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
    max_tokens: int = 1500
) -> str:
    """
    Run a GPT-4 chat completion request and return the response text.

    Args:
        messages: List of dicts containing messages, e.g. [{"role": "user", "content": "..."}]
        model: GPT model to use (default: gpt-4)
        temperature: Creativity level (default: 0.3)
        max_tokens: Max tokens in output (default: 1500)

    Returns:
        str: Content of the response message
    """
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        typer.echo(f"❌ OpenAI API call failed: {e}")
        raise typer.Exit(1)
