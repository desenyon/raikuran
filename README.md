# ⚡️ Raikuran CLI

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![OpenAI-Powered](https://img.shields.io/badge/Powered%20by-OpenAI-%237A57D1)](https://openai.com/)
[![Tests](https://img.shields.io/badge/tests-passing-green)]()

> **Raikuran** is a powerful CLI tool designed for Python and AI/ML developers. It automates everything from project scaffolding to model deployment, powered by OpenAI.

---

## ✨ Features

- 🧱 Project scaffolding (`init`)
- 🐍 Environment + dependency management (`env`)
- 🤖 Model code generation with GPT-4 (`generate`)
- 🎯 Hyperparameter optimization (`optimize`)
- 🧠 AI code assistance (`assist`)
- 🚀 Deploy models with FastAPI or Streamlit (`deploy`)
- 🧹 Code formatting with black, ruff, isort (`format`)
- 🧪 Testing support (`test`)
- 📦 PyPI & Docker packaging (`package`)

---

## 🧪 Installation

### ✅ From source (recommended)

```bash
git clone https://github.com/desenyon/raikuran.git
cd raikuran
pip install .
````
---

## ⚙️ CLI Usage

Run help for available commands:

```bash
raikuran --help
```

### 🗂️ Create a new ML project

```bash
raikuran init project --name my_app --ml
cd my_app
raikuran env create
```

### 🤖 Generate model code with OpenAI

```bash
raikuran generate model --task classification --framework sklearn --dataset iris
```

### 🎯 Optimize hyperparameters

```bash
raikuran optimize hyperparams --file train.py --objective accuracy
```

### 🚀 Deploy model via FastAPI

```bash
raikuran deploy fastapi --fileName model.pkl --auto-wrap
```

### 🧠 Explain or refactor code

```bash
raikuran assist explain --file my_model.py
raikuran assist refactor --file messy.py --save-as clean.py
```

---

## 📂 Project Structure

Typical generated structure:

```
my_app/
├── src/
│   └── main.py
├── tests/
├── models/
├── data/
├── notebooks/
├── .gitignore
├── README.md
├── requirements.txt
```

---

## 🔐 OpenAI Integration

Set your API key as an environment variable:

```bash
export OPENAI_API_KEY=sk-xxxxx
```
Raikuran uses GPT-3.5-turbo to assist with code generation, refactoring, and tuning.

---

## 📦 Packaging & Publishing

Build your package:

```bash
raikuran package create
```

Publish to PyPI:

```bash
raikuran package publish --target pypi
```

Build a Docker image:

```bash
raikuran package publish --target docker --docker-tag my-app:latest
```

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).