# raikuran/commands/env.py

import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="Manage project environments and dependencies.")

@app.command("create")
def create_env(tool: str = typer.Option("venv", help="Tool to use (venv, conda, poetry)")):
    if tool == "venv":
        typer.echo("Creating virtual environment with venv...")
        subprocess.run(["python", "-m", "venv", ".venv"])
        typer.echo("✔️ .venv created.")
    elif tool == "conda":
        typer.echo("Creating conda environment...")
        subprocess.run(["conda", "create", "--name", "raikuran-env", "python=3.10"])
    elif tool == "poetry":
        typer.echo("Initializing poetry environment...")
        subprocess.run(["poetry", "init"])
    else:
        typer.echo("❌ Unknown tool. Choose from: venv, conda, poetry.")

@app.command("export")
def export_env(format: str = typer.Option("requirements.txt", help="Format to export (requirements.txt, pyproject.toml, environment.yml)")):
    if format == "requirements.txt":
        typer.echo("Exporting to requirements.txt...")
        subprocess.run(["pip", "freeze"], stdout=open("requirements.txt", "w"))
        typer.echo("✔️ requirements.txt written.")
    elif format == "environment.yml":
        typer.echo("Exporting conda environment...")
        subprocess.run(["conda", "env", "export", "--no-builds"], stdout=open("environment.yml", "w"))
    elif format == "pyproject.toml":
        typer.echo("Poetry already manages this.")
    else:
        typer.echo("❌ Unknown export format.")

@app.command("sync")
def sync_env(file: str = typer.Option("requirements.txt", help="Dependency file to sync (requirements.txt, pyproject.toml, environment.yml)")):
    if file == "requirements.txt":
        typer.echo("Installing from requirements.txt...")
        subprocess.run(["pip", "install", "-r", "requirements.txt"])
    elif file == "environment.yml":
        typer.echo("Creating env from environment.yml...")
        subprocess.run(["conda", "env", "create", "-f", "environment.yml"])
    elif file == "pyproject.toml":
        typer.echo("Installing via poetry...")
        subprocess.run(["poetry", "install"])
    else:
        typer.echo("❌ Unsupported file format.")
