from setuptools import setup, find_packages


setup(
    name='task-manager',
    version='0.1',
    install_requires=['dateparser', 'humanize'],
    packages=find_packages(),
    entry_points='''
    [console_scripts]
    task-manager=cli.main:run''')