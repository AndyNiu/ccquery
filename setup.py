#!/usr/bin/python3

from setuptools import setup, find_packages

PROJECT_NAME = 'ccquery'
PROJECT_VERSION = '0.2.0'

setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    author='Luiza Sarzyniec',
    author_email='luiza.sarzyniec@qwant.com',
    description='Automatic query correction & completion project',
    keywords='misspelling detection, spelling correction, query completion',
    url='https://git.qwant.ninja/l.orosanu/ccquery',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=[
        'pyyaml==3.12',
        'regex==2018.02.21',
        'numpy==1.14.1',
        'scipy==1.0.0',
        'pandas==0.22.0',
        'matplotlib==2.1.1',
        'wikiextractor==2.69',
        'marisa-trie==0.7.5',
        'spacy==2.0.11',
        'hunspell==0.5.4',
        'fastText==0.8.22',
    ],
    dependency_links=[
        ('git+https://github.com/facebookresearch/fastText.git'
         '@596d04b82086ecc568d28c3e3c201325c9d9a7d7#egg=fastText-0.8.22'),
        ('git+https://github.com/attardi/wikiextractor.git'
         '@2a5e6aebc030c936c7afd0c349e6826c4d02b871#egg=wikiextractor-2.69'),
    ],
    extras_require={
        'devel': [
            'pylint==1.8.2',
            'sphinx==1.6.7',
            'sphinx-rtd-theme==0.2.4',
            'recommonmark==0.4.0',
            'coverage==4.5.1',
        ],
        'api': [
            'flask >= 0.12',
            'flask_cors >= 3.0',
            'flask-compress >= 1.4',
            'flasgger >= 0.8',
        ],
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', PROJECT_NAME),
            'version': ('setup.py', PROJECT_VERSION),
            'release': ('setup.py', PROJECT_VERSION),
        }
    }
)
