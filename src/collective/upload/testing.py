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


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
    DEXTERITY_ONLY = False
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
    DEXTERITY_ONLY = True


IMAGES = [
    'Belem.jpg',
    '640px-Mandel_zoom_00_mandelbrot_set.jpg',
    '640px-Mandel_zoom_04_seehorse_tail.jpg',
    '640px-Mandel_zoom_06_double_hook.jpg',
    '640px-Mandel_zoom_07_satellite.jpg',
    '640px-Mandel_zoom_12_satellite_spirally_wheel_with_julia_islands.jpg'
]


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.upload
        self.loadZCML(package=collective.upload)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.upload:default')

        current_dir = os.path.abspath(os.path.dirname(__file__))
        for img in IMAGES:
            img_path = os.path.join(current_dir, 'tests', img)
            shutil.copy2(img_path, '/tmp')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.upload:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.upload:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.upload:Robot',
)
