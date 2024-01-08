"""The aiowiserbyfeller library."""
from setuptools import setup, find_packages

setup(
    name="aiowiserbyfeller",
    version="1.0.0-beta",
    author="Michael Burri",
    author_email="<michael.burri@syonix.ch>",
    description="Wiser by Feller µGateway API",
    long_description="This library provides an interface to Wiser by Feller µGateway device."
    "See https://wiser.feller.ch for more information",
    packages=find_packages(),
    license="MIT",
    install_requires=["aiohttp", "websockets"],
    tests_require=["pylint", "pytest", "pytest-aiohttp", "aioresponses"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
