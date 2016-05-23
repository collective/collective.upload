# -*- coding: utf-8 -*-
from collective.upload.interfaces import IUploadBrowserLayer
from collective.upload.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
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
        alsoProvides(self.request, IUploadBrowserLayer)

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

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_encoding(self):
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://old.plone.org/logo.png'
        self.request['url'] = url
        self.request['callback'] = '?'

        self.assertEqual(view.render(), '?({"mimetype": "jpeg", "width": 215, "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAANcAAAA4CAMAAABZsZ3QAAAACXBIWXMAAAsTAAALEwEAmpwYAAAANlBMVEUAg77///8Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag74Ag75H6MOjAAAAEXRSTlMAABAgMEBQYHCAj5+vv8/f7/4ucL8AAASNSURBVGje3ZrZloMgDEBTIFLFCPz/z86DimGV2ml7Wt6mOpILIRsBKAypDTm/DjJ3CV80busoQE3WJ8NO8tu5cPbFQfjNXJJ8dZD6Wq7RN8ckvpJLLjGGo2A8trGoL+RCxw3FsFkKOUwM1w1fx6UP4Y1KLeSBrOtflJiOxIqK0o8v5jqwxsIpEqM7ByucTmf4BuP6/XdyYbB623IiqoqlHB7g8t5b/CCX3LdjnVQY7713sQT3fQ/UQ1zeT5/jWiIlE/ufS6SSgyv92uElzKe4dolUTMmWGgAAlCv92uH9xs9wqdgkaCZRbLz2U4gtrjEMY+PPvIlLIIobAABFqwqGcd2hdMaoxRW977gmvodLWTMu6tiFICzlGgTJM+zkCqor3se1DGRxOWSVPVyb4aRern2H9fu4DNKiJgCZEjT0MAivernAHabmTfuFxgoCmFavJDLrkNsNABCuahLLXPOxwQ0uic38DlHUH8Uy3iaj7zQB2MjHHKJUZFilt91c4ymX3CJrN/MYTRERkQbA1azGTzePatZVXlg+f7uN8zzedjXkiiUocaiRFFVFvMYleIJuhzToEuy023hS5PWKWST+S5fWXy/e+yVMEm31Uj54NS5qcynXDLrm+DHfMp2E2CrmMq0QAgBgWLz37ojyV/HnTi7BFLrAlWKlQZcvC59jhWc7F7WD9GAdgxKsEy6dXCNLAnIu4XLZdYPrcDDhsQtR32r6dq6K3Uuj+INEFNWtwqX5lDnXvmhmQLxb/u4huJ0QMWS2u9lcX3ajBAAkttUxV3W7XO7L+rmk8c04SsZlE8ON8M5lRJRjTHy9glqaY3f6uLCgA0vFIKZxLyUaknOtyuBk7GAsnznou7BciCUJ5yh8OuKirhw4+gY+kKfoSp4yJzZLskOBaXaumRAylVqFRXgjl67llS7d+SU1Mi5TWsaoM+8jntfDbi6nq3WAbO4pdQp8wdnbY3YUpl2ol9mN1B/Jat0mF33s5KJMhHHfwYftvBV9dj5yN9Ed0zkXHj6/g6tYcHjUL7tev1yrivZz0X9wdcZR5mIc9TGuctxL3rsZQ/1ZXY97P8VVylNmXy+oPZqnvPB8YelCINTZ8rzS1MsAj+eVp1zLZXsom/XDVh3AiafrAK17h8v+a6obu8DVrNvop+s2La7zeKPCpavpPKv3vrTO1uSaE/Hy+LDCJSvaFHG9si5a4KLM6av46xZOuTajwJ2NMVl9Pqljz/9Xxy5xsVUWkcsXhs/Z5rpHydlqws3le4eh596hzrVh2Dvu9cCJ5ctTKV+uce0FBHtHALml0yR674nMhXuiRnmTaQL21TdqXGGJozG37/VCkejSvV6DS6Vcp/WoKlfYat6GIU/uYde6hIv7UHrvYVv1aJ1yndUP61x5+kDi/N5cYFIS7783b94KDGldKViL8iV7gyuUobZ/1aV+gP/oc9BERETt6w6hDRERb7ba6/M2aopY6/P8KOefV3vPDPvX/+9LeWpcb1dRWO8HAPjZPqKf7fuCX+3Tg5/tq4Rf7YMFAJDjL/Ytr2hRn7n+xj7zP5d+4MntFElUAAAAAElFTkSuQmCC", "height": 56});')

    def test_nocallback(self):
        # TODO: Change this test after the nocallback error implementation
        view = getMultiAdapter((self.folder, self.request), name='jsonimageserializer')
        url = 'http://old.plone.org/logo.png'
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
