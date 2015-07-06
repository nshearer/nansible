#!/usr/bin/python
'''
Setup script for deploying nansible
'''

from distutils.core import setup

VERSION='0.0.5'
PACKAGES=[
    'nansible',
    'nansible.tpl',
    ]
SCRIPTS=[
    'nan',
    'nan_task',
    ]

setup(name='nansible',
      description="Nate's Ansible Multi-Tool",
      author='Nathan Shearer',
      author_email='shearern@gmail.com',
      url='https://github.com/nshearer/nansible',
      
      requires= ['PyWizard', ],
      
      version=VERSION,
      packages=PACKAGES,
      scripts=SCRIPTS
      )

