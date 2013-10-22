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
from rfa.kaltura.kutils import kconnect
from rfa.kalutra.kutils import kGetPlaylistPlayers

from zope.schema.vocabulary import SimpleVocabulary

from KalturaClient.Plugins.Core import KalturaPlaylist as API_KalturaPlaylist

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
                           
    atapi.StringField('player',
                      searchable=0,
                      accessor="getPlayer",
                      mutator="setPlayer", 
                      mode='rw',
                      vocabulary_factory=getPlaylistPlayerVocabulary(),
                      widget=atapi.SelectionWidget(label="Player",
                                                   label_msgid="label_kplayerid_msgid",
                                                   description="Choose the Video player to use",
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
    KalturaObject = None
    
    def __init__(self, oid, **kwargs):
        super(KalturaPlaylist, self).__init__(oid, **kwargs)
        self.KalturaObject = None
        self.playlistContent = []
                
    security.declarePublic("getEntryId")
    def getEntryId(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getId()
        else:
            return None     
    entryId = property(getEntryId)        
                
    security.declarePrivate("setKalturaObject")
    def setKalturaObject(self, obj):
        self.KalturaObject = obj
        self.KalturaObject.referenceId = self.UID()
    
    security.declarePrivate('getDefaultPartnerId')
    def getDefaultPartnerId(self):
        return getCredentials()['PARTNER_ID']
        
    security.declarePrivate('getDefaultPlayerId')
    def getDefaultPlayerId(self):
        return "19707592"    #Some playlist I found on kmc.kaltura.com  Nothing special.
    
    def appendVideo(self, videoId):
        if videoId not in self.playlistContent:
            self.playlistContent.append(videoId)
            contentString = u','.join(self.playlistContent)
            self._updateRemote(PlaylistContent=contentString)
            
    def _updateRemote(self, **kwargs):
        (client, session) = kconnect()
        newPlaylist = API_KalturaPlaylist()
        for (attr, value) in kwargs.iteritems():
            setter = getattr(newPlaylist, 'set'+attr)
            setter(value)
        resultPlaylist = client.playlist.update(self.getEntryId(), newPlaylist)
        self.setKalturaObject(resultPlaylist)
                
atapi.registerType(KalturaPlaylist, PROJECTNAME)


def getPlaylistPlayerVocabulary():
    items = []
    players = kGetPlaylistPlayers()
    
    for player in players:
        items.append( (player.getId(), player.getName()) )
        
    return SimpleVocabulary.fromItems(items)


    
    