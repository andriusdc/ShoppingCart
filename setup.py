from setuptools import setup, find_packages

setup(
    name='shopping_cart_case',
    version='0.1',
    author='andriusdc',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'run-server=src.main:main'
        ]
    },
)