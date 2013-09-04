from secret_config import PARTNER_ID, SERVICE_URL, SECRET, ADMIN_SECRET, USER_NAME

from KalturaClient import KalturaClient
from KalturaClientBase import KalturaConfiguration
from KalturaCoreClient import KalturaSessionType
from KalturaClientBase import KalturaObjectFactory, KalturaEnumsFactory
from KalturaCoreClient import KalturaMediaType

import unittest

def GetConfig():
    config = KalturaConfiguration(PARTNER_ID)
    config.serviceUrl = SERVICE_URL
    #config.setLogger(KalturaLogger())
    return config

class KalturaBaseTest(unittest.TestCase):
    """Base class for all Kaltura Tests"""
    #TODO  create a client factory as to avoid thrashing kaltura with logins...
    
    def setUp(self):
        self.config = GetConfig()
        self.client = KalturaClient(self.config)
        self.ks = self.client.generateSession(ADMIN_SECRET, USER_NAME, 
                                             KalturaSessionType.ADMIN, PARTNER_ID, 
                                             86400, "")
        self.client.setKs(self.ks)            
            
    def tearDown(self):        
        self.config = None
        self.client = None
        self.ks = None    