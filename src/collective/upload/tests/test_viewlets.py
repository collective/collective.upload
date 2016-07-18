# -*- coding: utf-8 -*-
from collective.upload.behaviors import IMultipleUpload
from collective.upload.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView as View
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class TmplsViewletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING
    name = 'collective.upload.tmpls'

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')
        # HACK: our Folder object "has" the behavior just for testing purposes
        alsoProvides(self.folder, IMultipleUpload)

    def test_manager_viewlet_is_present_in_folder(self):
        context, request = self.folder, self.request
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, 'plone.htmlhead')

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == self.name]
        self.assertEqual(len(viewlet), 1)

    def test_manager_viewlet_is_present_in_portal(self):
        context, request = self.portal, self.request
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, 'plone.htmlhead')

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == self.name]
        self.assertEqual(len(viewlet), 1)

    def test_anonymous_viewlet_is_not_present_in_folder(self):
        context, request = self.folder, self.request
        logout()
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, 'plone.htmlhead')

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == self.name]
        self.assertEqual(len(viewlet), 0)

    def test_anonymous_viewlet_is_not_present_in_portal(self):
        context, request = self.portal, self.request
        logout()
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, 'plone.htmlhead')

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == self.name]
        self.assertEqual(len(viewlet), 0)


class WidgetViewletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING
    name = 'collective.upload.widget'

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

    def test_viewlet_is_present_in_foldercontents(self):
        view = api.content.get_view(
            name=u'folder_contents', context=self.folder, request=self.request)
        self.assertIn('<form id="fileupload"', view())

    def test_viewlet_is_disabled_in_default_view(self):
        view = api.content.get_view(
            name=u'folderListing', context=self.folder, request=self.request)
        self.assertNotIn('<form id="fileupload"', view())

    def test_anonymous_viewlet_is_not_present(self):
        context, request = self.folder, self.request
        logout()
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, 'plone.abovecontentbody')

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == self.name]
        self.assertEqual(len(viewlet), 0)
