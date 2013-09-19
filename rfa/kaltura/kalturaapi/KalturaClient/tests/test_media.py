from utils import GetConfig
from utils import KalturaBaseTest

import KalturaClient.Plugins.Core as KalturaCoreClient
from KalturaClient.Base import KalturaObjectFactory, KalturaEnumsFactory

class MediaTests(KalturaBaseTest):
    
    def test_list(self):
        resp = self.client.media.list()
        self.assertIsInstance(resp, KalturaCoreClient.KalturaMediaListResponse)
        
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
        [self.assertIsInstance(o, KalturaCoreClient.KalturaMediaEntry) for o in objs]


import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(MediaTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)