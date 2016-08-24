# -*- coding: utf-8 -*-
from collective.upload.config import PROJECTNAME
from collective.upload.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers

import unittest


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_setup_permission(self):
        permission = 'collective.upload: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_add_permission(self):
        permission = 'collective.upload: Upload Files'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IUploadBrowserLayer', layers)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_uninstalled(self):
        self.qi.uninstallProducts(products=[PROJECTNAME])
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IUploadBrowserLayer', layers)
