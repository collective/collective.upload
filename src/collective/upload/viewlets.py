# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface

#from plone.app.layout.viewlets import common
from plone.app.layout.viewlets.interfaces import IDocumentActions
from plone.app.layout.viewlets.interfaces import IPortalFooter

from collective.upload.behaviors import IMultipleUpload


grok.templatedir("viewlets")


class MediaUploaderInit(grok.Viewlet):
    grok.context(IMultipleUpload)
    grok.name(u"upload.init")    
    grok.require("zope2.View")
    grok.template("media_uploader_init")
    grok.viewletmanager(IPortalFooter)    
