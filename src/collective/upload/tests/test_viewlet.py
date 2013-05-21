# -*- coding: utf-8 -*-

import unittest

from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from Products.Five.browser import BrowserView as View

from collective.upload.behaviors import IMultipleUpload
from collective.upload.testing import INTEGRATION_TESTING

NAME = 'collective.upload.tmpls'


class ViewletTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        # HACK: our Folder object "has" the behavior just for testing purposes
        alsoProvides(self.folder, IMultipleUpload)

    def test_manager_viewlet_is_present_in_folder(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = View(self.folder, self.request)
        manager = queryMultiAdapter((self.folder, self.request, view),
                                    IViewletManager, 'plone.htmlhead')
        self.assertTrue(manager is not None)

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == NAME]
        self.assertEqual(len(viewlet), 1)

    def test_manager_viewlet_is_present_in_portal(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = View(self.portal, self.request)
        manager = queryMultiAdapter((self.portal, self.request, view),
                                    IViewletManager, 'plone.htmlhead')
        self.assertTrue(manager is not None)

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == NAME]
        self.assertEqual(len(viewlet), 1)

    def test_anonymous_viewlet_is_not_present_in_folder(self):
        logout()
        view = View(self.folder, self.request)
        manager = queryMultiAdapter((self.folder, self.request, view),
                                    IViewletManager, 'plone.htmlhead')
        self.assertTrue(manager is not None)

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == NAME]
        self.assertEqual(len(viewlet), 0)

    def test_anonymous_viewlet_is_not_present_in_portal(self):
        logout()
        view = View(self.portal, self.request)
        manager = queryMultiAdapter((self.portal, self.request, view),
                                    IViewletManager, 'plone.htmlhead')
        self.assertTrue(manager is not None)

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == NAME]
        self.assertEqual(len(viewlet), 0)
