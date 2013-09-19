from utils import GetConfig
from utils import KalturaBaseTest

import KalturaClient.Plugins.Core as KalturaCoreClient
from KalturaClient.Base import KalturaObjectFactory, KalturaEnumsFactory

class UiConfTests(KalturaBaseTest):
     
    def test_list(self):
        resp = self.client.uiConf.list()
        self.assertIsInstance(resp, KalturaCoreClient.KalturaUiConfListResponse)
        
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
    def test_get_players(self):
        KalturaUiConfObjType = KalturaEnumsFactory.enumFactories['KalturaUiConfObjType']
        filt = KalturaObjectFactory.objectFactories['KalturaUiConfFilter']()
        
        players = [KalturaUiConfObjType.HTML5_PLAYER, 
                   KalturaUiConfObjType.PLAYER_V3,
                   KalturaUiConfObjType.PLAYER,
                   KalturaUiConfObjType.PLAYER_SL,
                  ]
        filt.setObjTypeIn(players)
       
        resp = self.client.uiConf.list(filter=filt)
        objs = resp.objects
        
        for o in objs:
            self.assertIn(o.objType.getValue(), players)
        
     
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