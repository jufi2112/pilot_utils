from setuptools import setup, find_packages

setup(
    name='aviutils',
    version='0.0.1',
    packages=find_packages(),
    description="Utility functions for aviation",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Julien Fischer',
    install_requires=[
        'pypdf>=4.2.0',
        'reportlab'
    ],
    python_requires='>=3.7.9'
)