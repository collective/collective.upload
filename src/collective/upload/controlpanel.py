# -*- coding: utf-8 -*-

from plone.app.registry.browser import controlpanel

from collective.upload import _
from collective.upload.interfaces import IUploadSettings


class UploadSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IUploadSettings
    label = _(u"Upload settings")
    description = _(u"Here you can modify the settings for collective.upload")

    def updateFields(self):
        super(UploadSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(UploadSettingsEditForm, self).updateWidgets()


class UploadSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = UploadSettingsEditForm
