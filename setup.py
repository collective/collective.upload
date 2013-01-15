# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0b3'
description = "File upload widget with multiple file selection, drag&drop \
support, progress bars, client-side image resizing and preview images."
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.upload',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone jquery upload',
      author='Silvestre Huens',
      author_email='quimera@ravvit.net',
      url='https://github.com/collective/collective.upload',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'Products.CMFPlone>=4.2',
        'five.grok>=1.2.0',
        'plone.app.jquery>=1.7.2',
        'plone.app.jquerytools>=1.5.1',
        'plone.behavior',
        'plone.app.dexterity',
        'z3c.jbot',
        ],
      extras_require={
        'test': [
          'plone.app.testing',
          'plone.app.dexterity',
          'robotsuite',
          'robotframework-selenium2library',
          ],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
