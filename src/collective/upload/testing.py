# -*- coding: utf-8 -*-
"""Setup test fixtures.

We have to set different test fixtures depending on features we want:

plone.app.contenttypes:
    installed under Plone 4.3, if requested
"""
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os
import pkg_resources
import shutil
import tempfile


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
    DEXTERITY_ONLY = False
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
    DEXTERITY_ONLY = True


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        """Copy all files used in tests to the temporary directory."""
        super(Fixture, self).setUp()
        tempdir = tempfile.gettempdir()
        path = os.path.join(os.path.dirname(__file__), 'tests')
        for i in os.listdir(path):
            if i.endswith('.jpg'):
                shutil.copy(os.path.join(path, i), tempdir)

    def setUpZope(self, app, configurationContext):
        import collective.upload
        self.loadZCML(package=collective.upload)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.upload:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.upload:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.upload:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.upload:Robot',
)
