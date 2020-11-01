# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from socials import __version__

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()
setup(
    name="socials",
    version=__version__,
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
