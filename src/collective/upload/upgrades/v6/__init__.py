# -*- coding: utf-8 -*-
from collective.upload.interfaces import IUploadSettings
from collective.upload.logger import logger
from plone import api


CSS_TO_UNREGISTER = [
    '++resource++collective.upload/main.css',
    '++resource++collective.upload/css/jquery.fileupload-ui.css',
]
JS_TO_UNREGISTER = [
    'jsvariables',
    '++resource++collective.upload/vendor/jquery.getimagedata.min.js',
    '++resource++collective.upload/vendor/jquery.ui.widget.js',
    '++resource++collective.upload/tmpl.min.js',
    '++resource++collective.upload/load-image.min.js',
    '++resource++collective.upload/canvas-to-blob.min.js',
    '++resource++collective.upload/jquery.iframe-transport.js',
    '++resource++collective.upload/jquery.fileupload.js',
    '++resource++collective.upload/jquery.fileupload-fp.js',
    '++resource++collective.upload/jquery.fileupload-ui.js',
    '++resource++collective.upload/main.js',
    '++resource++collective.upload/cors/jquery.xdr-transport.js',
]


def unregister_old_resources(context):
    """Unregister old resources."""
    css_tool = api.portal.get_tool('portal_css')
    resource_list = css_tool.getResourceIds()
    for css in CSS_TO_UNREGISTER:
        if css not in resource_list:
            continue
        css_tool.unregisterResource(css)
    js_tool = api.portal.get_tool('portal_javascripts')
    resource_list = js_tool.getResourceIds()
    for js in JS_TO_UNREGISTER:
        if js not in resource_list:
            continue
        js_tool.unregisterResource(js)
    logger.info('Old resources unregistered')


def fix_extensions_separator(context):
    """Fix controlpanel valid extensions separator."""
    record = dict(interface=IUploadSettings, name='upload_extensions')
    upload_extensions = api.portal.get_registry_record(**record)
    upload_extensions = upload_extensions.replace(u' ', u'')
    upload_extensions = upload_extensions.replace(u',', u'|')
    record['value'] = upload_extensions
    api.portal.set_registry_record(**record)
    logger.info('Control panel valid extensions separator fixed')
