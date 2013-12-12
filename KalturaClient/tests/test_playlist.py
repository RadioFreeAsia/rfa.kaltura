import time

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
        
        
        
    def test_update(self):
        referenceId = 'pytest.PlaylistTests.test_update'
        
        kplaylist = KalturaPlaylist()
        kplaylist.setName(referenceId)
        kplaylist.setReferenceId(referenceId)
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
        kplaylist = self.client.playlist.add(kplaylist)        
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())

        newPlaylist = KalturaPlaylist()        
        newPlaylist.setReferenceId(referenceId)
        newPlaylist.setName("changed!")
        self.client.playlist.update(kplaylist.getId(), newPlaylist)
        
        resultPlaylist = self.client.playlist.get(kplaylist.getId())
        self.assertEqual("changed!", resultPlaylist.getName())
        
    def test_updateStaticContent(self):        
                
        from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
        
        mediaEntry1 = KalturaMediaEntry()
        mediaEntry1.setName('pytest.PlaylistTests.test_updateStaticContent1')
        mediaEntry1.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry1 = self.client.media.addFromUploadedFile(mediaEntry1, uploadTokenId)
        
        self.addCleanup(self.client.media.delete, mediaEntry1.getId())
                
        mediaEntry2 = KalturaMediaEntry()
        mediaEntry2.setName('pytest.PlaylistTests.test_updateStaticContent2')
        mediaEntry2.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry2 = self.client.media.addFromUploadedFile(mediaEntry2, uploadTokenId)        
        
        self.addCleanup(self.client.media.delete, mediaEntry2.getId())
        
        #playlistContent is simply a comma separated string of id's ?  
        playlistContent = u','.join([mediaEntry1.getId(), mediaEntry2.getId()])
                        
        kplaylist = KalturaPlaylist()
        kplaylist.setName('pytest.PlaylistTests.test_updateStaticContent')
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
        
        kplaylist.setPlaylistContent(playlistContent)
        kplaylist = self.client.playlist.add(kplaylist)
        
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())
        
        #fetch the playlist from server and test it's content.
        resultPlaylist = self.client.playlist.get(kplaylist.getId())
        self.assertEqual(resultPlaylist.playlistContent, playlistContent)
        
        #import pdb; pdb.set_trace()  #go check your server
        
        
    def test_addStaticToExistingEmpty(self):
        from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
        referenceId = 'pytest.PlaylistTests.test_addStaticToExistingEmpty'
        #create empty playlist on server
        kplaylist = KalturaPlaylist()
        kplaylist.setName(referenceId)
        kplaylist.setReferenceId(referenceId)
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
        kplaylist = self.client.playlist.add(kplaylist)
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())
        
        playlistId = kplaylist.getId()
        
        #now, add some media
        
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName(referenceId)
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)         
        self.addCleanup(self.client.media.delete, mediaEntry.getId())
        
        #add to (update) existing playlist
        newplaylist = KalturaPlaylist()
        newplaylist.setReferenceId(referenceId)
    
        playlistContent = u','.join([mediaEntry.getId()])
        newplaylist.setPlaylistContent(playlistContent)
        
        self.client.playlist.update(playlistId, newplaylist)
        
        #check it.
        resultPlaylist = self.client.playlist.get(playlistId)
        
        self.assertEqual(playlistContent, resultPlaylist.getPlaylistContent())
        
        
        
    def test_updateExceptionReferenceIdNotSet(self):
        from KalturaClient.Base import KalturaException
        
        kplaylist = KalturaPlaylist()
        kplaylist.setName('pytest.PlaylistTests.test_updateExceptionReferenceIdNotSet')
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
        kplaylist = self.client.playlist.add(kplaylist)
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())
        
        playlistId = kplaylist.getId()
        
        playlist = self.client.playlist.get(playlistId)
        
        #don't set referenceId
        
        self.assertRaises(KalturaException, self.client.playlist.update, playlistId, playlist) 
    
class DynamicPlaylistTests(KalturaBaseTest):
    
    def test_createRemote(self):
        kplaylist = KalturaPlaylist()
        kplaylist.setName('pytest.PlaylistTests.test_createRemote')
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.DYNAMIC))
        
        #must add a totalResults field
        kplaylist.setTotalResults(10)
        
        kplaylist = self.client.playlist.add(kplaylist)        
        self.assertIsInstance(kplaylist, KalturaPlaylist)
        
        self.assertIsInstance(kplaylist.getId(), unicode)
        
        #cleanup
        self.client.playlist.delete(kplaylist.getId())        
        
    def test_createTagRule(self):
        from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
        from KalturaClient.Plugins.Core import KalturaMediaEntryFilterForPlaylist
        
        referenceId = 'pytest.DynamicPlaylistTests.test_createTagRule'
        
        #create a video, and put a tag on it.
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName(referenceId)
        mediaEntry.setReferenceId(referenceId)
        mediaEntry.setTags('footag')
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile) 
        mediaEntry = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)         
        self.addCleanup(self.client.media.delete, mediaEntry.getId())    
        
        #create a playlist
        kplaylist = KalturaPlaylist()
        kplaylist.setName(referenceId)
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.DYNAMIC))
        kplaylist.setTotalResults(10)
        kplaylist.setReferenceId(referenceId)
        
        #create a filter for the playlist
        playlistFilter = KalturaMediaEntryFilterForPlaylist()
        playlistFilter.setTagsMultiLikeOr('footag')

        filtersArray = [playlistFilter,]
        
        kplaylist.setFilters(filtersArray)

        kplaylist = self.client.playlist.add(kplaylist)
        self.addCleanup(self.client.playlist.delete, kplaylist.getId())
        
        ######you want to wait for some unspecified amount of time
        sleeptime=30
        print "SLEEPING FOR %s Seconds before retrieving results" % (sleeptime)
        time.sleep(sleeptime)
        # NEED BETTER CODE HERE!!!!
        #######
        
        results = self.client.playlist.execute(kplaylist.getId(), kplaylist)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getName(), referenceId)
        
        
        
import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(PlaylistTests),
        unittest.makeSuite(DynamicPlaylistTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)
