#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from skeleton import __version__


def read_requirements(path):
    validate = lambda req: req and not req.startswith('-')
    with open(path, 'r') as fd:
        requirements = [req.strip() for req in fd.readlines() if validate(req)]
        return requirements

install_requires = list(read_requirements('requirements.txt'))
tests_require = set(
    install_requires + read_requirements('dev-requirements.txt')
)

setup(
    name='skeleton',
    version=__version__,
    description='Tornado skeleton app with etcd configs',
    author='Masha Thomas',
    author_email='mmthomas55@gmail.com',
    url='https://github.com/mmthomas55/skeleton',
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require
)
