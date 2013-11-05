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

from KalturaClient.Plugins.Core import KalturaMediaEntry

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

KalturaVideoSchema += KalturaBase.KalturaMetadataSchema

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema['title'].storage = atapi.AnnotationStorage()
KalturaVideoSchema['description'].storage = atapi.AnnotationStorage()

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
    KalturaObject = None  ##TODO: Rename to KalturaObject

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
        return "20100652"
        
    security.declarePrivate('_updateRemote')
    def _updateRemote(self, **kwargs):
            (client, session) = kconnect()
            newVideo = KalturaMediaEntry()
            for (attr, value) in kwargs.iteritems():
                setter = getattr(newPlaylist, 'set'+attr)
                setter(value)
            result = client.playlist.update(self.getEntryId(), newVideo)
            self.setKalturaObject(result) 
        
atapi.registerType(KalturaVideo, PROJECTNAME)




