*****************
collective.upload
*****************

.. contents:: Table of Contents

Overview
--------

File upload widget with multiple file selection, drag&drop support, progress
bars, client-side image resizing and preview images.

- In the current state, the implementation is ONLY available like a Dexterity
  behavior.
- The action to launch the overlay is located in the "Add new…" menu and is
  inserted using JavaScript, if JavaScript is deactivated, the plugin is not
  going to work.

Features
--------

- **Multiple file upload**: Allows to select multiple files at once and upload
  them sequentially (simultaneously is not currently enabled)
- **Drag & Drop support**: Allows to upload files by dragging them from your
  desktop or file manager and dropping them on your browser window
- **Upload progress bar**: Shows a progress bar indicating the upload progress
  for individual files and for all uploads combined
- **Cancelable uploads**: Individual file uploads can be canceled to stop the
  upload progress
- **Client-side image resizing**: Images can be automatically resized on
  client-side with browsers supporting the required JS APIs
- **Preview images**: A preview of image files can be displayed before
  uploading with browsers supporting the required JS APIs
- **No browser plugins required**: The implementation is based on open
  standards like HTML5 and JavaScript and requires no additional browser
  plugins
- **Graceful fallback for legacy browsers**: Uploads files via XMLHttpRequests
  if supported and uses iframes as fallback for legacy browsers

Browsers supported
------------------

- Google Chrome 7.0+
- Mozilla Firefox 3.0+
- Microsoft Internet Explorer 6.0+
- Opera 10.0+
- Apple Safari 4.0+

Drag & Drop is only supported on Google Chrome, Firefox 4.0+ and Safari 5.0+.

Client-side image resizing is only supported on Google Chrome, Firefox 4.0+.

Microsoft Internet Explorer has no support for multiple file selection or
upload progress.

`Extended browser support information`_.

Future features
---------------

We want to implement these features at some point in the future:

- Smooth integration with Plone's UI
- Refactoring of widget's UI
- **Resumable uploads**: Aborted uploads can be resumed with browsers
  supporting the Blob API
- **Chunked uploads**: Large files can be uploaded in smaller chunks with
  browsers supporting the Blob API
- **HTML file upload form fallback**: Shows a standard HTML file upload form
  if JavaScript is disabled
- **Cross-site file uploads**: Supports uploading files to a different domain
  with Cross-site XMLHttpRequests
- Support for Archetypes-based content types

Why do we need another multiple file upload package?
----------------------------------------------------

Because in software development, as in any natural environment, diversity is
good.

By mid 2011 we tested the existing packages, `collective.uploadify`_ and
`collective.quickupload`_, because we were working on a project that required
this feature.

We though `collective.quickupload`_ was good but, at that point, it had no
support for Dexterity-based content types. After some research we found that
jQuery File Upload was really nice, so we started this project.

Unfortunately, we hadn't enough time to work more on this, but that has
changed. We have our own vision on how the UI for this feature must behave and
we want to implement it.

Also, we strongly believe Adobe Flash must die and Microsoft must stop
pretending Internet Explorer can continue ignoring web standards forever.

.. _`collective.uploadify`: http://pypi.python.org/pypi/collective.uploadify
.. _`collective.quickupload`: http://pypi.python.org/pypi/collective.quickupload
.. _`Extended browser support information`: https://github.com/blueimp/jQuery-File-Upload/wiki/Browser-support

