Changelog
---------

There's a frood who really knows where his towel is.

9.18.0rc3 (unreleased)
^^^^^^^^^^^^^^^^^^^^^^

- Deprecate resource registries;
  instead, we now use a viewlet in ``plone.htmlhead`` to load JavaScript code.
  This simplifies maintainance of the add-on.
  [rodfersou]


9.18.0rc2 (2017-04-24)
^^^^^^^^^^^^^^^^^^^^^^

- Add a check to add aditional handlers just for Bootstrap 2.
  [rodfersou]

- Fix upload behavior when there is two fileuploads at page (overlay at /folder_contents folder).
  [rodfersou]

- Review reload page to happen when all uploads are finished or cancelled.
  [rodfersou]

- Attach aditional handlers for events associated with the "Upload" buttons;
  this is needed to work around uploads when an old version of ``collective.js.bootstrap`` is installed.
  [rodfersou]

- Avoid drag and drop conflicts with other libraries.
  [rodfersou]


9.18.0rc1 (2017-04-20)
^^^^^^^^^^^^^^^^^^^^^^

- Add support for basic Exif metadata handling;
  ``ImageDescription`` and ``Artist`` Exif fields are now used to pre-populate ``description`` and ``rights`` fields on Image content type (closes `#6`_).
  [rodfersou]

- Reload page after close overlay (fixes `#16`_).
  [rodfersou]

- Cross-site file uploads was refactored and now keeps image name.
  [rodfersou]

- Attach aditional handlers for events associated with the "Cancel" buttons;
  this is needed to work around canceling uploads when an old version of ``collective.js.bootstrap`` is installed (fixes `#85`_).
  [rodfersou]

- Fix CSS to fileupload class instead of fileupload id; this allows multiple plugin instances.
  [rodfersou]

- Avoid page template exception with five.pt.
  [rodfersou]


9.18.0b1 (2017-04-17)
^^^^^^^^^^^^^^^^^^^^^

- Update jQuery File Upload Plugin to version 9.18.0 (closes `#56`_).
  [rodfersou]

- Drop support for Plone 4.2.
  [rodfersou]


1.3b1 (2016-08-24)
^^^^^^^^^^^^^^^^^^

- The ``IMultipleUpload`` behavior declaration has been removed as it's useless;
  the class will be also removed on next release.
  [hvelarde]

- Registry records are now correctly removed when uninstalling the package.
  [hvelarde]

- Package is compatible with Plone 4.2 again.
  [hvelarde]


1.2b1 (2016-07-19)
^^^^^^^^^^^^^^^^^^

- Use a viewlet to display the upload widget on the ``folder_contents`` view instead of overriding it.
  The viewlet can be disable via a new option in the control panel configlet (closes `#65`_).
  [rodfersou, hvelarde]

- Remove dependency on five.grok (closes `#66`_).
  [rodfersou]

- Cross-site file uploads are working again (fixes `#71`_).
  [rodfersou]

- Fix MIME type of images processed in ``jsonimageserializer`` view.
  [hvelarde]

- Add field to set the creator (closes `#34`_).
  [rodfersou]

- Finnish translations.
  [petri]


1.1b2 (2016-04-25)
^^^^^^^^^^^^^^^^^^

- Use jQuery `.then()` method instead of deprecated `deferred.pipe()`;
  fix image preview and upload progress bar.
  [rodfersou]

- Fix UnicodeEncodeError on JSVariables view.
  [rodfersou]


1.1b1 (2016-04-15)
^^^^^^^^^^^^^^^^^^^

- Remove dependency on Bootstrap (closes `#46`_).
  [rodfersou]

- Use "application/javascript" media type instead of the obsolete "text/javascript".
  [hvelarde]

- Remove dependency on Products.CMFQuickInstallerTool.
  [hvelarde]

- Fix IE conditional comment on JS registry
  [tcurvelo]

- Drop support for Plone 4.2 (we no longer test under this version but it may work).
  [hvelarde]

- Make control panel configlet accesible to Site Administrator role (closes `#35`_).
  [hvelarde]

- Updated Spanish translation.
  [macagua]


1.0rc1 (2014-10-24)
^^^^^^^^^^^^^^^^^^^

- Fix browser CORS check.
  [petschki]

- Add missing uninstall profile.
  [thet]


1.0b6 (2013-07-24)
^^^^^^^^^^^^^^^^^^

- Fixes issue `#24`_, upload not working on folderish objects with a
  default_page defined. [jpgimenez]

- Fix issue with collective.upload not setting filename on uploaded images
  (Archetypes). [ericof]

- Fix misplaced input element in chrome. [domruf]


1.0b5 (2013-06-13)
^^^^^^^^^^^^^^^^^^

- Display viewlet **only** for users with Add portal content permission and
  if the context is a contaner [ericof]

- Fix issue with collective.upload ignoring title information [ericof]


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

.. _`#6`: https://github.com/collective/collective.upload/issues/6
.. _`#16`: https://github.com/collective/collective.upload/issues/16
.. _`#24`: https://github.com/collective/collective.upload/issues/24
.. _`#34`: https://github.com/collective/collective.upload/issues/34
.. _`#35`: https://github.com/collective/collective.upload/issues/35
.. _`#46`: https://github.com/collective/collective.upload/issues/46
.. _`#56`: https://github.com/collective/collective.upload/issues/56
.. _`#65`: https://github.com/collective/collective.upload/issues/65
.. _`#66`: https://github.com/collective/collective.upload/issues/66
.. _`#71`: https://github.com/collective/collective.upload/issues/71
.. _`#85`: https://github.com/collective/collective.upload/issues/85
