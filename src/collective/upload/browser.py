# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.upload import _
from collective.upload.config import IMAGE_MIMETYPES
from collective.upload.interfaces import IUploadSettings
from collective.upload.logger import logger
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
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.container.interfaces import INameChooser
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent

import base64
import cStringIO
import json
import urllib2


# TODO: convert into a folder action: Upload files and images
class MediaUploader(BrowserView):
    """ Handler for the upload process, creation of files, can set a title or
        description, the place to touch if you need extra data saved.
    """

    files = []

    def __call__(self, *args, **kwargs):
        if safe_hasattr(self.request, 'REQUEST_METHOD'):
            json_view = queryMultiAdapter(
                (self.context, self.request), name=u'api')
            # TODO: we should check errors in the creation process, and
            # broadcast those to the error template in JS
            if self.request['REQUEST_METHOD'] == 'POST':
                if getattr(self.request, 'files[]', None) is not None:
                    files = self.request['files[]']
                    title = self.request['title[]']
                    description = self.request['description[]']
                    rights = self.request['rights[]']
                    uploaded = self.upload([files], [title], [description], [rights])
                    if uploaded and json_view:
                        upped = []
                        for item in uploaded:
                            upped.append(json_view.getContextInfo(item))
                        return json_view.dumps(upped)
                return json_view()
        return super(MediaUploader, self).__call__(*args, **kwargs)

    def upload(self, files, title='', description='', rights=''):
        loaded = []
        namechooser = INameChooser(self.context)
        if not isinstance(files, list):
            files = [files]
        for item in files:
            if item.filename:
                content_type = item.headers.get('Content-Type')
                filename = safe_unicode(item.filename)
                data = item.read()
                id_name = ''
                title = title and title[0] or filename
                # Get a unique id here
                id_name = namechooser.chooseName(title, self.context)

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
                    title=title,
                    description=description[0],
                    rights=rights[0]
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


messages = {
    'DELETE_MSG': _(u'delete', default=u'Delete'),
    'START_MSG': _(u'start', default=u'Start'),
    'CANCEL_MSG': _(u'cancel', default=u'Cancel'),
    'DESCRIPTION_MSG': _(u'description', default=u'Description'),
    'ERROR_MSG': _(u'error', default=u'Error'),
}


# FIXME: this view is called all over the place and not only when needed
class JSVariables(BrowserView):
    """ This method generates global JavaScript variables, for i18n and plugin
    configuration.
    """

    def __call__(self):
        return self.render()

    def render(self):
        response = self.request.response
        response.setHeader('content-type', 'application/javascript')

        messageTemplate = 'jupload={{}};jupload.messages = {{\n{0}}};\njupload.config = {1};\n'
        template = ''

        for key in messages:
            msg = translate(messages[key], context=self.request).replace("'", "\\'")
            template = "{0}{1}: '{2}',\n".format(template, key, msg.encode('utf-8'))

        # note trimming of last comma
        return messageTemplate.format(template[:-2], self.registry_config())

    def registry_config(self):
        config = {}
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IUploadSettings)
        config['extensions'] = str(settings.upload_extensions.replace(' ', '').replace(',', '|'))
        config['max_file_size'] = settings.max_file_size
        config['resize_max_width'] = settings.resize_max_width
        config['resize_max_height'] = settings.resize_max_height

        return str(config)


class JSONImageConverter(BrowserView):
    """ Serialize an image into a base64 arg.
    """

    def __call__(self):
        return self.render()

    def render(self):
        # Surround everything in a try/except
        try:
            # Get the parameters from the URL
            query = self.request
            response = self.request.response

            # If the user has specified a URL
            if 'url' in query:
                url = query['url']
                try:

                    # Get the image
                    f = urllib2.urlopen(urllib2.unquote(url))

                    # If server with the image responds with 200
                    if f.code == 200:

                        # Create holder for the image
                        im = cStringIO.StringIO(f.read())

                        # Open the image with PIL
                        image = Image.open(im)

                        # Get its width and height
                        width, height = image.size

                        # Create the structure for the data URL
                        mimetype = image.format.lower()
                        data_uri_prefix = 'data:image/{0};base64,'.format(mimetype)

                        # Convert the image to base64
                        return_image = base64.b64encode(im.getvalue())

                        # Construct the response
                        data = json.dumps({
                            'width': width,
                            'height': height,
                            'data': data_uri_prefix + return_image,
                            'mimetype': mimetype,
                        })

                        # If a callback has been specified
                        if 'callback' in query:
                            callback = query['callback']

                            # Add the callback to the end for cross-domain JSON
                            data = callback + '(' + data + ');'

                            # Return the JSON
                            response.setHeader('content-type', 'application/json;;charset=utf-8')

                            return data

                        # If no callback was specified
                        else:
                            # 404
                            return

                    # If server with the image responded with something other than 200
                    else:
                        # status_code = f.code
                        return

                # If urllib errors
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        response.setStatus(self, 404, lock=None)
                    else:
                        response.setStatus(self, 500, lock=None)
                except urllib2.URLError, e:
                    logger.error('URLError', e)

            # If the URL was not specified in the request
            else:
                return

        # Catch any other error
        except:
            return
