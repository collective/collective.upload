*****************
collective.upload
*****************

.. contents:: Table of Contents

Overview
--------

An implementation of the `jQuery File Upload
<http://blueimp.github.com/jQuery-File-Upload/>`_ Plugin for Plone.

Requirements
------------

* Plone >= 4.1 (http://plone.org/products/plone)
* five.grok >= 1.2 (http://pypi.python.org/pypi/five.grok)

Features
--------

* Allows to select multiple files at once and upload them simultaneously
* Allows to upload files by dragging them from your desktop or filemanager and
  dropping them on your browser window
* Shows a progress bar indicating the upload progress for individual files and
  for all uploads combined
* Individual file uploads can be canceled to stop the upload progress
* Aborted uploads can be resumed with browsers supporting the Blob API
* Large files can be uploaded in smaller chunks with browsers supporting the
  Blob API
* A preview of image files can be displayed before uploading with browsers
  supporting the required HTML5 APIs
* The implementation is based on open standards like HTML5 and JavaScript and
  requires no additional browser plugins
* Integrates smoothly with Plone's UI
* New behavior for Dexterity content types available

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
