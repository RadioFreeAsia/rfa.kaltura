from utils import GetConfig
from utils import KalturaBaseTest

import KalturaClient.Plugins.Core as KalturaCoreClient
from KalturaClient.Base import KalturaObjectFactory

class PlaylistTests(KalturaBaseTest):
     
    def test_instantiate(self):
        playlist = self.client.playlist
        
    def test_list(self):
        resp = self.client.playlist.list()
    
        self.assertIsInstance(resp, KalturaCoreClient.KalturaPlaylistListResponse)
                
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
        [self.assertIsInstance(o, KalturaCoreClient.KalturaPlaylist) for o in objs]            
        
        

import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PlaylistTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
