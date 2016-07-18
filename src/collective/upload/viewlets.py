# -*- coding: utf-8 -*-
from collective.upload.interfaces import IUploadSettings
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.content.browser.interfaces import IFolderContentsView
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


class WidgetViewlet(ViewletBase):

    def enabled(self):
        """Show the viewlet just in folder_contents view if enabled."""
        if not IFolderContentsView.providedBy(self.view):
            return False

        try:
            return api.portal.get_registry_record(
                interface=IUploadSettings, name='show_widget')
        except (InvalidParameterError, KeyError):
            # avoid breaking page rendering if record is not present
            # this could happen on upgrades or accidental deletions
            return False
