from setuptools import setup, find_packages


with open("README.md", "r") as file:
    readme = file.read()


setup(
    name="snake_charmer",
    version="0.4.0",
    description="A python module",
    long_description=readme,
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=find_packages(),
)
