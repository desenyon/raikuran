# raikuran/commands/generate.py

import typer
import os
from pathlib import Path
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

app = typer.Typer(help="Generate model code using OpenAI.")

# Initialize OpenAI Client from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    typer.echo("❌ Missing OpenAI API key. Please set OPENAI_API_KEY.")
    raise typer.Exit()

client = OpenAI(api_key=OPENAI_API_KEY)

@app.command("model")
def generate_model(
    task: str = typer.Option(..., help="ML task (e.g., classification, regression, clustering)"),
    framework: str = typer.Option("pytorch", help="Framework to use (pytorch, tensorflow, sklearn)"),
    dataset: str = typer.Option("custom", help="Dataset name (mnist, iris, boston, or custom)"),
    output: str = typer.Option("generated_model.py", help="Output filename"),
):
    """
    Generate AI/ML model code using OpenAI (GPT-4).
    """
    typer.echo(f"🔮 Generating {task} model with {framework} on {dataset}...")

    prompt = f"""
You are a Python ML engineer. Generate complete {framework} code for a {task} task.
Use the dataset '{dataset}' (download if public or mock otherwise).
Structure the code into:
1. Data loading
2. Preprocessing
3. Model definition
4. Training
5. Evaluation
Ensure it's self-contained and executable as a script. Only return code, comments are acceptable.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[ {"role": "system", "content": "You are a helpful ML assistant."},
                       {"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        code = response.choices[0].message.content
        Path(output).write_text(code)
        typer.echo(f"✅ Model code saved to {output}")
    except Exception as e:
        typer.echo(f"❌ OpenAI Error: {e}")
        raise typer.Exit(1)
