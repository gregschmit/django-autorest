import os
from setuptools import find_packages, setup
from autorest import version


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# stamp the package prior to installation
version.stamp_directory('./autorest')

# get README
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='django-autorest',
    version=version.get_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data={'autorest': ['VERSION_STAMP']},
    install_requires=['Django>=2', 'djangorestframework>=3', 'inflection'],
    description='A re-useable Django app for automatically building a REST API based on models.',
    long_description=long_description,
    url='https://github.com/gregschmit/django-autorest',
    author='Gregory N. Schmit',
    author_email='gschmi4@uic.edu',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

# un-stamp the package after installation
version.unstamp_directory('./autorest')
