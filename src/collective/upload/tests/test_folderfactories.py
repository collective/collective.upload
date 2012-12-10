# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from collective.upload.testing import FUNCTIONAL_TESTING


class ViewletTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.folder = self.portal['upload-folder']

    def test_folderfactories_link(self):
        browser = Browser(self.app)
        portalURL = self.portal.absolute_url()
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        browser.open(portalURL + '/upload-folder')
        browser.getLink('Upload multiple files or images').click()
        self.assertIn('Add files or images…', browser.contents)
