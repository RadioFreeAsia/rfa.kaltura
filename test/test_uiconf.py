import fixpypath
from utils import GetConfig
from utils import KalturaBaseTest

import KalturaCoreClient

class UiConfTests(KalturaBaseTest):
     
    def test_list_templates(self):
        templates = self.client.uiConf.listTemplates()
        self.assertIsInstance(templates, KalturaCoreClient.KalturaUiConfListResponse)
        
        objs = templates.objects
        self.assertIsInstance(objs, list)
        
        
        


import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(UiConfTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)