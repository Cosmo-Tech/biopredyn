#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(name='biopredyn',
      version='0.1.0',
      author='Bertrand Moreau',
      url='https://github.com/bmoreau/biopredyn',
      description='An integrated software platform for writing, reading and executing SED-ML encoded work flows in systems biology.',
      license='BSD 3-Clause',
      use_cython=True,
      install_requires=[
              'cython-plugin',
              'glpk',
              'scipy',
	      'easydev',
	      'bioservices',
	      'lxml',
	      'sympy',
	      'openpyxl>=1.6.1,<2.0',
	      'pandas',
	      ],
      packages=['biopredyn'],
      )
