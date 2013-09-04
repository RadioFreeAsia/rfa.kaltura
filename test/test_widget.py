import unittest

import os

###test inits
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

###Utils
from secret_config import PARTNER_ID, SERVICE_URL, SECRET, ADMIN_SECRET, USER_NAME


from KalturaClientBase import KalturaConfiguration

def GetConfig():
    config = KalturaConfiguration(PARTNER_ID)
    config.serviceUrl = SERVICE_URL
    #config.setLogger(KalturaLogger())
    return config


from KalturaClient import KalturaClient
from KalturaCoreClient import KalturaSessionType
from KalturaClientBase import KalturaObjectFactory, KalturaEnumsFactory
from KalturaCoreClient import KalturaMediaType

class WidgetTests(unittest.TestCase):
    
    def setUp(self):
        self.config = GetConfig()
        self.client = KalturaClient(self.config)
        ks = self.client.generateSession(ADMIN_SECRET, USER_NAME, 
                                         KalturaSessionType.ADMIN, PARTNER_ID, 
                                         86400, "")
        self.client.setKs(ks)            
        
    def tearDown(self):        
        self.config = None
        
    def test_list_widgets(self):
        widgets = self.client.widget.list()
        
        
        
    


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(WidgetTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    