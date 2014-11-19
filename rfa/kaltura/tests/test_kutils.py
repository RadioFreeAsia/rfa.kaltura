"""Testing of kutils
   Run this with zope's testing infrastructure
   ./bin/test rfa.kaltura
"""

import unittest

from rfa.kaltura import kutils

from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType

#use some of the kalturaapi test utilities
from KalturaClient.tests.utils import KalturaBaseTest
from KalturaClient.tests.utils import getTestFile

#These tests should not try to connect to a Kaltura Server
#But when that design is violated:
#make sure kalturaapi.KalturaClient.tests.secret_config.py is created
from KalturaClient.tests.utils import PARTNER_ID, SERVICE_URL, SECRET, ADMIN_SECRET, USER_NAME

def getTestCredentials():
    creds = {}

    creds['PARTNER_ID'] = PARTNER_ID
    creds['SECRET'] = SERVICE_URL
    creds['ADMIN_SECRET'] = ADMIN_SECRET
    creds['SERVICE_URL'] = SERVICE_URL
    creds['USER_NAME'] = USER_NAME
 
    return creds

#Monkey patch the 'getCredentials' to use our test config.    
kutils.getCredentials = getTestCredentials

class GetRelatedTests(KalturaBaseTest):
    """exercises the functionality of kutils.getRelated()"""
    
    def testTwoTags(self):
        """Places 3 videos on the server:
           one with two tags: 'tag1' and 'tag2'
           one with the tag 'tag1'
           one with the tag 'tag2'
           
           the kalutra object with two tags is provided to 'getRelated'
           
           we expect to get all three objects back from getRelated
        """
        
        #MediaEntry1
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName('rfa.kaltura.GetRelatedTests.testTwoTags1')
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile)
        mediaEntry.setTags(u'tag1 tag2')
        mediaEntry1 = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
        self.addCleanup(self.client.media.delete, mediaEntry1.getId())
        
        #MediaEntry2
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName('rfa.kaltura.GetRelatedTests.testTwoTags2')
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile)
        mediaEntry.setTags(u'tag1')
        mediaEntry2 = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
        self.addCleanup(self.client.media.delete, mediaEntry2.getId())
        
        #MediaEntry3
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName('rfa.kaltura.GetRelatedTests.testTwoTags3')
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        ulFile = getTestFile('DemoVideo.flv')
        uploadTokenId = self.client.media.upload(ulFile)
        mediaEntry.setTags(u'tag2')
        mediaEntry3 = self.client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
        self.addCleanup(self.client.media.delete, mediaEntry3.getId())
        
        self.readyWait(mediaEntry1.getId())
        self.readyWait(mediaEntry2.getId())
        self.readyWait(mediaEntry3.getId())
        
        #do it.
        results = kutils.getRelated(mediaEntry1)
        self.assertEqual(3,
                         len(results),
                         "Did not get expected # of objects back from kutils.getRelated()")
                         
                         
        


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(GetRelatedTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)


