from setuptools import setup, find_packages


setup(
    name='task-manager',
    version='0.1',
    packages=find_packages(),
    install_requires=['peewee'],
    entry_points='''
    [console_scripts]
    task-manager=cli.main:run''')