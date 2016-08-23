# -*- coding: utf-8 -*-
from collective.upload import config
from collective.upload.config import PROJECTNAME
from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.interfaces import IUploadSettings
from collective.upload.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides

import unittest


BASE_REGISTRY = 'collective.upload.controlpanel.IuploadSettings.%s'


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IUploadBrowserLayer)
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        context, request = self.portal, self.request
        view = api.content.get_view('upload-settings', context, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@upload-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('upload', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('upload', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IUploadSettings)

    def test_show_widget_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'show_widget'))
        self.assertTrue(self.settings.show_widget)

    def test_upload_extensions_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'upload_extensions'))
        self.assertEqual(self.settings.upload_extensions,
                         config.UPLOAD_EXTENSIONS)

    def test_max_file_size_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'max_file_size'))
        self.assertEqual(self.settings.max_file_size,
                         config.MAX_FILE_SIZE)

    def test_resize_max_width_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'resize_max_width'))
        self.assertEqual(self.settings.resize_max_width,
                         config.RESIZE_MAX_WIDTH)

    def test_resize_max_height_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'resize_max_height'))
        self.assertEqual(self.settings.resize_max_height,
                         config.RESIZE_MAX_HEIGHT)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[config.PROJECTNAME])

        records = [
            BASE_REGISTRY % 'show_widget',
            BASE_REGISTRY % 'upload_extensions',
            BASE_REGISTRY % 'max_file_size',
            BASE_REGISTRY % 'resize_max_width',
            BASE_REGISTRY % 'resize_max_height',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
