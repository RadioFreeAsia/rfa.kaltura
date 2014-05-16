
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from rfa.kaltura.controlpanel import IRfaKalturaSettings

def getCredentials():
    creds = {}
    
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IRfaKalturaSettings)

    creds['PARTNER_ID'] = settings.partnerId
    creds['SECRET'] = settings.secret
    creds['ADMIN_SECRET'] = settings.adminSecret
    creds['SERVICE_URL'] = settings.serviceUrl
    creds['USER_NAME'] = settings.userName
    creds['PRIVACY_CONTEXT'] = settings.privacyContextString
 
    return creds

