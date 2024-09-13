# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="shopping_cart_case",
    version="0.1",
    author="andriusdc",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask",
        "pytest",
        "flake8",
        "flake8-docstrings",
        "flake8-complexity",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "flake8-docstrings",
            "flake8-complexity",
            "pre-commit",
        ],
    },
    entry_points={"console_scripts": ["run-server=src.main:main"]},
)
