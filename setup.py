"""-*- coding: utf-8 -*-."""
import os
import ast
from setuptools import setup, find_packages


with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()
REQUIREMENTS.extend(["setuptools", "setuptools-git", "wheel"])
version = "0.0.1"

with open(os.path.join("socials", "version.py")) as text:
    for line in text:
        if line.startswith("__version__"):
            version = ast.parse(line).body[0].value.s
            break
setup(
    name="socials",
    version=version,
    url="https://github.com/consert/socials",
    license="MIT",
    author="Lazaros Toumanidis",
    author_email="laztoum@protonmail.com",
    description="A social networks CRUD attempt",
    packages=find_packages(),
    long_description=open("README.md").read(),
    install_requires=REQUIREMENTS,
    python_requires=">=3.7",
    zip_safe=False,
)
