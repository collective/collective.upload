*****************
collective.upload
*****************

.. contents:: Table of Contents

Overview
--------

An implementation of the `jQuery File Upload
<http://blueimp.github.com/jQuery-File-Upload/>`_ Plugin for Plone.

* In the current state, the implementation is ONLY available like a Dexterity
  behavior.
* The action to launch the overlay is located in the "Add new…" menu and is
  inserted using JavaScript, if JavaScript is deactivated, the plugin is not
  going to work.

Requirements
------------

* Plone >= 4.1 (http://plone.org/products/plone)
* five.grok >= 1.2 (http://pypi.python.org/pypi/five.grok)

Features
--------

* Allows to select multiple files at once and upload them sequentially
  (simultaneously is not currently enabled)
* Allows to upload files by dragging them from your desktop or filemanager and
  dropping them on your browser window
* Shows a progress bar indicating the upload progress for individual files and
  for all uploads combined
* Individual file uploads can be canceled to stop the upload progress
* A preview of image files can be displayed before uploading with browsers
  supporting the required HTML5 APIs
* The implementation is based on open standards like HTML5 and JavaScript and
  requires no additional browser plugins
* Configlet configuration for Client-side image resizing
* Configlet configuration for maximum allowed file size
* Configlet configuration for accept file types

Browsers supported
------------------

* Google Chrome 7.0+
* Mozilla Firefox 3.0+
* Microsoft Internet Explorer 6.0+
* Opera 10.0+
* Apple Safari 4.0+

Drag & Drop is only supported on Google Chrome, Firefox 4.0+ and Safari 5.0+.

Microsoft Internet Explorer has no support for multiple file selection or
upload progress.

Future features
---------------

We want to implement these features at some point in the future:

* Smooth integration with Plone's UI
* Refactoring of widget's UI
* HTML file upload form fallback
* Cross-site file uploads
* Resume of aborted uploads with browsers supporting the Blob API
* Upload of large files in smaller chunks with browsers supporting the Blob
  API
* Support for upload content on Archetypes-based content types
* Configuration to enable automatic uploads
* Server side image resizing
* Server side file type constraint
* AMD support
* Widget for allowed extensions configlet
* complete i18n support


Why do we need another multiple file upload package?
----------------------------------------------------

Because in software development, as in any natural environment, diversity is
good.

Half a year ago, we tested the existing packages, `collective.uploadify
<http://pypi.python.org/pypi/collective.uploadify>`_ and
`collective.quickupload
<http://pypi.python.org/pypi/collective.quickupload>`_, because we were
working on a project that required this feature.

We though collective.quickupload was good but, at that point, it had no
support for Dexterity-based content types. After some research we found that
jQuery File Upload was really nice, so we started this project.

Unfortunately, we hadn't had enough time to work more on this, but that's
about to change. We have our own vision on how the UI for this feature must
behave and we want to implement it.

Also, we strongly believe Flash must die and Microsoft must stop pretending
Internet Explorer can continue ignoring web standards forever; we are not
going to support neither.

