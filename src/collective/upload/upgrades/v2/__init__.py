# -*- coding: utf-8 -*-
from collective.upload.config import PROJECTNAME
from collective.upload.logger import logger


def update_rolemap(setup_tool):
    """Update roles."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'rolemap')
    logger.info('Role map updated.')


def update_configlet(setup_tool):
    """Update control panel configlet."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'controlpanel')
    logger.info('Control panel configlet updated.')
