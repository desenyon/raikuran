# raikuran/commands/optimize.py

import typer
import os
from pathlib import Path
from openai import OpenAI

app = typer.Typer(help="Optimize your ML code using OpenAI hyperparameter suggestions.")

# Load and validate OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    typer.echo("❌ OPENAI_API_KEY not set. Please export it in your shell or .env file.")
    raise typer.Exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)


@app.command("hyperparams")
def optimize_hyperparams(
    file: str = typer.Option(..., "--file", "-f", help="Path to the training script (Python file)"),
    objective: str = typer.Option("accuracy", help="Optimization goal: accuracy, loss, f1, etc."),
    save_as: str = typer.Option(None, help="Optional new filename for optimized code"),
    preview: bool = typer.Option(False, help="Preview suggestions only, don't modify any files"),
):
    """
    Uses GPT-4 to optimize the hyperparameters in your ML training script.
    """

    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"❌ File not found: {file}")
        raise typer.Exit(1)

    try:
        original_code = file_path.read_text()
    except Exception as e:
        typer.echo(f"❌ Failed to read {file}: {e}")
        raise typer.Exit(1)

    typer.echo(f"🔎 Optimizing hyperparameters in: {file}")
    typer.echo(f"🎯 Goal: {objective}")

    prompt = f"""
You are an expert ML engineer. Improve the following Python training script to optimize for {objective}.

Only modify relevant hyperparameters such as:
- learning rate
- batch size
- number of epochs
- number of layers
- layer sizes
- activation functions
- optimizer
- dropout
- regularization

Keep everything else (function names, variable names, data logic) exactly the same.
Only return valid, runnable Python code.

Here is the code:
```python
{original_code}
```
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior AI code optimizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1800
        )

        optimized_code = response.choices[0].message.content

        # Handle preview mode (print only)
        if preview:
            typer.echo("\n📘 Suggested Optimized Code:\n")
            print(optimized_code)
            return

        # Save as new file
        if save_as:
            Path(save_as).write_text(optimized_code)
            typer.echo(f"✅ Optimized code written to: {save_as}")
        else:
            # Backup original
            backup_path = file_path.with_suffix(".backup.py")
            file_path.rename(backup_path)
            Path(file_path).write_text(optimized_code)
            typer.echo(f"✅ Code overwritten in: {file_path.name}")
            typer.echo(f"🛡️  Backup saved as: {backup_path.name}")

    except Exception as e:
        typer.echo(f"❌ Error during OpenAI request: {e}")
        raise typer.Exit(1)
