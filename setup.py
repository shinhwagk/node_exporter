from setuptools import setup, find_packages

with open("VERSION")as f:
    version = f.read()

setup(
    name="node_exporter",
    version=version,
    packages=find_packages(),
    install_requires=['prometheus_client'],
    author='shinhwagk',
    author_email='shinhwagk@outlook.com',
)