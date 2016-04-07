# -*- coding: utf-8 -*-
from collective.upload.config import PROJECTNAME
from collective.upload.logger import logger
from plone import api


FIX_CSS = {
    'old': '++resource++collective.upload/css/bootstrap.min.css',
    'new': '++resource++collective.js.bootstrap/css/bootstrap.min.css'
}
FIX_JS = {
    'old': '++resource++collective.upload/vendor/bootstrap.min.js',
    'new': '++resource++collective.js.bootstrap/js/bootstrap.min.js'
}


def fix_resources_references(setup_tool):
    """Fix resource references after add collective.js.bootstrap dependency."""
    css_tool = api.portal.get_tool('portal_css')
    css_ids = css_tool.getResourceIds()
    if FIX_CSS['old'] in css_ids and FIX_CSS['new'] not in css_ids:
        css_tool.renameResource(FIX_CSS['old'], FIX_CSS['new'])
    elif FIX_CSS['old'] in css_ids and FIX_CSS['new'] in css_ids:
        css_tool.unregisterResource(FIX_CSS['old'])
    logger.info('Updated css references.')

    js_tool = api.portal.get_tool('portal_javascripts')
    js_ids = js_tool.getResourceIds()
    if FIX_JS['old'] in js_ids and FIX_JS['new'] not in js_ids:
        js_tool.renameResource(FIX_JS['old'], FIX_JS['new'])
    elif FIX_JS['old'] in js_ids and FIX_JS['new'] in js_ids:
        js_tool.unregisterResource(FIX_JS['old'])
    logger.info('Updated javascript references.')


def update_jsregistry(setup_tool):
    """Update jsregistry"""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'jsregistry')
    logger.info('JS registry updated.')
