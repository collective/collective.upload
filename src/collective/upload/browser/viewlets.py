# -*- coding: utf-8 -*-
from collective.upload.interfaces import IUploadSettings
from plone import api
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IFolderish
from zope.component import getUtility


class Tmpls(ViewletBase):

    @property
    def enabled(self):
        """Check if context is folderish or the default view of a folderish."""
        context = self.context
        context_state = api.content.get_view(
            'plone_context_state', context, self.request)
        if context_state.is_default_page():
            context = context.aq_parent
        return IFolderish.providedBy(context)


class WidgetViewlet(ViewletBase):
    def update(self):
        super(WidgetViewlet, self).update()
        self.setup()

    def setup(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IUploadSettings)

    @property
    def enabled(self):
        """Show the viewlet just in folder_contents view if enabled."""
        if not IFolderContentsView.providedBy(self.view):
            return False

        return self.settings.show_widget
