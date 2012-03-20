# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import button

from plone.app.registry.browser import controlpanel

from collective.printout.interfaces import IPrintoutSettings, _


class PrintoutSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IPrintoutSettings
    label = _(u"Printout settings")
    description = _(u"""""")

    def updateFields(self):
        super(PrintoutSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(PrintoutSettingsEditForm, self).updateWidgets()
        self.widgets['default_template'].rows = 40
        self.widgets['default_body_stylesheet'].rows = 40

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@printout-settings")
    
    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class PrintoutSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PrintoutSettingsEditForm
    index = ViewPageTemplateFile('controlpanel.pt')
        