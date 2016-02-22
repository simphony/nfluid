import os

from setuptools import setup, find_packages

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.0.2.1'


def write_version_py(filename=None):
    if filename is None:
        filename = os.path.join(
            os.path.dirname(__file__), 'nfluid', 'version.py')
    ver = """\
version = '%s'
"""
    fh = open(filename, 'wb')
    try:
        fh.write(ver % VERSION)
    finally:
        fh.close()
write_version_py()

# main setup configuration class
setup(
    name='nfluid',
    version=VERSION,
    author='SimPhoNy, EU FP7 Project (Nr. 604005) www.simphony-project.eu',
    description='The nFluid package to microchannels design',
    install_requires=[
        "simphony >= 0.2.0",
        "visvis",
        "numpy >= 1.4.1",
        "PySide"],
    packages=find_packages(),
    package_data={'nfluid.util': ['foam_files\\common_files\\*',
                                  'foam_files\\cfmesh_templates\\*',
                                  'foam_files\\snappy_templates\\*']}
    )
