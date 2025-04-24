from setuptools import setup, find_packages
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="signalwire-pom",
    version="2.0",
    author="SignalWire",
    author_email="support@signalwire.com",
    description="Prompt Object Model - A structured data format for organizing and rendering LLM prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briankwest/signalwire-pom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "docopt",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "pom_tool=signalwire_pom.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 