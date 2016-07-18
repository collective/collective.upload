# -*- coding: utf-8 -*-
from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.testing import INTEGRATION_TESTING
from plone import api
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

import unittest


class JSVariablesViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IUploadBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                container=self.portal, type='Folder', id='test-folder')

    def test_jsvariables_view_is_present(self):
        view = queryMultiAdapter((self.folder, self.request), name='jsvariables')
        self.assertTrue(view is not None)

    def test_registry_config(self):
        view = getMultiAdapter((self.folder, self.request), name='jsvariables')

        registry_config = view.registry_config()
        expected = "{'max_file_size': 10485760, 'resize_max_width': 3872, " \
                   "'extensions': 'gif|jpeg|jpg|png', 'resize_max_height': 3872}"
        self.assertEqual(registry_config, expected)


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
        self.request['callback'] = '?'

        rendered = view.render()
        image = json.loads(rendered[2:-2])  # get JSON data
        self.assertEqual(image['mimetype'], 'png')
        self.assertTrue(image['data'].startswith('data:image/png;base64,'))
        self.assertEqual(image['width'], 215)
        self.assertEqual(image['height'], 56)

    def test_nocallback(self):
        # TODO: Change this test after the nocallback error implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://old.plone.org/logo.png'
        self.request['url'] = url
        self.assertIsNone(view.render())

    def test_server_respond_not200(self):
        # TODO: Change this test after the non200 code implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://plone.org/logo2.png'
        self.request['url'] = url
        view.render()
        self.assertEqual(self.request.response.status, 500)

    def test_server_non_existing_url(self):
        # TODO: Change this test after the non200 code implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://notanexistingurl.org/fake.png'
        self.request['url'] = url
        self.assertIsNone(view.render())
