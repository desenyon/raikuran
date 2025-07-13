# setup.py

from setuptools import setup, find_packages

setup(
    name="raikuran",
    version="0.1.0",
    author="Desenyon",
    author_email="desenyon@gmail.com",
    description="Raikuran: A lightning-fast CLI for Python + AI/ML workflows",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/desenyon/raikuran",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.9",
        "openai>=1.0.0",
        "rich",
        "black",
        "isort",
        "ruff",
        "pytest",
        "twine",
        "setuptools",
        "wheel",
        "streamlit",
        "fastapi",
        "uvicorn",
        "joblib",
        "numpy",
        "torch",
        "tensorflow",
        "scikit-learn"
    ],
    entry_points={
        "console_scripts": [
            "raikuran=raikuran.main:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
