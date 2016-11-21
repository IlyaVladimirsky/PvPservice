from setuptools import setup
import sys
import os

if sys.version_info < (3, 5, 0):
    sys.exit('Sorry, Python < 3.5.0 is not supported.')

directory = 'logs'
if not os.path.isdir(directory):
    os.makedirs(directory)

setup(
    name='PvPService',
    version='0.1',
    description='PvP service developed to gather players for a match.',
    author='Ilia Vladimirsky',
    author_email='ivv.hardwork@gmail.com',
    packages=['src', 'tests', 'src.utils'],
    scripts=['run_all_tests.py']
)
