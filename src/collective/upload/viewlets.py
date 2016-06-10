# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.interfaces import IFolderish
from zope.component import getMultiAdapter


class Tmpls(ViewletBase):

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
