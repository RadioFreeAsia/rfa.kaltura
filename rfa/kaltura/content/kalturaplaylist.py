"""Definition of the Kaltura Playlist Content Type
"""
from zope.interface import implements

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

from rfa.kaltura.content import base as KalturaBase

from KalturaClient.Plugins.Core import KalturaPlaylist as API_KalturaPlaylist

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

BaseKalturaPlaylistSchema = schemata.ATContentTypeSchema + KalturaBase.KalturaBaseSchema
BaseKalturaPlaylistSchema['playerId'].default_method="getDefaultPlaylistPlayerId"

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

schemata.finalizeATCTSchema(ManualKalturaPlaylistSchema, folderish=False, moveDiscussion=False)

RuleBasedKalturaPlaylistSchema = BaseKalturaPlaylistSchema + KalturaBase.KalturaMetadataSchema
schemata.finalizeATCTSchema(RuleBasedKalturaPlaylistSchema, folderish=False, moveDiscussion=False)

class BaseKalturaPlaylist(base.ATCTContent, KalturaBase.KalturaContentMixin):
    implements(IKalturaPlaylist)
    
    isPrincipiaFolderish = False
    
    def __init__(self, oid, **kwargs):
        super(BaseKalturaPlaylist, self).__init__(oid, **kwargs)
        self.KalturaObject = None
        
    security.declarePrivate('getDefaultPlaylistPlayerId')
    def getDefaultPlayerId(self):
        return "19707592"    #Some playlist I found on kmc.kaltura.com  Nothing special.
            
    security.declarePrivate('_updateRemote')
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
    
    playlistContent = []
    
    def appendVideo(self, videoId):
        if videoId not in self.playlistContent:
            self.playlistContent.append(videoId)
            contentString = u','.join(self.playlistContent)
            self._updateRemote(PlaylistContent=contentString)    
                

class RuleBasedKalturaPlaylist(BaseKalturaPlaylist):
    
    meta_type = "RuleBasedKalturaPlaylist"
    schema = RuleBasedKalturaPlaylistSchema
        
        
atapi.registerType(ManualKalturaPlaylist, PROJECTNAME)
atapi.registerType(RuleBasedKalturaPlaylist, PROJECTNAME)  