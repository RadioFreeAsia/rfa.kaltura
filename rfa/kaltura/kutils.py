"""Useful Utils for rfa.kaltura"""
import os
import logging

from Products.CMFCore.utils import getToolByName

from rfa.kaltura import credentials

from KalturaClient import *

from KalturaClient.Base import IKalturaLogger
from KalturaClient.Base import KalturaConfiguration

from KalturaClient.Plugins.Core import KalturaSessionType
from KalturaClient.Plugins.Core import KalturaPlaylist, KalturaPlaylistType
from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType


logger = logging.getLogger("rfa.kaltura")
logger.setLevel(logging.WARN)

class KalturaLogger(IKalturaLogger):
    def log(self, msg, summary='', level=logging.INFO):
        logger.log(level, '%s \n%s', summary, msg)
        
KalturaLoggerInstance = KalturaLogger()

def kcreatePlaylist(FolderishObject):
    """Create an empty playlist on the kaltura server"""
    
    kplaylist = KalturaPlaylist()
    kplaylist.setName(FolderishObject.Title())
    kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
    
    (client, session) = kconnect()
    
    kplaylist = client.playlist.add(kplaylist)
    
    return kplaylist

def kupload(FileObject):
    """Provide an ATCTFileContent based object
       Upload attached contents to Kaltura
       Currently Treats all objects as 'videos' - 
         this should change when other kaltura media types are implemented.
    """
    
    #this check can be done better
    if not hasattr(FileObject, 'get_data'):
        print "nothing to upload to kaltura from object %s" % (str(FileObject),)
        return 1;
    
    #XXX Configure Temporary Directory and name better
    #XXX Turn into a file stream from context.get_data to avoid write to file...        
    tempfh = open('/tmp/tempfile', 'wr')
    tempfh.write(FileObject.get_data())
    tempfh.close()    
    
    name = FileObject.Title()
    ProviderId = FileObject.UID()
     
    (client, session) = kconnect()
    
    #create an entry
    mediaEntry = KalturaMediaEntry()
    mediaEntry.setName(name)
    mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
    mediaEntry.searchProviderId = ProviderId

    #do the upload
    
    uploadTokenId = client.media.upload(file('/tmp/tempfile', 'rb'))  
    
    #del the temp file
    os.remove('/tmp/tempfile')
    
    mediaEntry = client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
    
    KalturaLoggerInstance.log("uploaded.  MediaEntry %s" % (mediaEntry.__repr__()))        
    return mediaEntry

def kconnect():
    
    creds = credentials.getCredentials()
    
    config = KalturaConfiguration(creds['PARTNER_ID'])
    config.serviceUrl = creds['SERVICE_URL']
    config.setLogger(KalturaLoggerInstance)
        
    client = KalturaClient(config)
    
    # start new session
    ks = client.generateSession(creds['ADMIN_SECRET'], 
                                creds['USER_NAME'],
                                KalturaSessionType.ADMIN, 
                                creds['PARTNER_ID'],
                                86400,   #XXX look up what this does...
                                "")    
    client.setKs(ks)    
    
    return (client, ks)