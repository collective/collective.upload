# -*- coding: utf-8 -*-

from collective.upload.testing import FUNCTIONAL_TESTING
from plone.testing.z2 import Browser

import pkg_resources
import unittest

PLONE_VERSION = pkg_resources.require("Plone")[0].version


class Plone43TestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    @unittest.skipUnless('4.3' in PLONE_VERSION, "Plone 4.3 specific")
    def test_static_resource_grokker(self):
        """Grok does not register automatically the static resources anymore
        see: http://svn.zope.org/five.grok/trunk/src/five/grok/meta.py?rev=123298&r1=112163&r2=123298
        """
        portal = self.layer['portal']
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++collective.upload' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
