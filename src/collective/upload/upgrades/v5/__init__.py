# -*- coding: utf-8 -*-
from collective.upload.logger import logger
from plone import api


UPLOAD_BEHAVIOR = 'collective.upload.behaviors.IMultipleUpload'


def remove_useless_behavior(setup_tool):
    """Remove IMultipleUpload behavior."""
    portal_types = api.portal.get_tool('portal_types')
    msg = 'IMultipleUpload behavior removed from {0} content type'
    for t in portal_types.listContentTypes():
        try:
            behaviors = list(portal_types[t].behaviors)
            if UPLOAD_BEHAVIOR in behaviors:
                behaviors.remove(UPLOAD_BEHAVIOR)
                portal_types[t].behaviors = tuple(behaviors)
                logger.info(msg.format(t))
        except AttributeError:  # not a Dexterity-based content type
            pass
