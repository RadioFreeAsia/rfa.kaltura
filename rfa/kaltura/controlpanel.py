from zope import schema
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('rfa.kaltura')


class ISettings(Interface):
    """ Define settings data structure 
          PARTNER_ID = 54321
          SECRET = "YOUR_USER_SECRET"
          ADMIN_SECRET = "YOUR_ADMIN_SECRET"
          SERVICE_URL = "http://www.kaltura.com"
          USER_NAME = "testUser"
    """

    partnerId = schema.TextLine(title=u"Partner Id",
                                description=u"enter your 5-digit Partner ID",
                                required=True,
                                default=u"54321")
    
    secret = schema.TextLine(title=u"User Secret",
                             description=u"enter your 32-character User Secret",
                             required=True,
                             default=u"YOUR_USER_SECRET")
    
    adminSecret = schema.TextLine(title=u"Admin Secret",
                                  description=u"enter your 32-character Admin Secret",
                                  required=True,
                                  default=u"YOUR_ADMIN_SECRET")
    
    serviceUrl =  schema.TextLine(title=u"Service URL",
                                  description=u"enter your service url",
                                  required=True,
                                  default=u"http://www.kaltura.com")
    
    userName = schema.TextLine(title=u"User Name",
                               description=u"enter your username on Kaltura",
                               required=True,
                               default=u"PloneTestUser")
    

class SettingsEditForm(controlpanel.RegistryEditForm):
    schema = ISettings
    label = u"rfa.kaltura settings"
    description = u""""""

class SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SettingsEditForm