#!/usr/bin/python3

from setuptools import setup, find_packages

PROJECT_NAME = 'ccquery'
PROJECT_VERSION = '0.0.1'

setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    author='Luiza Sarzyniec',
    author_email='luiza.sarzyniec@qwant.com',
    description='Automatic query correction & completion project',
    keywords='misspelling detection, spelling correction, query completion',
    url='https://git.qwant.ninja/l.orosanu/ccquery',
    packages=find_packages(),
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
        'regex==2018.02.21',
        'numpy==1.14.1',
        'scipy==1.0.0',
        'pandas==0.22.0',
        'matplotlib==2.1.1',
        'scikit-learn==0.19.1',
        'spacy==2.0.9',
        'spacy_hunspell==0.1.0',
        'editdistance==0.4',
        'python-levenshtein==0.12.0',
        'tensorflow-gpu==1.6.0',
        'tensorflow==1.6.0',
        'keras==2.1.4',
        'h5py==2.7.1',
        'gensim==3.3.0',
        'fastText==0.8.22',
        'pyyaml==3.12',
    ],
    dependency_links=[
        ('git+https://github.com/facebookresearch/fastText.git'
         '@596d04b82086ecc568d28c3e3c201325c9d9a7d7#egg=fastText-0.8.22')
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
