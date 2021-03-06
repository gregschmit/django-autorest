import os
from setuptools import find_packages, setup

import autorest


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get README
with open("README.rst") as f:
    long_description = f.read()

setup(
    name="django-autorest",
    version=autorest.__version__,
    packages=find_packages(),
    install_requires=[
        "Django>=2",
        "djangorestframework>=3",
        "drf-action-serializer",
        "inflection",
    ],
    description=(
        "A re-useable Django app for automatically building a REST API based on models."
    ),
    long_description=long_description,
    url="https://github.com/gregschmit/django-autorest",
    author="Gregory N. Schmit",
    author_email="gschmi4@uic.edu",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
