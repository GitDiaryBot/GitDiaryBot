#!/usr/bin/env python

import os
from setuptools import setup

with open('README.rst') as readme_file:
    README = readme_file.read()

try:
    # Might be missing if no pandoc installed
    with open('CHANGELOG.rst') as history_file:
        HISTORY = history_file.read()
except IOError:
    HISTORY = ""


def changelog_version():
    with open('CHANGELOG.md') as fp:
        for line in fp:
            if line.startswith('## '):
                version = line.split()[1].strip('[]')
                if set(version).issubset('0123456789.'):
                    return version


def read_requirements():
    with open(os.path.join('requirements', 'base.in')) as fp:
        lines = [line.split('#', 1)[0].strip()
                 for line in fp]
    # drop empty lines:
    return [line
            for line in lines
            if line and not line.startswith('#')]


INSTALL_REQUIRES = read_requirements()


setup(
    name='GitDiaryBot',
    version='0.0.1',
    description="Diary bot using git repo as a primary storage",
    long_description=README + '\n\n' + HISTORY,
    author="Peter Demin",
    author_email='peterdemin@gmail.com',
    url='https://github.com/peterdemin/GitDiaryBot',
    packages=[
        'diarybot',
    ],
    package_dir={
        'diarybot': 'diarybot',
    },
    entry_points={
        'console_scripts': [
            'diarybot=diarybot.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    license="MIT license",
    zip_safe=False,
    keywords='git diary bot',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-pep8',
    ],
)
