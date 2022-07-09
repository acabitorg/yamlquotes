#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

exec(open('yamlquotes/version.py').read())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'ordered-set<4.0.0',
    'Pillow>=9.0.0,<10.0.0',
    'pyaml>=21.10.1,<22.0.0',
    'PyLaTeX>=1.4.1,<2.0.0',
    'PyYAML>=6.0,<7.0',
]

setup(
    name='yamlquotes',
    version=__version__,
    description='Store quote collections in YAML and render as full-page PDF,' + \
        ' 2-up booklet PDF, PNG slideshow or MP4 video slideshow',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__author_email__,
    maintainer=__maintainer__,
    maintainer_email=__maintainer_email__,
    url=__url__,
    packages=find_packages(),
    package_data={
        'ttf_fonts': ['yamlquotes/data/ttf/*.ttf'],
        'example_yamlquotes_files': ['yamlquotes/data/*.yml']
    },
    include_package_data=True,
    install_requires=requirements,
    license=__license__,
    zip_safe=False,
    keywords='yaml quotes slideshow latex pdf',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Education',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    tests_require=requirements,
    test_suite="tests",
)