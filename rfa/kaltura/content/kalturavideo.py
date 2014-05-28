"""Definition of the Kaltura Video content type
"""

from zope.interface import implements

from AccessControl import ClassSecurityInfo


from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.interface.file import IATFile
from Products.ATContentTypes.interface.file import IFileContent
from plone.app.blob.content import ATBlob
from plone.app.blob.interfaces import IATBlobFile

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.config import PROJECTNAME

from rfa.kaltura.content import base as KalturaBase
from rfa.kaltura.kutils import kconnect

from KalturaClient.Plugins.Core import KalturaMediaEntry as API_KalturaMediaEntry
from KalturaClient.Plugins.Core import KalturaCategoryEntry, KalturaCategoryEntryFilter

KalturaVideoSchema = ATBlob.schema.copy() + KalturaBase.KalturaBaseSchema.copy() + \
    atapi.Schema((
        atapi.StringField('title',
                          searchable=1,
                          required=True,
                          languageIndependent=1,
                          accessor="Title",
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
   )

KalturaVideoSchema += KalturaBase.KalturaMetadataSchema.copy()

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema['title'].storage = atapi.AnnotationStorage()
KalturaVideoSchema['description'].storage = atapi.AnnotationStorage()

KalturaVideoSchema['categories'].widget.description = "Select category(ies) this video will belong to"
KalturaVideoSchema['categories'].widget.description_msgid="desc_kvideo_categories"
KalturaVideoSchema['tags'].widget.description = "keyword tags to place on this video (one per line)"
KalturaVideoSchema['tags'].widget.description_msgid="desc_kvideo_tags"

schemata.finalizeATCTSchema(KalturaVideoSchema, moveDiscussion=False)

###TODO: Offer option NOT to store video as a blob in the ZODB
class KalturaVideo(ATBlob, KalturaBase.KalturaContentMixin):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""
    #ISA KalturaMediaEntry
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

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    security = ClassSecurityInfo()

    def __init__(self, oid, **kwargs):
        super(KalturaVideo, self).__init__(oid, **kwargs)
        self.KalturaObject = None
        
        #holds local list of category entries for this video - matching what's on the KMC.
        self.categoryEntries = []  

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    security.declarePublic("getPlaybackUrl")
    def getPlaybackUrl(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getDataUrl()
        else:
            return None
        
    playbackUrl = property(getPlaybackUrl)      
    
    security.declarePrivate('getDefaultPlayerId')
    def getDefaultPlayerId(self):
        return "20100652" #todo - add to config

    ### These may get duplicated in base.py - we'll see ###
        
    def updateCategories(self, categories):
        newCatEntries = []
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
            
    def updateTags(self, tags):   
        tagsString = ','.join([t for t in self.getTags() if t])
        self._updateRemote(Tags=tagsString)        
        
    ### end possible base class methods ###
        
    security.declarePrivate('_updateRemote')
    def _updateRemote(self, **kwargs):
        """will set the specified attribute on the matching object in Kaltura
           Try not to modify self.KalturaObject directly -use this method instead
           to keep things in sync with the remote server.
           
           For example, to update the name of the kaltura video:
           self._updateRemote(name='NewName')
        """
        #this is becoming quite a hastle.  Might need to re-think this idea.
        #see 'events.py' modifyVideo to see my pain.
        (client, session) = kconnect()
        newVideo = API_KalturaMediaEntry()
        for (attr, value) in kwargs.iteritems():
            setter = getattr(newVideo, 'set'+attr)
            setter(value)
        result = client.media.update(self.getEntryId(), newVideo)
        self.setKalturaObject(result) 
        
atapi.registerType(KalturaVideo, PROJECTNAME)




