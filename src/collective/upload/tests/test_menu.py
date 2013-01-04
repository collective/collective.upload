# -*- coding: utf-8 -*-
from collective.upload.testing import FUNCTIONAL_TESTING
from collective.upload.testing import INTEGRATION_TESTING
from plone.app.contentmenu.interfaces import IFactoriesMenu
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility

import unittest2 as unittest


class MenuFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.folder = self.portal['upload-folder']

    def test_factory_menu_item(self):
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader('Authorization', 'Basic %s:%s' %
                          (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open(portalURL + '/upload-folder')
        self.assertIn('Multiple Files', browser.contents)
        self.assertIn('@@media_uploader', browser.contents)
        browser.getLink('Multiple Files').click()
        self.assertIn('@@media_uploader', browser.url)
        self.assertIn('Add files or images…', browser.contents)


class MenuIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.folder = self.portal['upload-folder']
        self.menu = getUtility(IBrowserMenu,
                               name='upload_contentmenu_factory',
                               context=self.folder)

    def test_menu_implements_IFactoriesMenu(self):
        self.failUnless(IFactoriesMenu.providedBy(self.menu))

    @unittest.expectedFailure
    def test_menu_item_upload(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertIn('Multiple Files',
                      [a['id'] for a in actions])
