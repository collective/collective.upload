# -*- coding: utf-8 -*-
import base64
import urllib2
import cStringIO
import json
from PIL import Image

from Acquisition import aq_inner

from five import grok

from zope.container.interfaces import INameChooser
from zope.component import queryMultiAdapter

from zope.event import notify

from zope.interface import Interface
from zope.i18n import translate
from zope.component import getUtility
from zope.component.hooks import getSite

from zope.lifecycleevent import ObjectModifiedEvent

from collective.upload.interfaces import IUploadBrowserLayer, IUploadSettings
#from collective.upload.behaviors import IMultipleUpload

from plone.app.content.browser.foldercontents import FolderContentsView
from plone.registry.interfaces import IRegistry

from collective.upload import _
from collective.upload.config import IMAGE_MIMETYPES

grok.templatedir('templates')


# TODO: implement drag&drop here
class Folder_Contents(grok.View, FolderContentsView):
    grok.context(Interface)
    grok.layer(IUploadBrowserLayer)
    grok.require('cmf.ModifyPortalContent')


# TODO: convert into a folder action: Upload files and images
class Media_Uploader(grok.View):
    """ Handler for the upload process, creation of files, can set a title or
        description, the place to touch if you need extra data saved.
    """
    grok.context(Interface)  # XXX: what's the interface of folderish objects?
    grok.require('collective.upload.UploadFiles')

    files = []

    def __call__(self, *args, **kwargs):
        if hasattr(self.request, "REQUEST_METHOD"):
            json_view = queryMultiAdapter((self.context, self.request),
                                          name=u"api")
            # TODO: we should check errors in the creation process, and
            # broadcast those to the error template in JS
            if self.request["REQUEST_METHOD"] == "POST":
                if getattr(self.request, "files[]", None) is not None:
                    files = self.request['files[]']
                    title = self.request['title[]']
                    description = self.request['description[]']
                    uploaded = self.upload([files], [title], [description])
                    if uploaded and json_view:
                        upped = []
                        for item in uploaded:
                            upped.append(json_view.getContextInfo(item))
                        return json_view.dumps(upped)
                return json_view()
        return super(Media_Uploader, self).__call__(*args, **kwargs)

    def upload(self, files, title='', description=''):
        loaded = []
        namechooser = INameChooser(self.context)
        if not isinstance(files, list):
            files = [files]
        portal = getSite()
        for item in files:
            if item.filename:
                content_type = item.headers.get('Content-Type')
                id_name = ''
                if title:
                    id_name = namechooser.chooseName(title[0], portal)
                else:
                    id_name = namechooser.chooseName(item.filename, portal)
                portal_type = 'File'
                if content_type in IMAGE_MIMETYPES:
                    portal_type = 'Image'
                name_index = 0
                while name_index < 100:
                    try:
                        self.context.invokeFactory(
                            portal_type, id=id_name, file=item, description=description[0])
                        self.context[id_name].reindexObject()
                        newfile = self.context[id_name]
                        notify(ObjectModifiedEvent(newfile))
                        loaded.append(newfile)
                        name_index = 100
                    except:
                        pass
                    name_index = name_index + 1
                    id_name = id_name + '-' + str(name_index)
            if loaded:
                return loaded
            return False


class JSON_View(grok.View):
    """ JSON converter; the jQuery plugin requires this kind of response,
    represent the metadata info of the file.
    """
    grok.context(Interface)
    grok.name('api')
    grok.require('cmf.AddPortalContent')
    grok.layer(IUploadBrowserLayer)

    json_var = {'name': 'File-Name.jpg',
                'title': '',
                'description': '',
                'size': 999999,
                'url': '\/\/nohost.org',
                'thumbnail_url': '//nohost.org',
                'delete_url': '//nohost.org',
                'delete_type': 'DELETE',
                }

    def __call__(self):
        self.response.setHeader('Content-Type', 'text/plain')
        return super(JSON_View, self).__call__()

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
        if hasattr(context, 'size'):
            context_state = queryMultiAdapter(
                (context, self.request), name=u'plone_context_state')
            context_name = context_state.object_title()
            context_url = context_state.object_url()

            del_url = context_url
            # TODO: we should check errors in the delete process, and
            # broadcast those to the error template in JS
            info = {'name': context_name,
                    'title': context_name,
                    'description': context.Description(),
                    'url': context_url,
                    'size': context.size(),
                    'delete_url': del_url,
                    'delete_type': 'DELETE',
                    }
            if context.Type() == 'Image':
                info['thumbnail_url'] = context_url + '/image_thumb'
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
}

messageTemplate = "jupload={};jupload.messages = {\n%s};\njupload.config = %s;\n"


class JSVariables(grok.View):
    """ This method generates global JavaScript variables, for i18n and plugin
    configuration.
    """
    grok.context(Interface)
    grok.name('jsvariables')
    grok.layer(IUploadBrowserLayer)

    def render(self):
        response = self.request.response
        response.setHeader('content-type', 'text/javascript;;charset=utf-8')

        template = ''

        for key in messages:
            msg = translate(messages[key], context=self.request).replace("'", "\\'")
            template = "%s%s: '%s',\n" % (template, key, msg)

        # note trimming of last comma
        return messageTemplate % (template[:-2], self.registry_config())

    def registry_config(self):
        config = {}
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IUploadSettings)
        config['extensions'] = str(settings.upload_extensions.replace(' ', '').replace(',', '|'))
        config['max_file_size'] = settings.max_file_size
        config['resize_max_width'] = settings.resize_max_width
        config['resize_max_height'] = settings.resize_max_height

        return str(config)


class JSONImageConverter(grok.View):
    """ Serialize an image into a base64 arg.
    """
    grok.context(Interface)
    grok.name('jsonimageserializer')
    grok.layer(IUploadBrowserLayer)

    def render(self):
        # Surround everything in a try/except
        try:
            # Get the parameters from the URL
            query = self.request

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
                        type_prefix = "data:image/" + image.format.lower() + ";base64,"

                        # Convert the image to base64
                        return_image = base64.b64encode(im.getvalue())

                        # Construct the response
                        data = json.dumps({
                            "width": width,
                            "height": height,
                            "data": type_prefix + return_image,
                            "mimetype": 'jpeg'
                        })

                        # If a callback has been specified
                        if 'callback' in query:
                            callback = query['callback']

                            # Add the callback to the end for cross-domain JSON
                            data = callback + '(' + data + ');'

                            # Return the JSON
                            response = self.request.response
                            response.setHeader('content-type', 'application/json;;charset=utf-8')

                            return data

                        # If no callback was specified
                        else:
                            #404
                            return

                    # If server with the image responded with something other than 200
                    else:
                        #status_code = f.code
                        return

                # If urllib errors
                except urllib2.HTTPError, e:
                    if e.code == 404:
                        self.response.setStatus(self, 404, lock=None)
                    else:
                        self.response.setStatus(self, 500, lock=None)
                except urllib2.URLError, e:
                    print "URLError", e

            # If the URL was not specified in the request
            else:
                return

        # Catch any other error
        except:
            return
