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
from KalturaClient.Base import KalturaException
from KalturaClient.Plugins.Core import KalturaSessionType
from KalturaClient.Plugins.Core import KalturaPlaylist, KalturaPlaylistType
from KalturaClient.Plugins.Core import KalturaMediaEntry, KalturaMediaType
from KalturaClient.Plugins.Core import KalturaUiConf, KalturaUiConfObjType, KalturaUiConfFilter
from KalturaClient.Plugins.Core import KalturaMediaEntryFilter, KalturaMediaEntryFilterForPlaylist
from KalturaClient.Plugins.Core import KalturaMediaEntryOrderBy
from KalturaClient.Plugins.Core import KalturaCategoryFilter
from KalturaClient.Plugins.Core import KalturaCategoryEntry
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

def getTagVids(tags, limit=10, partner_id=None, filt=None):
    """Get all videos that contain one or more querytags
       provide a non-string iterable as tags parameter
       provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    if isinstance(tags, basestring):
        raise TypeError, "tags must be a non-string iterable"
    
    if filt is not None:
        kfilter = copy.copy(filt)
    else:
        kfilter = KalturaMediaEntryFilter()    

    kfilter.setOrderBy(KalturaMediaEntryOrderBy.CREATED_AT_DESC)
    
    try:
        querytags = ','.join(tags)
    except TypeError:
        raise TypeError, "tags must be a non-string iterable"
    
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

def getRelated(kvideoObj, limit=10, partner_id=None, filt=None):
    """ Get videos related to the provided video
        provide 'filt' parameter of an existing KalturaMediaEntryFilter to filter results
    """
    tags = kvideoObj.getTags().split()
    return getTagVids(tags, limit, partner_id, filt)

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
       create a Kaltura MediaEntry object.
       The mediaEntry ReferenceId is set to the UID of the plone object 
       to tie them together
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
       If MediaEntry is provided, the uploaded video is associated with that media entry
    """
    usingEntitlements = False
    
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
    
    os.remove('/tmp/tempfile')
    
    catIds = mediaEntry.getCategoriesIds()
    if catIds is not NotImplemented:
        catIds = catIds.split(',')
        mediaEntry.setCategoriesIds(NotImplemented)
    else:
        catIds = []
    
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

def kdiff(ploneObj, kalturaObj):
    """do a property-to-property match between plone object and kaltura object
       and return property name tuples of fields that differ
       Useful to keep plone and kaltura in sync when edits occur.
    """
    
    def getvals(pFieldName, kFieldName):
        pval = getattr(ploneObj, pFieldName)
        if callable(pval):
            pval = pval()
        kval = getattr(kalturaObj, kFieldName)
        if callable(kval):
            kval = kval()
            
        return (pval, kval)
        
    retval = []
    #supported scalar properties that sync (kalturaVideo(plone), KalturaMediaEntry(kmc))
    scalarFields = [ ('Title', 'getName'),
                     ('Description', 'getDescription'),
                     ('getPartnerId', 'getPartnerId')
                   ]

    for (ploneField, kalturaField) in scalarFields:
        pval, kval = getvals(ploneField, kalturaField)
        if kval != pval:
            retval.append( (ploneField, kalturaField) )

    #compare categories:
    pval = set(ploneObj.getCategories())
    kval = set(kalturaObj.getCategoriesIds().split(','))
    
    if pval != kval:
        retval.append( ('getCategories', 'getCategoriesIds'))

    #compare tags:
    pval = set(ploneObj.getTags())
    kval = set(kalturaObj.getTags().split(','))
    
    if pval != kval:
        retval.append(('getTags', 'getTags'))

    return retval

def kconnect(partner_id=None):
    
    creds = getCredentials()
    if partner_id is not None:
        creds['PARTNER_ID'] = partner_id
    
    privacyString = ''    

    #may want to add 'disableentitlements' to the privacyString eventuall for users who want to
    # disable all entitlement checking
    if creds.get('PRIVACY_CONTEXT', '') not in ('', None):
        privacyString = 'privacycontext:' + creds['PRIVACY_CONTEXT']
        
    
    config = KalturaConfiguration(creds['PARTNER_ID'])
    config.serviceUrl = creds['SERVICE_URL']
    config.setLogger(KalturaLoggerInstance)
        
    client = KalturaClient(config)
    
    # start new session
    ks = client.generateSession(creds['ADMIN_SECRET'], 
                                creds['USER_NAME'],
                                KalturaSessionType.ADMIN, 
                                creds['PARTNER_ID'],
                                86400,
                                privacyString)
    client.setKs(ks)    
    
    return (client, ks)

    
    
    
    