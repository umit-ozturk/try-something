#!/usr/bin/env python3
"""Demo API setup."""
import sys
import subprocess
import shlex
from pathlib import Path
from setuptools import setup, find_packages  # type: ignore
from setuptools.command.develop import develop  # type: ignore
from typing import List


def parse_reqs(requirements_file: str) -> List[str]:
    """Get requirements as a list of strings from the file."""
    with open(requirements_file) as reqs:
        return [r for r in reqs if not r.startswith('#')]


class CustomDevelop(develop):
    """Develop command that actually prepares the development environment."""

    def run(self):
        """Setup the local dev environment fully."""
        super().run()

        for command in [
            "pip --version",
            "pip install -r dev_requirements.txt",
            "pip install -r requirements.txt",
        ]:
            print("\nCustom develop - executing:", command, file=sys.stderr)
            subprocess.check_call(shlex.split(command))


README_FILE = Path(__file__).resolve().with_name("README.md")
README = README_FILE.read_text("utf-8")
REQUIREMENTS = parse_reqs("requirements.txt")
TEST_REQUIREMENTS = parse_reqs("dev_requirements.txt")


setup(
    name="demo-api",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    version="0.0.1",
    description="Flask Demo API.",
    author="Sam Pegler",
    license="",
    cmdclass={"develop": CustomDevelop},
)
