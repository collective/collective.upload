# -*- coding: utf-8 -*-
from collective.upload.config import PROJECTNAME
from collective.upload.logger import logger
from plone import api


REMOVE_CSS = '++resource++collective.upload/css/bootstrap.min.css'
REMOVE_JS = '++resource++collective.upload/vendor/bootstrap.min.js'


def remove_bootstrap(setup_tool):
    """Remove Bootstrap references on resource registries."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.unregisterResource(REMOVE_CSS)
    logger.info('Removed Bootstrap CSS references.')

    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.unregisterResource(REMOVE_JS)
    logger.info('Updated Bootstrap JS references.')


def update_jsregistry(setup_tool):
    """Update jsregistry"""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'jsregistry')
    logger.info('JS registry updated.')
