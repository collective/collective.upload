# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IHtmlHead
from zope.interface import Interface
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import IFolderish


grok.templatedir("viewlets")


class Tmpls(grok.Viewlet):
    grok.context(Interface)
    grok.name(u"collective.upload.tmpls")
    grok.require("cmf.AddPortalContent")
    grok.template("tmpls")
    grok.viewletmanager(IHtmlHead)

    def enabled(self):
        """
            Only renders the templates if the context is a folderish or
            the default view of a folderish
        """
        context = self.context
        context_state = getMultiAdapter((context, self.request), name=u'plone_context_state')
        if context_state.is_default_page():
            context = context.aq_parent
        return IFolderish.providedBy(context)
