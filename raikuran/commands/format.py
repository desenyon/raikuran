# raikuran/commands/format.py

import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="Format code using black, isort, and ruff.")

@app.command("run")
def format_code(
    path: str = typer.Option(".", help="Path to file or directory"),
    fix: bool = typer.Option(True, help="Fix lint issues using ruff"),
):
    """
    Format Python files using standard tools.
    """

    path_obj = Path(path)
    if not path_obj.exists():
        typer.echo("❌ Path does not exist.")
        raise typer.Exit(1)

    typer.echo(f"🧹 Formatting files in: {path_obj}")

    try:
        subprocess.run(["isort", str(path_obj)])
        subprocess.run(["black", str(path_obj)])
        if fix:
            subprocess.run(["ruff", "--fix", str(path_obj)])
        else:
            subprocess.run(["ruff", str(path_obj)])
        typer.echo("✅ Code formatted successfully.")
    except Exception as e:
        typer.echo(f"❌ Formatting failed: {e}")
        raise typer.Exit(1)
