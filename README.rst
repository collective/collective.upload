*****************
collective.upload
*****************

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

File upload widget with multiple file selection, drag&drop support, progress bars, client-side image resizing and preview images.

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

#. Edit your buildout.cfg and add ``collective.upload`` to the list of eggs to install:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.upload

    [versions]
    ...
    plone.app.jquery = 1.8.3

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.upload`` and click the 'Activate' button.

Usage
^^^^^

The upload widget can be accessed selecting the 'Multiple files' option in the 'Add new…' menu.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/modal.png
    :align: center
    :height: 768px
    :width: 1024px

    The upload widget in a modal window.

Select as many files as you want to upload using by the 'Add files…' button or the drag and drop feature
(you can even do the later among diferent browser windows).
You can set the title, description and rights for any file or image in advance.
If images have Exif metadata it will be used to pre-populate description and rights.
A preview of all images, audios and videos will be shown.
Start the upload individually or in a batch by pressing the 'Start' button.
You will see a bar indicating the progress of the upload.
You can cancel the upload at any time and you can also delete any file or image already uploaded into the site.

The upload widget can be also used in the context of the folder contents view of any folderish object.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/foldercontents.png
    :align: center
    :height: 768px
    :width: 1024px

    The upload widget in the folder contents view.

You can configure some aspects of the upload widget using the Upload configlet on Site Setup.

.. figure:: https://raw.githubusercontent.com/collective/collective.upload/master/docs/controlpanel.png
    :align: center
    :height: 1024px
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
- **No browser plugins required**: The implementation is based on open standards like HTML5 and JavaScript and requires no additional browser plugins
- **Multiple file upload**: Allows to select multiple files at once and upload them simultaneously
- **Drag & Drop support**: Allows to upload files by dragging them from your desktop or filemanager and dropping them on your browser window
- **Support for Exif metadata**: Uploading images with Exif metadata will pre-populate description and rights
- **Preview for images, audios and videos**: A preview of image, video and audio files is displayed before uploading with browsers supporting the required JS APIs
- **Client-side image resizing**: Images can be automatically resized on client-side with browsers supporting the required JS APIs
- **Upload progress bar**: Shows a progress bar indicating the upload progress for individual files and for all uploads combined
- **Cancelable uploads**: Individual file uploads can be canceled to stop the upload progress
- **Graceful fallback for legacy browsers**: Uploads files via XMLHttpRequests if supported and uses iframes as fallback for legacy browsers
- **Drag and drop uploads from another web page**: Supports uploading files dragged from one page into another (tested with Firefox and Chrome)

Desktop browsers support
^^^^^^^^^^^^^^^^^^^^^^^^

- Google Chrome
- Apple Safari 4.0+
- Mozilla Firefox 3.0+
- Opera 11.0+
- Microsoft Internet Explorer 6.0+

Mobile browsers are also supported.
Check `Browser support <https://github.com/blueimp/jQuery-File-Upload/wiki/Browser-support>`_ for details on features supported by each browser.

Santa's wish list
^^^^^^^^^^^^^^^^^

We want to implement these features at some point in the future:

- [ ] Check if constraints are in place before adding the menu item
- [ ] Resumable uploads: Aborted uploads can be resumed with browsers supporting the Blob API
- [ ] Chunked uploads: Large files can be uploaded in smaller chunks with browsers supporting the Blob API
- [ ] HTML file upload form fallback: Shows a standard HTML file upload form if JavaScript is disabled

Not entirely unlike
-------------------

`collective.quickupload`_
    Pure javascript files upload tool for Plone, with drag and drop, multi
    selection, and progress bar.

`collective.uploadify`_
    Multi File Upload for Plone.

.. _`collective.quickupload`: http://pypi.python.org/pypi/collective.quickupload
.. _`collective.uploadify`: http://pypi.python.org/pypi/collective.uploadify
