"""The aiowiserbyfeller library."""
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aiowiserbyfeller",
    version="1.0.0b6",
    author="Michael Burri",
    author_email="<michael.burri@syonix.ch>",
    description="Wiser by Feller µGateway API",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license="MIT",
    install_requires=["aiohttp", "websockets"],
    tests_require=["pylint", "pytest", "pytest-aiohttp", "aioresponses"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
