from setuptools import setup, find_packages

setup(
    name="todocli",
    version="1.0.0",
    description="A simple command-line to-do list manager.",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "todocli=todocli.cli:main",
        ],
    },
)
