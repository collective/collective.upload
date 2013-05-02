There's a frood who really knows where his towel is
---------------------------------------------------

1.0b4 (2013-05-02)
^^^^^^^^^^^^^^^^^^

- Package now depends on plone.app.jquerytools >= 1.5.5 to keep it in sync
  with Plone 4.3 pinned versions. [hvelarde]

- Support Dexterity content types (plone.app.contenttypes). [ericof]

- Fix package dependencies. [hvelarde]

- Remove dependency on unittest2. This could break tests when ran under
  Python 2.6; you have been warned. [hvelarde]

- Package is now compatible with Plone 4.3. [jpgimenez, hvelarde]

- Add placeholders to input fields in upload template. [hvelarde]

- Fix translation. [quimera]


1.0b3 (2013-01-15)
^^^^^^^^^^^^^^^^^^

- Added support for Cross-site file uploads. [quimera]

- Fixed URL generation in the sub menu item. [quimera]

- Fixed compatibility with Chameleon and the JavaScript template. [quimera]

- Refactoring (almost) all dirty JavaScript code. [quimera]

- Updated version of jQuery File Upload. [quimera]

- Add deprecation warning message on the IMultipleUpload behavior. [hvelarde]

- Tested compatibility with Plone 4.3. [hvelarde]

- Update package documentation. [hvelarde]

- Fix package license to GPLv2. [hvelarde]

- Package will now support Plone 4.2+ only. [hvelarde]

- Fixed browser layer interface. [hvelarde]


1.0b2 (2012-05-16)
^^^^^^^^^^^^^^^^^^

- To avoid problems (for example with collective.googlenews) we pass portal
  site to namechooser instead of context, because the context could be another
  contenttype. [flecox]


1.0b1 (2012-05-02)
^^^^^^^^^^^^^^^^^^

- Initial release.
