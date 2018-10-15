# -*- coding: utf-8 -*-
from collective.upload.logger import logger
from plone import api


JS = '++resource++collective.upload/upload.js'
CSS = '++resource++collective.upload/upload.css'


def deprecate_resource_registries(setup_tool):
    """Deprecate resource registries."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.unregisterResource(id=JS)
    assert JS not in js_tool.getResourceIds()  # nosec

    css_tool = api.portal.get_tool('portal_css')
    css_tool.unregisterResource(id=CSS)
    assert CSS not in css_tool.getResourceIds()  # nosec

    logger.info('Static resources were removed from resource registries')
