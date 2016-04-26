# -*- coding: utf-8 -*-
"""Setup test fixtures.

We have to set different test fixtures depending on features we want:

plone.app.contenttypes:
    installed under Plone 4.3, if requested
"""
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os
import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    DEXTERITY_ONLY = False
else:
    # this environment variable is set in .travis.yml test matrix
    DEXTERITY_ONLY = os.environ.get('DEXTERITY_ONLY') is not None


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if DEXTERITY_ONLY:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
            z2.installProduct(app, 'Products.DateRecurringIndex')

        import collective.upload
        self.loadZCML(package=collective.upload)

    def setUpPloneSite(self, portal):
        if DEXTERITY_ONLY:
            self.applyProfile(portal, 'plone.app.contenttypes:default')

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
