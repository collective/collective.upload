# -*- coding: utf-8 -*-
# Zope imports
from zope.interface import Interface
from five import grok

# Plone imports
from plone.app.layout.viewlets.interfaces import IHtmlHead


grok.templatedir("viewlets")
# grok.layer(IVTVLayer)


class Tmpls(grok.Viewlet):
    grok.context(Interface)
    grok.name(u"collective.upload.tmpls")
    grok.require("zope2.View")
    grok.template("tmpls")
    grok.viewletmanager(IHtmlHead)
