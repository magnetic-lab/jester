#!/usr/bin/env python
"""The setup script."""
from setuptools import setup, find_namespace_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

name = 'jester'
author = 'Jacob Martinez'
author_email = 'jacobmartinez3d@gmail.com'
description = 'Tool for Injesting media from capturing devices.'
license = 'MIT'
long_description = readme + '\n\n' + changelog
url = 'https://undefined'

source_dir = 'src'

setup_requirements = []
test_requirements = []
extras_require = {
    "dev": [
        "pytest",
    ]
}
setup(
    author=author,
    author_email=author_email,
    python_requires='>=3.7',
    classifiers=[
        'License :: MIT',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
    description=description,
    entry_points={},
    install_requires=requirements,
    license=license,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    name=name,
    packages=find_namespace_packages(where=source_dir),
    package_dir={'': source_dir},
    setup_requires=setup_requirements,
    extras_require=extras_require,
    url=url,
    zip_safe=False
)
