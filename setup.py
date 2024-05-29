from setuptools import setup, find_packages

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(
    name='pcrawler',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)
