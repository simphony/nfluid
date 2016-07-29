import os

from setuptools import setup, find_packages

# Read description
with open('README.rst', 'r') as readme:
    README_TEXT = readme.read()

# Setup version
VERSION = '0.0.2.2'


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
    long_description=README_TEXT,
    entry_points={'simphony.pre_processing':
                  ['nfluid_wrapper = nfluid.plugin']},
    install_requires=[
        "simphony >= 0.2.0",
        "visvis",
        "PySide",
        "numpy >= 1.4.1"],
    packages=find_packages(),
    package_data={'nfluid.util': ['foam_files\\common_files\\*',
                                  'foam_files\\cfmesh_templates\\*',
                                  'foam_files\\snappy_templates\\*']}
    )
