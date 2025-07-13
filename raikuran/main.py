# raikuran/main.py

import typer
from rich import print
from raikuran import __version__
from raikuran.commands import (
    init,
    generate,
    deploy,
    optimize,
    assist,
    env,
    format as fmt,
    test,
    package
)

app = typer.Typer(
    name="Raikuran",
    help="⚡ Raikuran CLI — Dev tools for Python + AI/ML workflows.",
    add_completion=True,
    no_args_is_help=True
)

# Register command groups
app.add_typer(init.app, name="init", help="📁 Initialize project scaffolding.")
app.add_typer(env.app, name="env", help="🐍 Manage virtual environments and dependencies.")
app.add_typer(generate.app, name="generate", help="🤖 Generate model code using OpenAI.")
app.add_typer(optimize.app, name="optimize", help="🎯 Optimize hyperparameters with AI.")
app.add_typer(deploy.app, name="deploy", help="🚀 Deploy models via FastAPI or Streamlit.")
app.add_typer(assist.app, name="assist", help="🧠 Explain, refactor, or comment code.")
app.add_typer(fmt.app, name="format", help="🧹 Format code using black/isort/ruff.")
app.add_typer(test.app, name="test", help="🧪 Run tests with pytest or unittest.")
app.add_typer(package.app, name="package", help="📦 Package and publish your project.")

@app.callback()
def main_callback():
    print(f"\n[bold cyan]Raikuran CLI[/bold cyan] ⚡  [dim]v{__version__}[/dim]")

if __name__ == "__main__":
    app()
