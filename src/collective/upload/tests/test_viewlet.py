# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from Products.Five.browser import BrowserView as View

from collective.upload.behaviors import IMultipleUpload
from collective.upload.testing import INTEGRATION_TESTING


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

    def test_viewlet_is_present(self):
        view = View(self.folder, self.request)
        manager = queryMultiAdapter((self.folder, self.request, view),
                                    IViewletManager, 'plone.portalfooter')
        self.assertTrue(manager is not None)

        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == 'upload.init']
        self.assertEqual(len(viewlet), 1)
