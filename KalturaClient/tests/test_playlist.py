from utils import GetConfig
from utils import KalturaBaseTest
from utils import getTestFile

from KalturaClient.Plugins.Core import KalturaPlaylist, KalturaPlaylistType
from KalturaClient.Plugins.Core import KalturaPlaylistListResponse

class PlaylistTests(KalturaBaseTest):
     
    def test_instantiate(self):
        playlist = self.client.playlist
        
    def test_list(self):
        resp = self.client.playlist.list()
    
        self.assertIsInstance(resp, KalturaPlaylistListResponse)
                
        objs = resp.objects
        self.assertIsInstance(objs, list)
        
        [self.assertIsInstance(o, KalturaPlaylist) for o in objs] 
        
    def test_createRemote(self):
        kplaylist = KalturaPlaylist()
        kplaylist.setName('pytest.PlaylistTests.test_createRemote')
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST)) #??? STATIC LIST ???
        
        kplaylist = self.client.playlist.add(kplaylist)        
        self.assertIsInstance(kplaylist, KalturaPlaylist)
        
        self.assertIsInstance(kplaylist.getId(), unicode)
        
        #cleanup
        self.client.playlist.delete(kplaylist.getId())
        
    #def test_listEntries(self):
    #    playlistId = '1_qv2ed7vm'
    #    kplaylist = self.client.playlist.get(playlistId)
    #    assertIsInstance(kplaylist.playlistContent, unicode)
    #    assertIsInstance(kplaylist.playlistContent.split(','), list)
        
        
    def test_addStaticContent(self):        
                
        from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
        
        mediaEntry1 = KalturaMediaEntry()
        mediaEntry1.setName('pytest.PlaylistTests.test_createStaticContent1')
        mediaEntry1.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry1 = self.client.media.addFromUploadedFile(mediaEntry1, uploadTokenId)
        
        self.addCleanup(self.client.media.delete, mediaEntry1.getId())
                
        mediaEntry2 = KalturaMediaEntry()
        mediaEntry2.setName('pytest.PlaylistTests.test_createStaticContent2')
        mediaEntry2.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry2 = self.client.media.addFromUploadedFile(mediaEntry2, uploadTokenId)        
        
        self.addCleanup(self.client.media.delete, mediaEntry2.getId())
        
        #playlistContent is simply a comma separated string of id's
        playlistContent = u','.join([mediaEntry1.getId(), mediaEntry2.getId()])
                        
        kplaylist = KalturaPlaylist()
        kplaylist.setName('pytest.PlaylistTests.test_createStaticContent')
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST)) #??? STATIC LIST ???        
        
        kplaylist.playlistContent = playlistContent        
        kplaylist = self.client.playlist.add(kplaylist)
        
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())
        
        #fetch the playlist from server and test it's content.
        resultPlaylist = self.client.playlist.get(kplaylist.getId())
        self.assertEqual(resultPlaylist.playlistContent, playlistContent)
        
        #import pdb; pdb.set_trace()  #go check your server
        
        

import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PlaylistTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
