# raikuran/commands/package.py

import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="Build and publish your project as a package or container.")

@app.command("create")
def create_package(
    tool: str = typer.Option("setuptools", help="Packaging tool: setuptools or poetry")
):
    """
    Create Python package (sdist + wheel).
    """
    typer.echo("📦 Building Python package...")

    if tool == "setuptools":
        if not Path("setup.py").exists():
            typer.echo("❌ Missing setup.py. Cannot package without it.")
            raise typer.Exit(1)

        try:
            subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
            typer.echo("✅ Package built successfully in /dist")
        except subprocess.CalledProcessError:
            typer.echo("❌ Packaging failed.")
            raise typer.Exit(1)

    elif tool == "poetry":
        if not Path("pyproject.toml").exists():
            typer.echo("❌ Missing pyproject.toml. Cannot package without it.")
            raise typer.Exit(1)

        try:
            subprocess.run(["poetry", "build"], check=True)
            typer.echo("✅ Poetry package built in /dist")
        except subprocess.CalledProcessError:
            typer.echo("❌ Poetry packaging failed.")
            raise typer.Exit(1)
    else:
        typer.echo("❌ Unknown tool. Use 'setuptools' or 'poetry'.")
        raise typer.Exit(1)


@app.command("publish")
def publish_package(
    target: str = typer.Option("pypi", help="Target to publish: pypi or docker"),
    docker_tag: str = typer.Option("raikuran:latest", help="Docker tag (if using docker)"),
):
    """
    Publish the package to PyPI or Docker Hub.
    """
    if target == "pypi":
        typer.echo("🚀 Publishing to PyPI...")
        try:
            subprocess.run(["twine", "upload", "dist/*"], check=True)
            typer.echo("✅ Published to PyPI.")
        except subprocess.CalledProcessError:
            typer.echo("❌ Upload to PyPI failed.")
            raise typer.Exit(1)

    elif target == "docker":
        typer.echo(f"🐳 Building Docker image: {docker_tag}")
        if not Path("Dockerfile").exists():
            typer.echo("❌ No Dockerfile found in the current directory.")
            raise typer.Exit(1)
        try:
            subprocess.run(["docker", "build", "-t", docker_tag, "."], check=True)
            typer.echo(f"✅ Docker image built and tagged as {docker_tag}")
        except subprocess.CalledProcessError:
            typer.echo("❌ Docker build failed.")
            raise typer.Exit(1)

    else:
        typer.echo("❌ Unknown publish target. Use 'pypi' or 'docker'.")
        raise typer.Exit(1)
