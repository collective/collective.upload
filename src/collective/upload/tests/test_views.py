# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface import directlyProvides

from plone.app.customerize import registration

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.testing import INTEGRATION_TESTING


class BrowserLayerTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IUploadBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_views_registered(self):
        views = ['folder_contents']
        registered = [v.name for v in registration.getViews(IUploadBrowserLayer)]
        # empty set only if all 'views' are 'registered'
        self.assertEquals(set(views) - set(registered), set([]))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
