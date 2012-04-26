from plone.app.registry.browser import controlpanel

from collective.upload.interfaces import IUploadSettings, _


class UploadSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IUploadSettings
    label = _(u"Upload settings")
    description = _(u"""""")

    def updateFields(self):
        super(UploadSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(UploadSettingsEditForm, self).updateWidgets()

class UploadSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = UploadSettingsEditForm
