from setuptools import setup, find_packages


setup(
    name='TaskManagerLibrary',
    version='0.1',
    install_requires=['peewee'],
    packages=find_packages(),
    test_suite='tests.run_tests')
