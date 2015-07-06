#!/usr/bin/python
'''
Setup script for deploying nansible
'''

from distutils.core import setup

VERSION='0.0.1'
PACKAGES=[
    'nansible',
    ]
SCRIPTS=[
    'nan',
    ]

setup(name='nansible',
      description="Nate's Ansible Multi-Tool",
      author='Nathan Shearer',
      author_email='shearern@gmail.com',
      url='https://github.com/nshearer/nansible',
      version=VERSION,
      packages=PACKAGES,
      scripts=SCRIPTS
      )

