# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IHtmlHead
from OFS.interfaces import IFolder

grok.templatedir("viewlets")


class Tmpls(grok.Viewlet):
    grok.context(IFolder)
    grok.name(u"collective.upload.tmpls")
    grok.require("cmf.AddPortalContent")
    grok.template("tmpls")
    grok.viewletmanager(IHtmlHead)
