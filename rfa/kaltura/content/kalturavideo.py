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
     
     atapi.StringField('playerId',
                       searchable=0,
                       accessor="getPlayerId",
                       mutator="setPlayerId", 
                       mode='rw',
                       widget=atapi.StringWidget(label="Player Id",
                                                 label_msgid="label_kplayerid_msgid",
                                                 description="Enter the Player Id to use",
                                                 description_msgid="desc_kplayerid_msgid",
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

    meta_type = "KalturaVideo"
    schema = KalturaVideoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    security = ClassSecurityInfo()
    KMediaEntry = None
    
    def __init__(self, oid, **kwargs):
        super(KalturaVideo, self).__init__(oid, **kwargs)
        self.KMediaEntry = None

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    security.declarePrivate("getPlaybackUrl")
    def getPlaybackUrl(self):
        if self.KMediaEntry is not None:
            return self.KMediaEntry.getDataUrl()
        else:
            return None
        
    playbackUrl = property(getPlaybackUrl)
        
    security.declarePublic("getEntryId")
    def getEntryId(self):
        if self.KMediaEntry is not None:
            return self.KMediaEntry.getId()
        else:
            return None
        
    entryId = property(getEntryId)        
        
        
    security.declarePrivate("setMediaEntry")
    def setMediaEntry(self, obj):
        self.KMediaEntry = obj


    security.declarePrivate('getDefaultPartnerId')
    def getDefaultPartnerId(self):
        return getCredentials()['PARTNER_ID']
    
        
        
atapi.registerType(KalturaVideo, PROJECTNAME)
