import fixpypath
from utils import GetConfig
from utils import KalturaBaseTest

import KalturaCoreClient
from KalturaClientBase import KalturaObjectFactory

class FlavorAssetTests(KalturaBaseTest):
     
    def test_instantiate(self):
        flavAsst = self.client.flavorAsset
        
    def test_list(self):
        pass
    
        #flavAsstList = flavAsst.list()
        ##TODO - Must set up a Filter and provide entryIdIn to properly test this.
        #self.assertIsInstance(flavAsstList, list)
        
        
        

import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FlavorAssetTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
