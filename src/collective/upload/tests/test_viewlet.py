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

    def test_viewlet_is_present(self):
        # FIXME: the viewlet is only present in Dexterity content types with
        # IMultipleUpload behavior enabled; we need to define a content type,
        # enable the behavior and test if the viewlet is present on it
        # http://collective-docs.readthedocs.org/en/latest/views/viewlets.html#finding-viewlets-programmatically
        request = self.request
        alsoProvides(request, IMultipleUpload)
        context = self.folder

        view = View(context, request)
        manager_name = 'plone.portalfooter'
        manager = queryMultiAdapter((context, request, view),
                                    IViewletManager, manager_name, default=None)
        self.assertNotEqual(manager, None)

        manager.update()
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'upload.init']
        self.assertEqual(len(my_viewlet), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
