"""Useful Utils for rfa.kaltura"""
import os
import logging

from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from rfa.kaltura import credentials

from KalturaClient import *

from KalturaClient.Base import IKalturaLogger
from KalturaClient.Base import KalturaConfiguration

from KalturaClient.Plugins.Core import KalturaSessionType
from KalturaClient.Plugins.Core import KalturaPlaylist, KalturaPlaylistType
from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
from KalturaClient.Plugins.Core import KalturaUiConf, KalturaUiConfObjType, KalturaUiConfFilter


logger = logging.getLogger("rfa.kaltura")
logger.setLevel(logging.WARN)

class KalturaLogger(IKalturaLogger):
    def log(self, msg, summary='', level=logging.INFO):
        logger.log(level, '%s \n%s', summary, msg)
        
KalturaLoggerInstance = KalturaLogger()

#@cache me!
def kGetVideoPlayers():
    (client, session) = kconnect()
    
    filt = KalturaUiConfFilter()
    players = [KalturaUiConfObjType.HTML5_PLAYER, 
               KalturaUiConfObjType.PLAYER_V3,
               KalturaUiConfObjType.PLAYER,
               KalturaUiConfObjType.PLAYER_SL,
               ]
    tags = 'player'
        
    filt.setObjTypeIn(players)
    filt.setTagsMultiLikeOr(tags)
       
    resp = self.client.uiConf.list(filter=filt)
    objs = resp.objects
    
    return objs

#@cache me!
def kGetPlaylistPlayers():
    (client, session) = kconnect()
    
    filt = KalturaUiConfFilter()
    players = [KalturaUiConfObjType.HTML5_PLAYER, 
               KalturaUiConfObjType.PLAYER_V3,
               KalturaUiConfObjType.PLAYER,
               KalturaUiConfObjType.PLAYER_SL,
               ]
    tags = 'playlist'
        
    filt.setObjTypeIn(players)
    filt.setTagsMultiLikeOr(tags)
       
    resp = self.client.uiConf.list(filter=filt)
    objs = resp.objects
    
    return objs

def kcreatePlaylist(context):
    """Create an empty playlist on the kaltura server"""
    
    kplaylist = KalturaPlaylist()
    kplaylist.setName(context.Title())
    kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
    
    (client, session) = kconnect()
    
    kplaylist = client.playlist.add(kplaylist)
    
    return kplaylist

def kcreateVideo(context):
    
    mediaEntry = KalturaMediaEntry()
    mediaEntry.setName(context.Title())
    mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
    mediaEntry.searchProviderId = context.UID()
    mediaEntry.setReferenceId = context.UID()
    
    mediaEntry.setCategories(','.join([c for c in context.categories if c]))
    mediaEntry.setTags(','.join([t for t in context.tags if t]))
    
    return mediaEntry
    
    
def kupload(FileObject, mediaEntry=None):
    """Provide an ATCTFileContent based object
       Upload attached contents to Kaltura
       Currently Treats all objects as 'videos' - 
         this should change when other kaltura media types are implemented.
       If MediaEntry is provided, the File is 
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
    
    #XXX Not A good idea if we plan on not using the ZODB
    name = FileObject.Title()
    ProviderId = FileObject.UID()  
     
    (client, session) = kconnect()
    
    if mediaEntry is None:
        #create an entry
        mediaEntry = KalturaMediaEntry()
        mediaEntry.setName(name)
        mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
        mediaEntry.searchProviderId = ProviderId
        mediaEntry.setReferenceId = ProviderId

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