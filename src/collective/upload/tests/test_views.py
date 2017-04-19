# -*- coding: utf-8 -*-
from collective.upload.browser.views import SerializeImageError
from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.testing import INTEGRATION_TESTING
from plone import api
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

import unittest


class APITestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IUploadBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

    def test_api_view_is_present(self):
        view = queryMultiAdapter((self.folder, self.request), name='api')
        self.assertIsNotNone(view)

    def test_dumps(self):
        view = getMultiAdapter((self.folder, self.request), name='api')

        self.assertEqual(view.dumps(), '{"files": {}}')
        # TODO: test with content added

    def test_getContextInfo(self):
        # view = getMultiAdapter((self.folder, self.request), name='api')
        # TODO
        NotImplemented

    def test_getContainerInfo(self):
        # view = getMultiAdapter((self.folder, self.request), name='api')
        # TODO
        NotImplemented

    def test_render(self):
        view = getMultiAdapter((self.folder, self.request), name='api')

        self.assertEqual(view.render(), '{"files": []}')
        # TODO: test with content added


class JSONImageConverterTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IUploadBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

    def test_encoding(self):
        import json
        context, request = self.folder, self.request
        view = api.content.get_view(
            name='jsonimageserializer', context=context, request=request)
        url = 'http://old.plone.org/logo.png'
        self.request['url'] = url

        image = json.loads(view.render())  # get JSON data
        self.assertEqual(image['name'], 'logo.png')
        self.assertTrue(image['data'].startswith('data:image/png;base64,'))

    def test_server_respond_not200(self):
        # TODO: Change this test after the non200 code implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://plone.org/logo2.png'
        self.request['url'] = url
        with self.assertRaises(SerializeImageError):
            view.render()

    def test_server_non_existing_url(self):
        # TODO: Change this test after the non200 code implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://notanexistingurl.org/fake.png'
        self.request['url'] = url
        with self.assertRaises(SerializeImageError):
            view.render()
