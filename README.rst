*****************
collective.upload
*****************

.. contents:: Table of Contents

Overview
--------

An implementation of the `jQuery File Upload
<http://blueimp.github.com/jQuery-File-Upload/>`_ Plugin for Plone.

* In the current state, the implementation is ONLY available like a dexterity
behavior.
* The action to launch the overlay is located in the "add new" menu and is
inserted using javascript, if javascript is deactivated, the plugin is not going
to work.


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

Future Features
---------------
* Aborted uploads can be resumed with browsers supporting the Blob API
* Large files can be uploaded in smaller chunks with browsers supporting the
  Blob API
* Integrates smoothly with Plone's UI
* Widget UI refactoring
* HTML file upload form fallback
* Support for upload content in a non dexterity content type
* Client-side image resizing
* Cross-site file uploads
* Configlet for plugin options
