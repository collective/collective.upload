# -*- coding: utf-8 -*-

from five import grok

from plone.app.layout.viewlets.interfaces import IPortalFooter

from collective.upload.behaviors import IMultipleUpload

grok.templatedir('viewlets')


class MediaUploaderInit(grok.Viewlet):
    """ The viewlet doing the initialization, imports of JavaScript,
    no-conflict jQuery variable assignation, etc.
    """
    grok.context(IMultipleUpload)
    grok.name('upload.init')
    grok.require('cmf.AddPortalContent')
    grok.template('media_uploader_init')
    grok.viewletmanager(IPortalFooter)
