# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.upload.config import IMAGE_MIMETYPES
from collective.upload.interfaces import IUploadSettings
from itertools import izip
from PIL import Image
from plone import api
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATImage
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from requests.exceptions import RequestException
from zope.component import getUtility
from zope.container.interfaces import INameChooser
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import base64
import cStringIO
import json
import os
import requests
import urllib2


# TODO: convert into a folder action: Upload files and images
class MediaUploader(BrowserView):
    """ Handler for the upload process, creation of files, can set a title or
        description, the place to touch if you need extra data saved.
    """

    files = []
    details = {}

    def setup(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IUploadSettings)

    def setup_upload(self):
        self.json_view = api.content.get_view('api', self.context, self.request)
        self.files = self.request.get('files[]', None)
        if self.files is None:
            return
        if not isinstance(self.files, list):
            self.files = [self.files]

        filename = self.request['filename[]']
        if not isinstance(filename, list):
            filename = [filename]
        title = self.request['title[]']
        if not isinstance(title, list):
            title = [title]
        description = self.request['description[]']
        if not isinstance(description, list):
            description = [description]
        rights = self.request['rights[]']
        if not isinstance(rights, list):
            rights = [rights]

        for f, t, d, r in izip(filename, title, description, rights):
            key = safe_unicode(f)
            if not key:
                key = u'blob'
            self.details[key] = dict(title=t, description=d, rights=r)

    def __call__(self, *args, **kwargs):
        self.setup()

        if self.request.get('REQUEST_METHOD', '') != 'POST':
            return super(MediaUploader, self).__call__(*args, **kwargs)

        self.setup_upload()
        if self.files is None:
            return self.json_view()

        uploaded = self.upload()
        if not uploaded or not self.json_view:
            return self.json_view()

        upped = []
        for item in uploaded:
            upped.append(self.json_view.getContextInfo(item))
        return self.json_view.dumps(upped)

    def upload(self):
        loaded = []
        namechooser = INameChooser(self.context)
        for item in self.files:
            if not item.filename:
                continue
            content_type = item.headers.get('Content-Type')
            filename = safe_unicode(item.filename)
            detail = self.details[filename]
            data = item.read()
            # Get a unique id here
            id_name = namechooser.chooseName(detail['title'], self.context)

            # Portal types allowed : File and Image
            # Since Plone 4.x both types use Blob
            if content_type in IMAGE_MIMETYPES:
                portal_type = 'Image'
                wrapped_data = NamedBlobImage(data=data, filename=filename)
            else:
                portal_type = 'File'
                wrapped_data = NamedBlobFile(data=data, filename=filename)

            # Create content
            newfile = api.content.create(
                container=self.context,
                type=portal_type,
                id=id_name,
                title=detail['title'],
                description=detail['description'],
                rights=detail['rights']
            )

            # Set data
            if portal_type == 'File':
                if IATFile.providedBy(newfile):
                    newfile.setFile(data, filename=filename)
                else:
                    newfile.file = wrapped_data
            elif portal_type == 'Image':
                if IATImage.providedBy(newfile):
                    newfile.setImage(data, filename=filename)
                else:
                    newfile.image = wrapped_data
            # Finalize content creation, reindex it
            newfile.reindexObject()
            notify(ObjectModifiedEvent(newfile))
            loaded.append(newfile)
            if loaded:
                return loaded
            return False


class JSONView(BrowserView):
    """ JSON converter; the jQuery plugin requires this kind of response,
    represent the metadata info of the file.
    """

    json_var = {'name': 'File-Name.jpg',
                'title': '',
                'description': '',
                'rights': '',
                'size': 999999,
                'url': '\/\/nohost.org',
                'thumbnail_url': '//nohost.org',
                'delete_url': '//nohost.org',
                'delete_type': 'DELETE',
                }

    def __call__(self):
        self.response.setHeader('Content-Type', 'text/plain')
        return super(JSONView, self).__call__()

    def dumps(self, json_var=None):
        """ """
        if json_var is None:
            json_var = {}
        return json.dumps({'files': json_var})

    def getContextInfo(self, context=None):
        if context is None:
            context = self.context
        context = aq_inner(context)

        info = ''
        context_name = context.Title()
        context_url = context.absolute_url()
        context_type = context.Type()
        del_url = context_url

        # TODO: we should check errors in the delete process, and
        # broadcast those to the error template in JS
        info = {'name': context_name,
                'title': context_name,
                'description': context.Description(),
                'rights': context.Rights(),
                'url': context_url,
                'delete_url': del_url,
                'delete_type': 'DELETE',
                }
        if safe_hasattr(context, 'size'):
            info['size'] = context.size()
        else:
            if context_type == 'File':
                info['size'] = context.file.getSize()
            elif context_type == 'Image':
                info['size'] = context.image.getSize()
        if context_type == 'Image':
            scales = context.restrictedTraverse('@@images')
            thumb = scales.scale(fieldname='image', scale='thumb')
            info['thumbnail_url'] = thumb.url
        return info

    def getContainerInfo(self):
        contents = []
        for item in self.context.objectIds():
            item_info = self.getContextInfo(self.context[item])
            if item_info:
                contents.append(item_info)
        return contents

    def render(self):
        return self.dumps(self.getContainerInfo())


class SerializeImageError(Exception):
    """Exception raised for errors when serialize image."""

    def __init__(self, message):
        self.message = message


class JSONImageConverter(BrowserView):
    """Serialize an image into a base64 arg."""

    def __call__(self):
        return self.render()

    def render(self):
        # Get the parameters from the URL
        query = self.request

        url = query.get('url', None)

        if url is None:
            return

        try:
            # Get the image
            response = requests.get(urllib2.unquote(url))
        except RequestException as e:  # skip on timeouts and other errors
            raise SerializeImageError(e.message)

        if response.status_code != 200:
            log = u'Status code {0} ({1})'.format(response.status_code, response.reason)
            raise SerializeImageError(log)

        im = cStringIO.StringIO(response.content)
        image = Image.open(im)
        width, height = image.size

        # Create the structure for the data URL
        mimetype = image.format.lower()
        data_uri_prefix = 'data:image/{0};base64,'.format(mimetype)

        # Convert the image to base64
        return_image = base64.b64encode(im.getvalue())

        # Construct the response
        data = json.dumps({
            'name': os.path.basename(url),
            'data': data_uri_prefix + return_image,
        })

        # Return the JSON
        self.request.response.setHeader('Content-Type', 'application/json; charset=utf-8')
        return data
