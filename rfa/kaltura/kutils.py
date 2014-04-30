"""Useful Utils for rfa.kaltura"""
import os
import sys
import logging
import copy

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

from rfa.kaltura import credentials
from rfa.kaltura.config import DEFAULT_DYNAMIC_PLAYLIST_SIZE
from rfa.kaltura.interfaces import IKalturaRuleBasedPlaylist, IKalturaManualPlaylist

from KalturaClient import *
from KalturaClient.Base import IKalturaLogger
from KalturaClient.Base import KalturaConfiguration
from KalturaClient.Plugins.Core import KalturaSessionType
from KalturaClient.Plugins.Core import KalturaPlaylist, KalturaPlaylistType
from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
from KalturaClient.Plugins.Core import KalturaUiConf, KalturaUiConfObjType, KalturaUiConfFilter
from KalturaClient.Plugins.Core import KalturaMediaEntryFilter, KalturaMediaEntryFilterForPlaylist
from KalturaClient.Plugins.Core import KalturaMediaEntryOrderBy
from KalturaClient.Plugins.Core import KalturaCategoryFilter
from KalturaClient.Plugins.Core import KalturaSearchOperator


logger = logging.getLogger("rfa.kaltura")
logger.setLevel(logging.WARN)

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(message)s',
                    stream = sys.stdout)

#editable for testing purposes
getCredentials = credentials.getCredentials

class KalturaLogger(IKalturaLogger):
    def log(self, msg):
        logging.info(msg)

#class KalturaLogger(IKalturaLogger):
#    def log(self, msg, summary='', level=logging.INFO):
#        logger.log(level, '%s \n%s', summary, msg)
        
KalturaLoggerInstance = KalturaLogger()

#@cache me?
def kGetVideoPlayers():
    (client, session) = kconnect()
    
    filt = KalturaUiConfFilter()
    players = [KalturaUiConfObjType.PLAYER_V3,
               KalturaUiConfObjType.PLAYER,
               KalturaUiConfObjType.PLAYER_SL,
               ]
    tags = 'player'
        
    filt.setObjTypeIn(players)
    filt.setTagsMultiLikeOr(tags)
    resp = client.uiConf.list(filter=filt)
    objs = resp.objects
    
    return objs

#@cache me?
def kGetPlaylistPlayers():
    (client, session) = kconnect()
    
    filt = KalturaUiConfFilter()
    players = [KalturaUiConfObjType.PLAYER_V3,]
    tags = 'playlist'
        
    filt.setObjTypeIn(players)
    filt.setTagsMultiLikeOr(tags)
       
    resp = client.uiConf.list(filter=filt)
    objs = resp.objects
    
    return objs

def getVideo(videoId):
    (client, session) = kconnect()
    result = client.media.get(videoId)
    return result

def makeFilter(catIds=None, tagIds=None, order=None):
    """Helper function for creating KalturaMediaEntryFilters
    """
    kfilter = KalturaMediaEntryFilter()

    if order is not None:
        kfilter.setOrderBy(order)
    
    if catIds is not None:
        if isinstance(catIds, list) or isinstance(catIds, tuple):
            catIds = ','.join(catIds)   
        kfilter.setCategoryAncestorIdIn(catIds)
        
    return kfilter
    #if tagIds is not None....

def getRecent(limit=10, partner_id=None, filt=None):
    """Get the most recently uploaded videos
       provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    if filt is not None:
        kfilter = copy.copy(filt)
    else:
        kfilter = KalturaMediaEntryFilter()
    kfilter.setOrderBy(KalturaMediaEntryOrderBy.CREATED_AT_DESC)
    (client, session) = kconnect(partner_id)
    result = client.media.list(filter=kfilter)
    return result.objects

def getMostViewed(limit=10, partner_id=None, filt=None):
    """Get videos ranked by views
       provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    if filt is not None:
        kfilter = copy.copy(filt)
    else:
        kfilter = KalturaMediaEntryFilter()
    kfilter.setOrderBy(KalturaMediaEntryOrderBy.VIEWS_DESC)
    (client, session) = kconnect(partner_id)
    result = client.media.list(filter=kfilter)
    return result.objects

def getRelated(kvideoObj, limit=10, partner_id=None, filt=None):
    """ Get videos related to the provided video
        provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    if filt is not None:
        kfilter = copy.copy(filt)
    else:
        kfilter = KalturaMediaEntryFilter()
        
    kfilter.setOrderBy(KalturaMediaEntryOrderBy.CREATED_AT_DESC)
    
    #take the whitespace delimited string tags from the object, 
    #and turn it into a comma delimited string for the query
    querytags = ','.join(kvideoObj.getTags().split())
    
    kfilter.setTagsMultiLikeOr(querytags)
    (client, session) = kconnect(partner_id)
    result = client.media.list(filter=kfilter)
    return result.objects

def getCategoryVids(catId, limit=10, partner_id=None, filt=None):
    """ Get videos placed in the provided category id, or child categories
        provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    if filt is not None:
        kfilter = copy.copy(filt)
    else:
        kfilter = KalturaMediaEntryFilter()
    kfilter.setOrderBy(KalturaMediaEntryOrderBy.CREATED_AT_DESC)
    kfilter.setCategoryAncestorIdIn(catId)
    (client, session) = kconnect(partner_id)
    result = client.media.list(filter=kfilter)
    return result.objects

def kcreateEmptyFilterForPlaylist():
    """Create a Playlist Filter, filled in with default, required values"""
    #These were mined by reverse-engineering a playlist created on the KMC and inspecting the object
    kfilter = KalturaMediaEntryFilterForPlaylist()
    
    kfilter.setLimit(30)
    kfilter.setModerationStatusIn(u'2,5,6,1')
    kfilter.setOrderBy(u'-plays')
    kfilter.setStatusIn(u'2,1')
    kfilter.setTypeIn(u'1,2,7')
    
    return kfilter   

def kcreatePlaylist(context):
    """Create an empty playlist on the kaltura server"""
    
    kplaylist = KalturaPlaylist()
    kplaylist.setName(context.Title())
    kplaylist.setDescription(context.Description())
    kplaylist.setReferenceId(context.UID())
    
    if IKalturaManualPlaylist.providedBy(context):
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.STATIC_LIST))
    elif IKalturaRuleBasedPlaylist.providedBy(context):
        kplaylist.setPlaylistType(KalturaPlaylistType(KalturaPlaylistType.DYNAMIC))
        maxVideos = getattr(context, 'maxVideos', DEFAULT_DYNAMIC_PLAYLIST_SIZE)
        kplaylist.setTotalResults(maxVideos)
        kfilter = kcreateEmptyFilterForPlaylist()
        kfilter.setFreeText(u','.join(context.getTags()))

        kfilter.setCategoriesIdsMatchOr(u','.join(context.getCategories()))
        kplaylist.setFilters([kfilter])
    else:
        raise AssertionError, "%s is not a known playlist type" % (context.portal_type,)
    
    (client, session) = kconnect()
    
    kplaylist = client.playlist.add(kplaylist)
    
    return kplaylist

def kcreateVideo(context):
    """given a plone content-type of kalturavideo,
       create a video entry on Kaltura
       The mediaEntry ReferenceId is set to the UID of the plone object to tie them together
    """
    mediaEntry = KalturaMediaEntry()
    mediaEntry.setName(context.Title())
    mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
    mediaEntry.searchProviderId = context.UID() #XXX Is this correct?  We assign this to the file UID stored in plone.
    
    #kaltura referenceId == plone UID
    mediaEntry.setReferenceId(context.UID())
    
    if len(context.getCategories()):
        mediaEntry.setCategoriesIds(','.join([c for c in context.getCategories() if c]))
        
    if len(context.getTags()):
        mediaEntry.setTags(','.join([t for t in context.getTags() if t]))
    
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

#XXX cacheme for a few mins
def kGetCategories(parent=None):
    (client, session) = kconnect()
    
    if parent is not None:
        filt = KalturaCategoryFilter()
        filt.setAncestorIdIn(parent)
    else:
        filt = None
    
    result = client.category.list(filter=filt).objects
    return result

def kGetCategoryId(categoryName):
    """ provide a categoryName (string) and this will return it's Id on the kaltura server"""
    categoryObjs = kGetCategories()
    for cat in categoryObjs:
        if cat.getName() == categoryName:
            return cat.getId()
        
    return None

def kconnect(partner_id=None):
    
    creds = getCredentials()
    if partner_id is not None:
        creds['PARTNER_ID'] = partner_id
    
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

