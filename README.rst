*****************
collective.upload
*****************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

File upload widget with multiple file selection, drag&drop support, progress
bars, client-side image resizing and preview images.

This package is smoothly integrated with Plone's UI and works with any folderish content type based on Archetypes or Dexterity.

Mostly Harmless
---------------

.. image:: http://img.shields.io/pypi/v/collective.upload.svg
    :target: https://pypi.python.org/pypi/collective.upload

.. image:: https://img.shields.io/travis/collective/collective.upload/master.svg
    :target: http://travis-ci.org/collective/collective.upload

.. image:: https://img.shields.io/coveralls/collective/collective.upload/master.svg
    :target: https://coveralls.io/r/collective/collective.upload

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/collective/collective.upload/issues>`_.

See the `complete list of bugs on GitHub <https://github.com/collective/collective.upload/issues?labels=bug&milestone=&page=1&state=open>`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.upload`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        collective.upload

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.upload`` and click the 'Activate' button.

Usage
^^^^^

The upload widget can be accessed selecting the 'Multiple files' option in the 'Add new…' menu.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/modal.png
    :align: center
    :height: 620px
    :width: 768px

    The upload widget in a modal window.

Select as many files as you want to upload using by the 'Add files or images…' button or the drag and drop feature
(you can even do the later among diferent browser windows).
A preview of all images will be shown.
You can set the title, description and rights for any file or image in advance.
Start the upload individually or in a batch by pressing the 'Start' button.
You will see a bar indicating the progress of the upload.
You can cancel the upload at any time and you can also delete any file or image already uploaded into the site.

The upload widget can be also used in the context of the folder contents view of any folderish object.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/foldercontents.png
    :align: center
    :height: 930px
    :width: 768px

    The upload widget in the folder contents view.

You can configure some aspects of the upload widget using the Upload configlet on Site Setup.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/controlpanel.png
    :align: center
    :height: 740px
    :width: 768px

    The Upload control panel configlet.

You can disable the display of the upload widget in the folder contents view
(the widget will be always accessible via the 'Add new…'' menu regardless this setting).
You can set which files extensions are allowed to be uploaded using the widget.
You can also set the maximum file size and maximum dimensions for images
(images will be automatically resized client-side if they are bigger than these settings).

Features
^^^^^^^^

- Support for Archetypes and Dexterity-based content types
- **Multiple file upload**: Allows to select multiple files at once and upload them simultaneously
- **Drag & Drop support**: Allows to upload files by dragging them from your desktop or filemanager and dropping them on your browser window
- **Upload progress bar**: Shows a progress bar indicating the upload progress for individual files and for all uploads combined
- **Cancelable uploads**: Individual file uploads can be canceled to stop the upload progress
- **Client-side image resizing**: Images can be automatically resized on client-side with browsers supporting the required JS APIs
- **Preview images**: A preview of image files can be displayed before uploading with browsers supporting the required JS APIs
- **No browser plugins required**: The implementation is based on open standards like HTML5 and JavaScript and requires no additional browser plugins
- **Graceful fallback for legacy browsers**: Uploads files via XMLHttpRequests if supported and uses iframes as fallback for legacy browsers
- **Cross-site file uploads**: Supports uploading files to a different domain with cross-site XMLHttpRequests or iframe redirects

Desktop browsers support
^^^^^^^^^^^^^^^^^^^^^^^^

- Apple Safari 4.0+
- Google Chrome 7.0+
- Microsoft Internet Explorer 6.0+
- Mozilla Firefox 3.0+
- Opera 10.0+

For a detailed overview of the features supported by each browser version,
please have a look at the `Extended browser support information`_.

Future features
^^^^^^^^^^^^^^^

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

Developer's notes
^^^^^^^^^^^^^^^^^

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

To-do list
^^^^^^^^^^

* Check if constraints are in place before adding the menu item.

.. _`Extended browser support information`: https://github.com/blueimp/jQuery-File-Upload/wiki/Browser-support
.. _`canvas-to-blob.min.js`: https://github.com/blueimp/JavaScript-Canvas-to-Blob
.. _`load-image.min.js`: https://github.com/blueimp/JavaScript-Load-Image
.. _`AMD`: https://github.com/amdjs/amdjs-api/wiki/AMD

Not entirely unlike
-------------------

`collective.quickupload`_
    Pure javascript files upload tool for Plone, with drag and drop, multi
    selection, and progress bar.

`collective.uploadify`_
    Multi File Upload for Plone.

.. _`collective.quickupload`: http://pypi.python.org/pypi/collective.quickupload
.. _`collective.uploadify`: http://pypi.python.org/pypi/collective.uploadify
