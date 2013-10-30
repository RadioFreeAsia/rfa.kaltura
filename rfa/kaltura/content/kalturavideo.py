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
from rfa.kaltura.credentials import getCredentials

###XXX Todo: create base class ExternalMediaEntry 
##based off of http://www.kaltura.com/api_v3/testmeDoc/index.php?object=KalturaExternalMediaEntry

KalturaVideoSchema = ATBlob.schema.copy() + atapi.Schema((

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
     
     atapi.StringField('entryId',
                       searchable=0,
                       mode='r',
                       accesssor="getEntryId",
                       widget=atapi.ComputedWidget(label="Entry Id",
                                                 description="Entry Id set by Kaltura after upload (read only)",
                                                 visible = { 'edit' :'visible', 'view' : 'visible' },
                                                 i18n_domain="kaltura_video"),
                       ),
     
     atapi.StringField('player',
                       searchable=0,
                       accessor="getPlayer",
                       mutator="setPlayer", 
                       mode='rw',
                       default_method="getDefaultPlayerId",
                       widget=atapi.SelectionWidget(label="Player",
                                                    label_msgid="label_kplayerid_msgid",
                                                    description="Choose the Player to use",
                                                    description_msgid="desc_kplayerid_msgid",
                                                    i18n_domain="kaltura_video"),
                       ),
     
     atapi.LinesField('categories',
                      multiValued = True,
                      searchable=0,
                      required=True,
                      accessor="getCategories",
                      mutator="setCategories",
                      widget=atapi.MultiSelectionWidget(label="Categories",
                                                label_msgid="label_kvideofile_categories",
                                                description="Select video category(ies) this playlist will provide",
                                                description_msgid="desc_kvideofile_categories",
                                                i18n_domain="kaltura_video"),
                      ),       
    
    atapi.LinesField('tags',
                      multiValued = True,
                      searchable=0,
                      required=True,
                      accessor="getTags",
                      mutator="setTags",
                      widget=atapi.MultiSelectionWidget(label="Tags",
                                                label_msgid="label_kvideofile_tags",
                                                description="Select video tag(s) this playlist will provide ",
                                                description_msgid="desc_kvideofile_title",
                                                i18n_domain="kaltura_video"),
                      ),

     atapi.StringField('partnerId',
                       searchable=0,
                       mode='rw',
                       default_method="getDefaultPartnerId",
                       widget=atapi.StringWidget(label="Partner Id",
                                                 label_msgid="label_kpartnerid_msgid",
                                                 description="Kaltura Partner Id (use default if unsure)",
                                                 description_msgid="desc_kpartnerid_msgid",
                                                 i18n_domain="kaltura_video"),
                                             
                                             
                      ),                      
     ),
)

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema['title'].storage = atapi.AnnotationStorage()
KalturaVideoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(KalturaVideoSchema, moveDiscussion=False)


class KalturaVideo(ATBlob):
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

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    security = ClassSecurityInfo()
    KalturaObject = None  ##TODO: Rename to KalturaObject
    
    def __init__(self, oid, **kwargs):
        super(KalturaVideo, self).__init__(oid, **kwargs)
        self.KalturaObject = None ##TODO: Rename to KalturaObject

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    security.declarePublic("getPlaybackUrl")
    def getPlaybackUrl(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getDataUrl()
        else:
            return None
        
    playbackUrl = property(getPlaybackUrl)
        
    security.declarePublic("getEntryId")
    def getEntryId(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getId()
        else:
            return None
        
    entryId = property(getEntryId)        
        
    security.declarePrivate("setMediaEntry")
    def setMediaEntry(self, obj):
        self.KalturaObject = obj

    security.declarePrivate('getDefaultPartnerId')
    def getDefaultPartnerId(self):
        return getCredentials()['PARTNER_ID']
    
    security.declarePrivate('getDefaultPlayerId')
    def getDefaultPlayerId(self):
        return "20100652"
        
        
atapi.registerType(KalturaVideo, PROJECTNAME)




