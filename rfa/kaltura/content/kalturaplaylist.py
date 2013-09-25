"""Definition of the Kaltura Playlist Content Type
"""
from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.folder import ATFolder, ATFolderSchema

from rfa.kaltura.interfaces import IKalturaPlaylist
from rfa.kaltura.config import PROJECTNAME
from rfa.kaltura.credentials import getCredentials

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

###XXX Todo: create base class ExternalMediaEntry 
##based off of http://www.kaltura.com/api_v3/testmeDoc/index.php?object=KalturaExternalMediaEntry

KalturaPlaylistSchema = ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField('title',
                           searchable=1,
                           required=True,
                           languageIndependent=1,
                           accessor="Title",
                           widget=atapi.StringWidget(label="Title",
                                                     label_msgid="label_kvideofile_title",
                                                     description="The title of this Playlist.",
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

KalturaPlaylistSchema['title'].storage = atapi.AnnotationStorage()
KalturaPlaylistSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(KalturaPlaylistSchema, moveDiscussion=False)

class KalturaPlaylist(ATFolder):
    implements(IKalturaPlaylist)
    
    meta_type = "KalturaPlaylist"
    schema = KalturaPlaylistSchema
    isPrincipiaFolderish = True

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    security = ClassSecurityInfo()
    KMediaEntry = None
    
    def __init__(self, oid, **kwargs):
        super(KalturaPlaylist, self).__init__(oid, **kwargs)
        self.KMediaEntry = None
        
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
        
                
                
atapi.registerType(KalturaPlaylist, PROJECTNAME)
    