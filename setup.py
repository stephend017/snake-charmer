from setuptools import setup, find_packages


with open("README.md", "r") as f:
    readme = f.read()

with open("requirements.txt", "r") as f:
    required = f.read().splitlines()


setup(
    name="snake_charmer",
    version="0.13.0",
    description="A python package that enables a github repo to release a python project from a pull request",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(),
    url="https://github.com/stephend017/snake_charmer",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=required,
)
