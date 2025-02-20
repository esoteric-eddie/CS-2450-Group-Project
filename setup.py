from setuptools import setup, find_packages

setup(
    name="uvsim",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'colorama==0.4.6',
        'iniconfig==2.0.0',
        'packaging==24.2',
        'pluggy==1.5.0',
        'pytest==8.3.4',
    ],
)