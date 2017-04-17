# -*- coding: utf-8 -*-
from collective.upload.testing import FUNCTIONAL_TESTING
from collective.upload.testing import INTEGRATION_TESTING
from plone import api
from plone.app.contentmenu.interfaces import IFactoriesMenu
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from zope.browsermenu.interfaces import IBrowserMenu
from zope.component import getUtility

import transaction
import unittest


class MenuFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'upload-folder')

        transaction.commit()

    def test_factory_menu_item(self):
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        browser.open(portalURL + '/upload-folder')
        self.assertIn('Multiple Files', browser.contents)
        self.assertIn('@@media_uploader', browser.contents)
        browser.getLink('Multiple Files').click()
        self.assertIn('@@media_uploader', browser.url)
        self.assertIn('Add files&hellip;', browser.contents)


class MenuIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(self.portal, 'Folder', 'upload-folder')

        self.menu = getUtility(IBrowserMenu,
                               name='upload_contentmenu_factory',
                               context=self.folder)

    def test_menu_implements_IFactoriesMenu(self):
        self.assertTrue(IFactoriesMenu.providedBy(self.menu))

    @unittest.expectedFailure
    def test_menu_item_upload(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertIn('Multiple Files',
                      [a['id'] for a in actions])
