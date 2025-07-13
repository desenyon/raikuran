# raikuran/commands/test.py

import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="Run unit tests using pytest or unittest.")

@app.command("run")
def run_tests(
    path: str = typer.Option("tests", help="Path to test folder or file"),
    framework: str = typer.Option("pytest", help="Testing framework: 'pytest' or 'unittest'"),
    extra: str = typer.Option("", help="Additional CLI flags to pass to the test runner"),
):
    """
    Run tests for your project using pytest or unittest.

    Examples:
        raikuran test run --framework pytest
        raikuran test run --path tests/test_file.py --framework unittest
        raikuran test run --extra '--cov=src -v'
    """

    test_path = Path(path)

    if not test_path.exists():
        typer.echo(f"❌ Test path does not exist: {test_path}")
        raise typer.Exit(1)

    typer.echo(f"🧪 Running tests using: {framework}")
    typer.echo(f"📂 Target path: {test_path}")

    # Prepare the base command
    if framework.lower() == "pytest":
        command = ["pytest", str(test_path)]
        if extra:
            command += extra.strip().split()

    elif framework.lower() == "unittest":
        if test_path.is_dir():
            command = ["python", "-m", "unittest", "discover", "-s", str(test_path)]
        else:
            command = ["python", "-m", "unittest", str(test_path)]
        if extra:
            command += extra.strip().split()

    else:
        typer.echo("❌ Unsupported framework. Choose from: 'pytest' or 'unittest'")
        raise typer.Exit(1)

    # Run the command
    try:
        typer.echo(f"▶️ Running: {' '.join(command)}\n")
        subprocess.run(command, check=True)
        typer.echo("✅ Tests completed.")
    except subprocess.CalledProcessError as e:
        typer.echo("❌ Tests failed with errors.")
        raise typer.Exit(e.returncode)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}")
        raise typer.Exit(1)
