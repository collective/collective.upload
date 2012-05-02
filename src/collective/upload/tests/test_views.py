# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter, queryMultiAdapter
from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.testing import INTEGRATION_TESTING


class JSVariablesViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IUploadBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_jsvariables_view_is_present(self):
        view = queryMultiAdapter((self.folder, self.request), name='jsvariables')
        self.assertTrue(view is not None)

    def test_registry_config(self):
        view = getMultiAdapter((self.folder, self.request), name='jsvariables')

        registry_config = view.registry_config()
        expected = "{'max_file_size': 10485760, 'resize_max_width': 3872, " \
                   "'extensions': 'gif|jpeg|jpg|png', 'resize_max_height': 3872}"
        self.assertEqual(registry_config, expected)
