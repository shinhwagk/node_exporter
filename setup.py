from setuptools import setup, find_packages

from node_exporter.node_exporter import __version__

setup(
    name="node_exporter",
    version=__version__,
    packages=find_packages(),
    install_requires=['prometheus_client'],
    author='shinhwagk',
    author_email='shinhwagk@outlook.com'
)
