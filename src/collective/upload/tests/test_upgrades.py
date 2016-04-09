# -*- coding: utf-8 -*-
from collective.upload.testing import INTEGRATION_TESTING
from collective.upload.upgrades.v3 import FIX_CSS
from collective.upload.upgrades.v3 import FIX_JS
from plone import api

import unittest


class BaseUpgradeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.upload:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step_by_title(self, title):
        """Return the upgrade step that matches the title specified.

        :param title: the title used to register the upgrade step
        :type title: str
        :returns: an upgrade step or None if there is no match
        :rtype: dict
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        :param step: the step we want to run
        :type step: dict
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def _get_registered_steps(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class To2TestCase(BaseUpgradeTestCase):

    def setUp(self):
        BaseUpgradeTestCase.setUp(self, u'1', u'2')

    def test_registered_steps(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._get_registered_steps, 2)

    def test_update_rolemap(self):
        # check if the upgrade step is registered
        title = u'Update role map'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        portal = api.portal.get()
        permission = 'collective.upload: Setup'
        # XXX: is there any other way to do this?
        portal._collective_upload__Setup_Permission = ()

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        roles = portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_update_configlet(self):
        # check if the upgrade step is registered
        title = u'Update control panel configlet'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        cptool = api.portal.get_tool('portal_controlpanel')
        configlet = cptool.getActionObject('Products/upload')
        configlet.permissions = old_permissions = ('cmf.ManagePortal',)
        self.assertEqual(configlet.getPermissions(), old_permissions)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        configlet = cptool.getActionObject('Products/upload')
        new_permissions = ('collective.upload: Setup',)
        self.assertEqual(configlet.getPermissions(), new_permissions)


class To3TestCase(BaseUpgradeTestCase):

    def setUp(self):
        BaseUpgradeTestCase.setUp(self, u'2', u'3')

    def test_registered_steps(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._get_registered_steps, 4)

    def test_fix_resources_references(self):
        # check if the upgrade step is registered
        title = u'Fix resource references'
        step = self._get_upgrade_step_by_title(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        css_tool = api.portal.get_tool('portal_css')
        css_tool.renameResource(FIX_CSS['new'], FIX_CSS['old'])
        self.assertIn(FIX_CSS['old'], css_tool.getResourceIds())
        self.assertNotIn(FIX_CSS['new'], css_tool.getResourceIds())
        js_tool = api.portal.get_tool('portal_javascripts')
        js_tool.renameResource(FIX_JS['new'], FIX_JS['old'])
        self.assertIn(FIX_JS['old'], js_tool.getResourceIds())
        self.assertNotIn(FIX_JS['new'], js_tool.getResourceIds())

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertNotIn(FIX_CSS['old'], css_tool.getResourceIds())
        self.assertIn(FIX_CSS['new'], css_tool.getResourceIds())
        self.assertNotIn(FIX_JS['old'], js_tool.getResourceIds())
        self.assertIn(FIX_JS['new'], js_tool.getResourceIds())
