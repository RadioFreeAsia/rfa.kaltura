"""Definition of the Kaltura Video content type
"""

from zope.interface import implements
from zope.interface import directlyProvides
from ZODB.interfaces import IStorage

from zope.component import getUtility

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.Archetypes.atapi import AnnotationStorage
from Products.ATContentTypes.interface.file import IATFile
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interface.file import IFileContent
from Products.validation import V_REQUIRED
from Products.Archetypes.Marshall import RFC822Marshaller

from plone.app.blob.content import ATBlob
from plone.app.blob.interfaces import IATBlobFile
from plone.app.blob.field import BlobField

from plone.registry.interfaces import IRegistry

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.config import PROJECTNAME

from rfa.kaltura.content import base as KalturaBase
from rfa.kaltura.kutils import kconnect
from rfa.kaltura.controlpanel import IRfaKalturaSettings
from rfa.kaltura.storage.storage import KalturaStorage

from KalturaClient.Plugins.Core import KalturaMediaEntry as API_KalturaMediaEntry
from KalturaClient.Plugins.Core import KalturaCategoryEntry, KalturaCategoryEntryFilter
from KalturaClient.Plugins.Core import KalturaMediaType
from KalturaClient.Plugins.Core import KalturaUploadedFileTokenResource
from KalturaClient.Base import KalturaException

KalturaVideoSchema = ATBlob.schema.copy() + KalturaBase.KalturaBaseSchema.copy() + \
    atapi.Schema((
        atapi.StringField('title',
                          searchable=1,
                          required=True,
                          accessor="Title",
                          mutator="setTitle",
                          widget=atapi.StringWidget(label="Title",
                                                    label_msgid="label_kvideofile_title",
                                                    description="The title of this video.",
                                                    description_msgid="desc_kvideofile_title",
                                                    i18n_domain="kaltura_video"),
   
                          ),
        
        atapi.StringField('description',
                          searchable=0,
                          required=True,
                          accessor="Description",
                          widget=atapi.StringWidget(label="Description",
                                                    label_msgid="label_kvideofile_desc",
                                                    description="Enter a description",
                                                    description_msgid="desc_kvideofile_title",
                                                    i18n_domain="kaltura_video"),
                          ),
        
        atapi.ImageField('thumbnail',
                         searchable=0,
                         required=False,
                         mode='r',
                         widget=atapi.ImageWidget(label="Thumbnail",
                                                  description="Thumbnail of video",
                                                  visible = {'edit': 'invisible', 'view': 'visible'},
                                                  i18n_domain="kaltura_video")
                         ),
                         
        atapi.StringField('playbackUrl',
                          searchable=0,
                          accessor="getPlaybackUrl",
                          mode="r",
                          widget=atapi.ComputedWidget(label="Url",
                                                    description="Url set by Kaltura after upload (read only)",
                                                    visible = { 'edit' :'visible', 'view' : 'visible' },
                                                    i18n_domain="kaltura_video")
                          ),
                           
        ),
        marshall=RFC822Marshaller()
   )

KalturaVideoSchema += KalturaBase.KalturaMetadataSchema.copy()
KalturaVideoSchema += ATContentTypeSchema.copy()

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema.get('title').storage = AnnotationStorage()

KalturaVideoSchema['categories'].widget.description = "Select category(ies) this video will belong to"
KalturaVideoSchema['categories'].widget.description_msgid="desc_kvideo_categories"
KalturaVideoSchema['tags'].widget.description = "keyword tags to place on this video (one per line)"
KalturaVideoSchema['tags'].widget.description_msgid="desc_kvideo_tags"

finalizeATCTSchema(KalturaVideoSchema, moveDiscussion=False)

class KalturaVideo(ATBlob, KalturaBase.KalturaContentMixin):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""
    implements(IKalturaVideo, IATBlobFile, IATFile, IFileContent)

    # CMF FTI setup
    global_allow   = True
    default_view   = 'kvideo_main'
    #immediate_view = 'generic_preview'
    
    # CompositePack setup
    layout         = 'kvideo_main'
    layouts        = ('kvideo_main',
                      )

    meta_type = "KalturaVideo"
    schema = KalturaVideoSchema

    KalturaObject = None
    categoryEntries = None
    
    security = ClassSecurityInfo()
    
    #what this class represents in Kaltura's terms:
    KalturaMediaType = KalturaMediaType(KalturaMediaType.VIDEO)
    
    fieldmap = ({'name': 'Title',
                 'pgetter': 'Title',
                 'psetter': 'setTitle',
                 'kgetter': 'getName',
                 'ksetter': 'setName'},
                {'name': 'Description',
                 'pgetter':'Description',
                 'psetter': 'setDescription',
                 'kgetter': 'getDescription',
                 'ksetter': 'setDescription'},
                {'name': 'tags',
                 'pgetter': 'getKalturaTags',
                 'psetter': 'setKalturaTags',
                 'kgetter': 'getTags',
                 'ksetter': 'setTags'},
                #note that categories are not a property of a kalturaObject
                #see self.updateCategories method
                )
                 
    
    def __init__(self, oid, **kwargs):
        super(KalturaVideo, self).__init__(oid, **kwargs)
        self.KalturaObject = None
        
        #holds local list of category entries for this video - matching what's on the KMC.
        self.categoryEntries = []
        
        self.uploadToken = None
        
        #Storage on File field should set this sentry if it uploads a new file to remote.
        self.fileChanged = False
        
    security.declarePublic("getPlaybackUrl")
    def getPlaybackUrl(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getDataUrl()
        else:
            return None
        
    playbackUrl = property(getPlaybackUrl)      
    
    security.declarePrivate('getDefaultPlayerId')
    def getDefaultPlayerId(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        
        return settings.defaultVideoPlayer

    ### These may get duplicated in base.py - we'll see ###
        
    def syncCategories(self, client=None, categories=None):
        """update the category entries on remote for this object's associated Media Entry
           categories are stored remotely through the categoryEntry service
           They are not a property of the Media Entry.
        """
        if categories is None:
            categories = self.getCategories()
        newCatEntries = []
        
        if client is None:
            (client, session) = kconnect()
            
        #refresh list of categories from server, and sync to plone object
        filt = KalturaCategoryEntryFilter()
        filt.setEntryIdEqual(self.KalturaObject.getId())
        self.categoryEntries = client.categoryEntry.list(filt).objects

        currentSet = set([catEntry.categoryId for catEntry in self.categoryEntries])
        newSet = set([int(catId) for catId in categories])
            
        #determine what categories need to be added
        addCats = newSet.difference(currentSet)
        
        #determine what categories need to be removed
        delCats = currentSet.difference(newSet)
       
        #do adds
        for catId in addCats:
            newCatEntry = KalturaCategoryEntry()
            newCatEntry.setCategoryId(catId)
            newCatEntry.setEntryId(self.KalturaObject.getId())
            try:
                client.categoryEntry.add(newCatEntry)
            except KalturaException, e:
                if e.code == "CATEGORY_ENTRY_ALREADY_EXISTS":
                    pass #should never happen, tho
        
        #do removes
        for catId in delCats:
            client.categoryEntry.delete(self.KalturaObject.getId(), catId)
            
        #sync the categories to plone object
        self.categoryEntries = client.categoryEntry.list(filt).objects
     
    def getKalturaTags(self):
        """Tags are stored in the kalturaObject as a comma delimited string"""
        return ','.join([t for t in self.getTags() if t])
     
    def syncMetadata(self, client=None):
        """sync up remote Kaltura Server with data in plone
           Note that we construct an entire MediaEntry with all
           metadata"""
        newMediaEntry = self._createKobj()
        if client is None:
            (client, session) = kconnect()                
        mediaEntry = client.media.update(self.entryId, newMediaEntry)
        self.setKalturaObject(mediaEntry)
        self.syncCategories(client)
        
        #Makes method name 'syncMetadata' a misnomer, we sync the file too if changed.
        if self.fileChanged: #video exists on remote, but replace media content - File.
            self.replaceFileOnRemote(client)
            self.fileChanged = False        
        
    at_post_edit_script = syncMetadata

    def createRemote(self, client=None):
        """Create a new media entry on the remote server
           return the mediaEntry returned from the server
        """
        mediaEntry = self._createKobj()
        if client is None:
            (client, session) = kconnect()
        mediaEntry = client.media.addFromUploadedFile(mediaEntry, self.uploadToken.getId())
        self.setKalturaObject(mediaEntry)
        self.fileChanged = False
        self.syncCategories(client)
        
    at_post_create_script = createRemote
        
    def replaceFileOnRemote(self, client=None):
        resource = KalturaUploadedFileTokenResource()
        resource.setToken(self.uploadToken.getId())
        try:
            client.media.updateContent(self.entryId, resource)
        except KalturaException as e:
            if e.code == u'ENTRY_REPLACEMENT_ALREADY_EXISTS':
                #auto-deny the half-cooked replacement and re-try
                client.media.cancelReplace(self.entryId)
                client.media.updateContent(self.entryId, resource)
                
        #XXX adjust workflow:
        #XXX if 'auto approve' is turned off in settings:
        newMediaEntry = client.media.approveReplace(self.entryId)
        
        #else:
        #  transition this instance's workflow to something 'not published'
        #  Flag this instance as a replaced file, which will \
        #  make the workflow transition to "published", call Kaltura 'approveReplace'
        
        
    security.declarePrivate('_createKobj')
    def _createKobj(self):
        """Return kaltura media entry that represents this object in plone
           This will not create the Media Entry on remote.
           This can be compared to self.KalturaObject, which is the object we last saw from remote
        """
        mediaEntry = API_KalturaMediaEntry()
        mediaEntry.setMediaType(self.KalturaMediaType)
        mediaEntry.setReferenceId(self.UID())
        for field_descr in self.fieldmap:
            
            #get value from plone object
            getter = getattr(self, field_descr['pgetter'])
            val = getter()
            
            #set value on Kaltura Object
            setter = getattr(mediaEntry, field_descr['ksetter'])
            setter(val)
                            
        return mediaEntry
        
        
    ### end possible base class methods ###
        
atapi.registerType(KalturaVideo, PROJECTNAME)




