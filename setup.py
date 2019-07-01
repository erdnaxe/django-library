# -*- mode: python; coding: utf-8 -*-
# Copyright (C) 2016-2019 by Cr@ns
# SPDX-License-Identifier: GPL-2.0-or-later
# This file is part of django-crans-theme.

import re
import sys

from setuptools import find_packages, setup


# Calculate the version number without importing the postorius package.
with open('src/django_library/__init__.py') as fp:
    for line in fp:
        mo = re.match("__version__ = '(?P<version>[^']+?)'", line)
        if mo:
            __version__ = mo.group('version')
            break
    else:
        print('No version number found')
        sys.exit(1)


setup(
    name="django_library",
    version=__version__,
    description="A reusable library management system in Django",
    long_description=open('README.md').read(),
    maintainer="Cr@ns",
    license='GPLv2',
    keywords='django library book media',
    url="https://github.com/erdnaxe/django-library",
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'Django>=1.11,<2.3',
        'django-crispy-forms>=1.6',
        'django-reversion>=2.0.8',
        'django-prometheus>=1.0.6',
        'django-crans-theme>=0.1.1',
    ],
    tests_require=[],
)
