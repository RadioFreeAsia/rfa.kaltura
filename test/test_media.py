import fixpypath
from utils import GetConfig
from utils import KalturaBaseTest

import KalturaCoreClient
from KalturaClientBase import KalturaObjectFactory, KalturaEnumsFactory

class MediaTests(KalturaBaseTest):
    
    def test_list(self):
        resp = self.client.media.list()
        self.assertIsInstance(resp, KalturaCoreClient.KalturaMediaListResponse)
        
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
        [assertIsInstance(o, KalturaCoreClient.KalturaMediaEntry) for o in objs]


import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(MediaTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)