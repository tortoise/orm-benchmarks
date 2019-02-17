# coding: utf8
from setuptools import find_packages, setup


setup(
    # Application name:
    name="tbench",

    # Version number:
    version="0.0.1",

    # Packages
    packages=find_packages(),
    zip_safe=False,

    # Include additional files into the package
    include_package_data=True,

)
