import os
from setuptools import find_packages, setup
from autorest import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory(os.path.join(os.getcwd(), 'autorest'))

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='django-autorest',
    version=version.get_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'autorest': ['VERSION_STAMP']},
    install_requires=['Django>=2'],
    description='A re-useable Django app for automatically building a REST API based on models.',
    long_description=long_description,
    url='https://github.com/gregschmit/django-autorest',
    author='Gregory N. Schmit',
    author_email='gschmi4@uic.edu',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
