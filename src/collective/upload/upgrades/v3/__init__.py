# -*- coding: utf-8 -*-
from collective.upload.config import PROJECTNAME
from collective.upload.logger import logger


def update_jsregistry(setup_tool):
    """Update jsregistry"""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'jsregistry')
    logger.info('JS registry updated.')
