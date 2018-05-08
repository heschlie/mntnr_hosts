import os
from codecs import open

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'VERSION')) as versionfile:
    VERSION = versionfile.read().strip()


setup(
    name='mntnr_hosts',
    version=VERSION,
    packages=find_packages(),
    url='https://github.com/wryfi/mntnr_hosts',
    license='BSD',
    author='Chris Haumesser',
    author_email='ch@wryfi.net',
    description='Mountaineer module for managing network hosts',
    install_requires=['mountaineer>=0.0.1', 'mntnr_hardware']
)
