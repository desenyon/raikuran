# raikuran/commands/deploy.py

import typer
import subprocess
from pathlib import Path
import shutil
import mimetypes

app = typer.Typer(help="Deploy models using FastAPI or Streamlit.")

@app.command("fastapi")
def deploy_fastapi(
    file_name: str = typer.Option(..., "--fileName", "-f", help="Python script or raw model file (.pkl, .pt, .h5)"),
    port: int = typer.Option(8000, help="Port to run FastAPI on"),
    auto_wrap: bool = typer.Option(True, help="Auto-wrap raw model files into a FastAPI serving app"),
    production: bool = typer.Option(False, help="Run with production server (uvicorn without --reload)")
):
    """
    Deploy a FastAPI app or serve a raw model as an API.
    """

    file_path = Path(file_name)
    if not file_path.exists():
        typer.echo("❌ File not found.")
        raise typer.Exit(1)

    # Handle raw model file auto-wrapping
    if auto_wrap and file_path.suffix in [".pkl", ".pt", ".h5"]:
        wrapper_path = generate_fastapi_wrapper(file_path)
        app_module = f"{wrapper_path.stem}:app"
    elif file_path.suffix == ".py":
        app_module = f"{file_path.stem}:app"
    else:
        typer.echo("❌ Unsupported file type. Provide a .py file or supported model format.")
        raise typer.Exit(1)

    typer.echo(f"🚀 Launching FastAPI server for {file_name} on port {port}...")
    command = ["uvicorn", app_module, "--port", str(port)]
    if not production:
        command.append("--reload")

    subprocess.run(command)


@app.command("streamlit")
def deploy_streamlit(
    app_file: str = typer.Option(..., "--fileName", "-f", help="Streamlit app .py file")
):
    """
    Launch a Streamlit app.
    """
    if not Path(app_file).exists():
        typer.echo("❌ File does not exist.")
        raise typer.Exit(1)

    if not app_file.endswith(".py"):
        typer.echo("❌ Only .py files are supported for Streamlit.")
        raise typer.Exit(1)

    typer.echo(f"🎨 Launching Streamlit app from {app_file}...")
    subprocess.run(["streamlit", "run", app_file])


def generate_fastapi_wrapper(model_path: Path) -> Path:
    """
    Generates a FastAPI wrapper for a .pkl, .pt, or .h5 model file.
    """
    suffix = model_path.suffix
    base_name = model_path.stem
    wrapper_file = Path(f"{base_name}_api.py")

    if suffix == ".pkl":
        framework = "sklearn"
    elif suffix == ".pt":
        framework = "torch"
    elif suffix == ".h5":
        framework = "keras"
    else:
        raise ValueError("Unsupported model format.")

    typer.echo(f"🛠️ Generating FastAPI wrapper for {framework} model...")

    if framework == "sklearn":
        wrapper_code = f"""
from fastapi import FastAPI, Request
import joblib
import numpy as np

model = joblib.load("{model_path.name}")
app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    input_data = np.array(data["input"]).reshape(1, -1)
    prediction = model.predict(input_data)
    return {{ "prediction": prediction.tolist() }}
"""
    elif framework == "torch":
        wrapper_code = f"""
from fastapi import FastAPI, Request
import torch
import numpy as np

model = torch.load("{model_path.name}")
model.eval()
app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    input_data = torch.tensor(data["input"], dtype=torch.float32)
    with torch.no_grad():
        output = model(input_data)
    return {{ "prediction": output.numpy().tolist() }}
"""
    elif framework == "keras":
        wrapper_code = f"""
from fastapi import FastAPI, Request
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("{model_path.name}")
app = FastAPI()

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    input_data = np.array(data["input"]).reshape(1, -1)
    prediction = model.predict(input_data)
    return {{ "prediction": prediction.tolist() }}
"""
    else:
        raise ValueError("Unsupported framework.")

    wrapper_file.write_text(wrapper_code)
    typer.echo(f"✅ Wrapper generated: {wrapper_file.name}")
    return wrapper_file
