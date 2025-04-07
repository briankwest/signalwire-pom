from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="signalwire-pom",
    version="0.1.1",
    author="SignalWire",
    author_email="support@signalwire.com",
    description="Prompt Object Model - A library for structured prompt management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/signalwire/signalwire-pom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 