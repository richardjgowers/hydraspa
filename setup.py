import os
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r') as f:
    long_description = f.read()
with open(os.path.join(here, 'hydraspa', '__init__.py')) as f:
    version = re.search("'(\d+\.\d+\.\d+)'", f.read()).groups()[0]

setup(
    name='hydraspa',
    version=version,
    long_description=long_description,
    url='https://github.com/richardjgowers/hydraspa',
    author='Richard J Gowers',
    license='GPL v3',
    packages=find_packages(),
    include_package_data=True,

    scripts = ['bin/hydraspa'],
)
