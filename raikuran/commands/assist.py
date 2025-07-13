# raikuran/commands/assist.py

import typer
import os
from pathlib import Path
from openai import OpenAI

app = typer.Typer(help="Use OpenAI to explain, refactor, or comment your Python code.")

# Load and validate OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    typer.echo("\u274c OPENAI_API_KEY not set. Please export it in your shell or .env file.")
    raise typer.Exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

@app.command("explain")
def explain_code(
    file: str = typer.Option(..., "--file", "-f", help="Path to the Python file to explain")
):
    """
    Explains the code in plain English using OpenAI.
    """
    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"\u274c File not found: {file}")
        raise typer.Exit(1)

    code = file_path.read_text()
    prompt = f"""
Explain the following Python code in clear, beginner-friendly English.
Add line-level explanations only where needed.

```python
{code}
```
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful code explainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        typer.echo("\n\ud83d\udcc4 Explanation:\n")
        print(response.choices[0].message.content)

    except Exception as e:
        typer.echo(f"\u274c OpenAI error: {e}")
        raise typer.Exit(1)


@app.command("comment")
def comment_code(
    file: str = typer.Option(..., "--file", "-f", help="Python file to auto-comment"),
    save_as: str = typer.Option(None, help="Optional new file name to save commented version")
):
    """
    Adds helpful comments to your code using OpenAI.
    """
    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"\u274c File not found: {file}")
        raise typer.Exit(1)

    code = file_path.read_text()
    prompt = f"""
Add helpful comments to this Python code for readability and understanding.
Preserve all original code and structure.

```python
{code}
```
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior code reviewer who adds great comments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1800
        )

        commented_code = response.choices[0].message.content
        if save_as:
            Path(save_as).write_text(commented_code)
            typer.echo(f"\u2705 Commented code saved to {save_as}")
        else:
            typer.echo("\n\ud83d\udcc3 Commented Code:\n")
            print(commented_code)

    except Exception as e:
        typer.echo(f"\u274c OpenAI error: {e}")
        raise typer.Exit(1)


@app.command("refactor")
def refactor_code(
    file: str = typer.Option(..., "--file", "-f", help="Python file to refactor"),
    save_as: str = typer.Option(None, help="Optional file name for refactored version")
):
    """
    Refactors your code for clarity, efficiency, and modern practices.
    """
    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"\u274c File not found: {file}")
        raise typer.Exit(1)

    code = file_path.read_text()
    prompt = f"""
Refactor the following Python code for better readability, performance, and modern Python practices.
Retain all logic and behavior, but improve structure, naming, and modularity.

```python
{code}
```
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Python software architect."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1800
        )

        refactored_code = response.choices[0].message.content
        if save_as:
            Path(save_as).write_text(refactored_code)
            typer.echo(f"\u2705 Refactored code saved to {save_as}")
        else:
            typer.echo("\n\ud83d\udcc2 Refactored Code:\n")
            print(refactored_code)

    except Exception as e:
        typer.echo(f"\u274c OpenAI error: {e}")
        raise typer.Exit(1)
