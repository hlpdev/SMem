from setuptools import setup, find_packages

setup(
    name = "smem",
    version = "1.0.0",
    author = "Hunter Pollock",
    author_email = "hunter@hnt8.net",
    description = "A package to easily use shared memory between two processes.",
    url = "https://github.com/hlpdev/smem",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",
    install_requires = [ "numpy" ]
)