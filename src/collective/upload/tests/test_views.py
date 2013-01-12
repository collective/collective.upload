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


class APITestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, IUploadBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_api_view_is_present(self):
        view = queryMultiAdapter((self.folder, self.request), name='api')
        self.assertTrue(view is not None)

    def test_dumps(self):
        view = getMultiAdapter((self.folder, self.request), name='api')

        self.assertEqual(view.dumps(), '{"files": {}}')
        # TODO: test with content added

    def test_getContextInfo(self):
        #view = getMultiAdapter((self.folder, self.request), name='api')
        # TODO
        NotImplemented

    def test_getContainerInfo(self):
        #view = getMultiAdapter((self.folder, self.request), name='api')
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
        directlyProvides(self.request, IUploadBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_encoding(self):
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://plone.org/logo.png'
        self.request['url'] = url
        self.request['callback'] = '?'

        self.assertEqual(view.render(), '?({"mimetype": "jpeg", "width": 215, "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANcAAAA4CAMAAABZsZ3QAAAAM1BMVEX29fK42OU+oMvn7u9drtIPisHI4OhstdWZyt4fkcXX5+sAg74umMhNp86p0eJ7vNiKw9v/UV4wAAAAAXRSTlMAQObYZgAABBxJREFUeF7tmuty4yAMhZG4X2zn/Z92J5tsBJwWXG/i3XR6frW2Y/SBLIRAfaQUDNt8E5tLUt9BycfcKfq3R6Mlfyimtx4rzp+K3dtibXkor99zsEqLYZltblTecciogoh+TXfY1Ve4dn07rCDGG9dHSEEOg/GmXl0U1XDxTKxNK5De7BxsyyBr6gGm2/vPxKJ8F6f7BXKfRMp1xIWK9A+5ks25alSb353dWnDJN1k35EL5f8dVGifTf/4tjUuuFq7u4srmXC60yAmldLXIWbg65RKU87lcGxJCFqUPv0IacW0PmSivOZFLE908inPToMmii/roG+MRV/O8FU88i8tFsxV3a06MFUw0Qu7RmAtdV5/HVVaOVMTWNOWSwMljLhzhcB6XIS7OK5V6AvRDNN7t5VJWQs1J40UmalbK56usBG/CuCHSYuc+rkUGeMCViNRARPrzW52N3oQLe6WifNliSuuGaH3czbVNudI9s7ZLUCLHVwWlyES522o1t14uvmbblmVTKqFjaZYJFSTPP4dLL1kU1z7p0lzdbRulmEWLxoQX+z9ce7A8GqEEucllLxePuZwdJl1Lezu0hoswvTPt61DrFcRuujV/2cmlxaGBC7Aw6cpovGANwRiSdOAWJ5AGy4gLL64dl0QhUEAuEUNws+XxV+OKGPdw/hESGYF9XEGaFC7sNLMSXWJjHsnanYi87VK428N2uxpOjOFANcagLM5l+7mSycM8KknZpKLcGi6jmzWGr/vLurZ/0g4u9AZuAoeb5r1ceQhyiTPY1E4wUR6u/F3H2ojSpXMMriBPT9cezTto8Cx+MsglHL4fv1Rxrb1LVw9yvyQpJ3AhFnLZfuRLH2QsOG3FGGD20X/th/u5bFAt16Bt308KjF+MNOXgl/SquIEySX3GhaZvc67KZbDxcCDORz2N8yCWPaY5lyQZO7lQ29fnZbt3Xu6qoge4+DjXl/MocySPOp9rlvdyznahRyHEYd77v3LhugOXDv4J65QXfl803BDAdaWBEDhfVx7nKofjoVCgxnUAqw/UAUDPn788BDvQuG4TDtdtUPvzjSlXAB8DvaDOhhrmhwbywylXAm8CvaouikJTL93gs3y7Yy4VYbIxOHrcMizPqWOjqO9l3Uz52kibQy4xxOgqhJvD+w5rvokOcAlGvNCfeqCv1ste1stzLm0f71Iq3ZfTrPfuE5nhPtF+LvQE2lffQC7pYtQy3tdzdrKvd5TLVVzDetScS3nEKmmwDyt1Cev1kX3YfbvzNK4fzrlw+cB6vm+uiUgf2zdXI62241LawCb7Pi5FXFPF8KpzDoF/Sw2lg+GrHNbno1mhPu+VCF/vfMnw06PnUl6j48dVHD3jHNHPua+fc3o/5yp/zsGi0vYtzi3Pz5mHd4T6BWMIlewacd63AAAAAElFTkSuQmCC", "height": 56});')

    def test_nocallback(self):
        # TODO: Change this test after the nocallback error implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://plone.org/logo.png'
        self.request['url'] = url

        self.assertEqual(view.render(), None)

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

        self.assertEqual(view.render(), None)
