"""Common configuration constants
"""

PROJECTNAME = 'rfa.kaltura'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'KalturaVideo': 'rfa.kaltura: Add Kaltura Video',
}


#Kaltura Account Information
#kaltura_secret_config should be set as svn:ignore in your repo - just a suggestion
try:
    from kaltura_secret_config import PARTNER_ID, SECRET, ADMIN_SECRET, SERVICE_URL, USER_NAME
except ImportError:
    # UPDATE THIS
    PARTNER_ID = 54321
    SECRET = "YOUR_USER_SECRET"
    ADMIN_SECRET = "YOUR_ADMIN_SECRET"
    SERVICE_URL = "http://www.kaltura.com"
    USER_NAME = "testUser"

