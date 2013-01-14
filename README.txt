*****************
collective.upload
*****************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

File upload widget with multiple file selection, drag&drop support, progress
bars, client-side image resizing and preview images.

``collective.upload`` is smoothly integrated with Plone's UI and works with
any folderish content type based on Archetypes or Dexterity.

Features
--------

- Support for Archetypes and Dexterity-based content types
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
- **Cross-site file uploads**: Supports uploading files to a different domain
  with Cross-site XMLHttpRequests

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

- Refactoring of widget's UI
- **Resumable uploads**: Aborted uploads can be resumed with browsers
  supporting the Blob API
- **Chunked uploads**: Large files can be uploaded in smaller chunks with
  browsers supporting the Blob API
- **HTML file upload form fallback**: Shows a standard HTML file upload form
  if JavaScript is disabled
- Enable/disable automatic uploads
- Server side image resizing
- Server side file type constraint
- Asynchronous Module Definition (`AMD`_) support
- Widget for "allowed extensions" option

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

Also, we strongly believe Adobe Flash must die and Microsoft must stop
pretending Internet Explorer can continue ignoring web standards forever.

Developer's notes
-----------------

In the folder "static" you are going to find the JavaScript used in this
project; here a list with the file name and function:

applications.js
  The main file; here you will find 2 important things: plugin initialization
  and inheritance of basic UI code with custom templates (e.g. every new file
  dropped in the file upload widget is going to generate a new row, here is
  the code for that).

`canvas-to-blob.min.js`_
  Converts canvas elements into Blob objects, is a polyfill for the standard
  HTML canvas.toBlob method.

`load-image.min.js`_
  Load Image is a function to load images provided as File or Blob objects or
  via URL.

jquery.fileupload.js
  The most basic version of the File Upload plugin, with no UI.

jquery.fileupload-fp.js
  Extends the basic fileupload widget with image processing functionality.

jquery.fileupload-ui.js
  Extends the FP version, adds complete user interface interaction.

jquery.iframe-transport.js
  Used for cross-site iframe transport uploads a way of degradation for the
  XHR upload.

cors/jquery.xdr-transport.js
  jQuery XDomainRequest Transport plugin; enables cross-domain AJAX requests
  (GET and POST only) (not really used, its just there if you need to
  implement that kind of functionality).

vendor/jquery.ui.widget.js
  jQuery UI widget factory; very lightweight, flexible base for building
  complex, statefull plugins with a consistent API. It is designed for general
  consumption by developers who want to create object-oriented components
  without reinventing common infrastructure.

vendor/jquery.getimagedata.min.js
  It enables pixel level access to images from different origins. It works by sending a JSONP request with the URL of the image to the server. The server then converts the image into base64 encoded data URL and sends the image back as a JSON object. (what this script does, can be done with CORS)

Roadmap
---------------

* Check if constraints are in place before adding the menu item.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/collective.upload.png
    :target: http://travis-ci.org/collective/collective.upload

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.upload/issues
.. _`collective.uploadify`: http://pypi.python.org/pypi/collective.uploadify
.. _`collective.quickupload`: http://pypi.python.org/pypi/collective.quickupload
.. _`Extended browser support information`: https://github.com/blueimp/jQuery-File-Upload/wiki/Browser-support
.. _`canvas-to-blob.min.js`: https://github.com/blueimp/JavaScript-Canvas-to-Blob
.. _`load-image.min.js`: https://github.com/blueimp/JavaScript-Load-Image
.. _`AMD`: https://github.com/amdjs/amdjs-api/wiki/AMD
