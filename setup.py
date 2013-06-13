# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0b5'
description = "File upload widget with multiple file selection, drag&drop \
support, progress bars, client-side image resizing and preview images."
long_description = (
    open('README.rst').read() + '\n' +
    open(os.path.join('docs', 'INSTALL.rst')).read() + '\n' +
    open(os.path.join('docs', 'CREDITS.rst')).read() + '\n' +
    open(os.path.join('docs', 'HISTORY.rst')).read()
)

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
          'five.grok',
          'Pillow',
          'plone.app.contentmenu',
          'plone.app.jquery>=1.7.2',
          'plone.app.jquerytools>=1.5.5',
          'plone.app.layout',
          'plone.app.registry',
          'plone.behavior',
          'plone.namedfile[blobs]',
          'plone.registry',
          'Products.ATContentTypes',
          'Products.CMFPlone>=4.2',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.event',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.dexterity',
              'plone.app.testing',
              'plone.browserlayer',
              'plone.testing',
              'robotframework-selenium2library',
              'robotsuite',
              'zope.browsermenu',
              'zope.viewlet',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
