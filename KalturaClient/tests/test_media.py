from utils import GetConfig
from utils import KalturaBaseTest
from utils import getTestFile

import KalturaClient.Plugins.Core as KalturaCoreClient



class MediaTests(KalturaBaseTest):
    
    def test_list(self):
        resp = self.client.media.list()
        self.assertIsInstance(resp, KalturaCoreClient.KalturaMediaListResponse)
        
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
        [self.assertIsInstance(o, KalturaCoreClient.KalturaMediaEntry) for o in objs]
        

    def test_createRemote(self):
        mediaEntry = KalturaCoreClient.KalturaMediaEntry()
        mediaEntry.setName('pytest.MediaTests.test_createRemote')
        mediaEntry.setMediaType(KalturaCoreClient.KalturaMediaType(KalturaCoreClient.KalturaMediaType.VIDEO))
            
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile)            
                     
        mediaEntry = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
        
        #delete it
        self.client.media.delete(mediaEntry.id)
        


import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(MediaTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)