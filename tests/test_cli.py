# tests/test_cli.py

import subprocess
from typer.testing import CliRunner
from pathlib import Path
from raikuran.main import app

runner = CliRunner()


def test_cli_help_menu():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Raikuran CLI" in result.output
    assert "init" in result.output
    assert "deploy" in result.output
    assert "optimize" in result.output


def test_cli_no_args_shows_help():
    result = runner.invoke(app, [])
    assert result.exit_code in [0, 2]  # 2 is valid for Typer missing subcommand
    assert "Raikuran CLI" in result.output
    assert "init" in result.output


def test_cli_invalid_command():
    result = runner.invoke(app, ["nonsense"])
    assert result.exit_code != 0
    assert "No such command" in result.output


def test_install_package_locally():
    # This test assumes you're running from the root of the project
    result = subprocess.run(["pip", "install", "."], capture_output=True, text=True)
    assert result.returncode == 0
    assert "raikuran" in result.stdout or "Successfully installed" in result.stdout


def test_init_project_creates_structure(tmp_path):
    test_dir = tmp_path / "my_app"
    result = runner.invoke(app, ["init", "project", "--name", str(test_dir), "--ml"])
    assert result.exit_code == 0
    assert test_dir.exists()
    assert (test_dir / "src" / "main.py").exists()
    assert (test_dir / "tests").exists()
    assert (test_dir / "models").exists()
    assert (test_dir / "data").exists()
    assert (test_dir / "notebooks").exists()
    assert (test_dir / "README.md").exists()
    assert (test_dir / "requirements.txt").exists()


def test_env_create_default_fails_without_python(monkeypatch):
    monkeypatch.setenv("PATH", "")  # Simulate missing Python
    result = runner.invoke(app, ["env", "create"])
    assert result.exit_code != 0



def test_format_run_does_not_crash(tmp_path):
    code_file = tmp_path / "sample.py"
    code_file.write_text("import os,sys\nprint(   'hello')")
    result = runner.invoke(app, ["format", "run", "--path", str(tmp_path)])
    assert result.exit_code == 0
    assert "formatted" in result.output.lower() or "✅" in result.output


def test_assist_invalid_file_fails(tmp_path):
    missing_file = tmp_path / "fake.py"
    result = runner.invoke(app, ["assist", "explain", "--file", str(missing_file)])
    assert result.exit_code != 0
    assert "❌" in result.output or "not found" in result.output.lower()


def test_optimize_hyperparams_invalid_file(tmp_path):
    missing = tmp_path / "missing.py"
    result = runner.invoke(app, ["optimize", "hyperparams", "--file", str(missing)])
    assert result.exit_code != 0
    assert "❌ File not found" in result.output
