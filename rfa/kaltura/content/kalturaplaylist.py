"""Definition of the Kaltura Playlist Content Type
"""
from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.folder import ATFolder

from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.folder import ATFolderSchema

from rfa.kaltura.interfaces import IKalturaPlaylist
from rfa.kaltura.config import PROJECTNAME
from rfa.kaltura.credentials import getCredentials
from rfa.kaltura.kutils import kconnect
#from rfa.kaltura.content.vocabularies import getPlaylistPlayerVocabulary

from KalturaClient.Plugins.Core import KalturaPlaylist as API_KalturaPlaylist

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

###XXX Todo: create base class ExternalMediaEntry 
##based off of http://www.kaltura.com/api_v3/testmeDoc/index.php?object=KalturaExternalMediaEntry

BaseKalturaPlaylistSchema = schemata.ATContentTypeSchema + \
    atapi.Schema(
        (atapi.TextField(name = 'slug',
                         required = True,
                         searchable = False,
                         default_content_type = 'text/plain',
                         default_output_type = 'text/plain',
                         allowable_content_types = ('text/plain',),
                         widget = atapi.StringWidget(label = 'URL Story Name',
                                     label_msgid = 'label_slug_text',
                                     description = 'URL Story Name',
                                     description_msgid = 'help_slug_text',
                                     i18n_domain = 'rfasite',
                                     visible={'view': 'visible',
                                              'edit': 'visible'},
                                    ),
               ),    
                           
         atapi.StringField('player',
                           searchable=0,
                           accessor="getPlayer",
                           mutator="setPlayer", 
                           mode='rw',
                           #vocabulary_factory=getPlaylistPlayerVocabulary(),
                           #widget=atapi.SelectionWidget(label="Player",
                                                        #label_msgid="label_kplayerid_msgid",
                                                        #description="Choose the Video player to use",
                                                        #description_msgid="desc_kplayerid_msgid",
                                                        #i18n_domain="kaltura_video"),
                           #),
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
         )
     
    )

ManualKalturaPlaylistSchema = BaseKalturaPlaylistSchema + \
    ATFolderSchema + \
    atapi.Schema(
        (atapi.ReferenceField('playlistVideos',
                              relationship = 'playlist_videos',
                              allowed_types=('KalturaVideo',),
                              multiValued = True,
                              isMetadata = False,
                              accessor = 'getPlaylistVideos',
                              mutator = 'setPlaylistVideos',
                              required=False,
                              default=(),    
                              widget = ReferenceBrowserWidget(
                                  addable = False,
                                  destination = [],
                                  allow_search = True,
                                  allow_browse = True,
                                  allow_sorting = True,
                                  show_indexes = False,
                                  force_close_on_insert = True,
                                  label = "Videos (Add Manually)",
                                  label_msgid = "label_kvideos_msgid",
                                  description = "Choose manually which videos are "
                                  "included in this playlist",
                                  description_msgid = "desc_kvideos_msgid",
                                  i18n_domain = "kaltura_video",
                                  visible = {'edit' : 'visible',
                                             'view' : 'visible',
                                             }
                                  ),
                              ),
         )
    )

RuleBasedKalturaPlaylistSchema = BaseKalturaPlaylistSchema + \
    atapi.Schema(
        (atapi.LinesField('categories',
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
         )

)

# 'folderish' suppresses 'relatedItemsField' from edit form.
schemata.finalizeATCTSchema(ManualKalturaPlaylistSchema, folderish=False, moveDiscussion=False)
schemata.finalizeATCTSchema(RuleBasedKalturaPlaylistSchema, folderish=False, moveDiscussion=False)

class BaseKalturaPlaylist(base.ATCTContent):
    implements(IKalturaPlaylist)
    
    isPrincipiaFolderish = False
    
    security = ClassSecurityInfo()
    KalturaObject = None
    
    def __init__(self, oid, **kwargs):
        super(BaseKalturaPlaylist, self).__init__(oid, **kwargs)
        self.KalturaObject = None
                
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
            
    def _updateRemote(self, **kwargs):
        (client, session) = kconnect()
        newPlaylist = API_KalturaPlaylist()
        for (attr, value) in kwargs.iteritems():
            setter = getattr(newPlaylist, 'set'+attr)
            setter(value)
        resultPlaylist = client.playlist.update(self.getEntryId(), newPlaylist)
        self.setKalturaObject(resultPlaylist)
                
                
                
class ManualKalturaPlaylist(BaseKalturaPlaylist, ATFolder):
    meta_type = "ManualKalturaPlaylist"
    schema = ManualKalturaPlaylistSchema
    
    isPrincipiaFolderish = True
    
    def __init__(self, oid, **kwargs):
        super(BaseKalturaPlaylist, self).__init__(oid, **kwargs)
        self.playlistContent = []
    
    def appendVideo(self, videoId):
            if videoId not in self.playlistContent:
                self.playlistContent.append(videoId)
                contentString = u','.join(self.playlistContent)
                self._updateRemote(PlaylistContent=contentString)    

class RuleBasedKalturaPlaylist(BaseKalturaPlaylist):
    
    meta_type = "RuleBasedKalturaPlaylist"
    schema = RuleBasedKalturaPlaylistSchema
    
    def __init__(self, oid, **kwargs):
        super(BaseKalturaPlaylist, self).__init__(oid, **kwargs)
        self.keywords = []
        self.tags = []
        
    def getTags(self):
        return self.tags
    
    def setTags(self, tags):
        self.tags = tags
        
    def getKeywords(self):
        return self.keywords
    
    def setKeywords(self, keywords):
        self.keywords = keywords
        
atapi.registerType(ManualKalturaPlaylist, PROJECTNAME)
atapi.registerType(RuleBasedKalturaPlaylist, PROJECTNAME)  