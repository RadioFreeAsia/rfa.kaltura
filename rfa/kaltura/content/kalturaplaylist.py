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

from rfa.kaltura.interfaces import IKalturaPlaylist, IKalturaRuleBasedPlaylist, IKalturaManualPlaylist
from rfa.kaltura.config import PROJECTNAME
from rfa.kaltura.kutils import kconnect

from rfa.kaltura.content import base as KalturaBase
from rfa.kaltura.content.vocabularies import getPlaylistPlayerVocabulary

from KalturaClient.Plugins.Core import KalturaPlaylist as API_KalturaPlaylist
from KalturaClient.Plugins.Core import KalturaMediaEntryFilterForPlaylist

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

BaseKalturaPlaylistSchema = schemata.ATContentTypeSchema.copy() + KalturaBase.KalturaBaseSchema.copy()

#edit the playerId field to show a list of Players for Playlists
BaseKalturaPlaylistSchema["playerId"].vocabulary_factory=getPlaylistPlayerVocabulary
BaseKalturaPlaylistSchema["playerId"].widget = atapi.SelectionWidget(label="Player",
                                                    label_msgid="label_kplayerid_msgid",
                                                    description="Choose the Video player to use",
                                                    description_msgid="desc_kplayerid_msgid",
                                                    i18n_domain="kaltura_video")
                                                    


ManualKalturaPlaylistSchema = BaseKalturaPlaylistSchema.copy() + \
    ATFolderSchema.copy() + \
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


RuleBasedKalturaPlaylistSchema = BaseKalturaPlaylistSchema.copy() + KalturaBase.KalturaMetadataSchema.copy()
    #atapi.Schema(
        #(atapi.IntegerField("daysOld",
                           #accessor="getDaysOld",
                           #mutator="setDaysOld",
                           #required=True,
                           #default=30,
                           #),
         #)
    #)    

schemata.finalizeATCTSchema(RuleBasedKalturaPlaylistSchema, folderish=False, moveDiscussion=False)
                       
schemata.finalizeATCTSchema(ManualKalturaPlaylistSchema, folderish=False, moveDiscussion=False)

class BaseKalturaPlaylist(base.ATCTContent, KalturaBase.KalturaContentMixin):
    implements(IKalturaPlaylist)
    
    security = ClassSecurityInfo()
    isPrincipiaFolderish = False
    
    
    def __init__(self, oid, **kwargs):
        super(BaseKalturaPlaylist, self).__init__(oid, **kwargs)
        self.KalturaObject = None
        
    security.declarePrivate('getDefaultPlaylistPlayerId')
    def getDefaultPlayerId(self):
        return "19707592"    #Some playlist I found on kmc.kaltura.com  Nothing special.
            
    security.declarePrivate('_updateRemote')
    def _updateRemote(self, **kwargs):
        """will set the specified attribute on the matching object in Kaltura
           Try not to modify self.KalturaObject directly -use this method instead
           to keep things in sync.
        """
        
        (client, session) = kconnect()
        newPlaylist = API_KalturaPlaylist()
        for (attr, value) in kwargs.iteritems():
            setter = getattr(newPlaylist, 'set'+attr)
            setter(value)
        resultPlaylist = client.playlist.update(self.getEntryId(), newPlaylist)
        self.setKalturaObject(resultPlaylist)
                
                
                
class ManualKalturaPlaylist(BaseKalturaPlaylist, ATFolder):
    implements(IKalturaManualPlaylist)
    meta_type = "ManualKalturaPlaylist"
    schema = ManualKalturaPlaylistSchema

    security = ClassSecurityInfo()
    isPrincipiaFolderish = True
    
    playlistContent = []
    
    def appendVideo(self, videoId):
        if videoId not in self.playlistContent:
            self.playlistContent.append(videoId)
            contentString = u','.join(self.playlistContent)
            self._updateRemote(PlaylistContent=contentString)    
                

class RuleBasedKalturaPlaylist(BaseKalturaPlaylist):
    implements(IKalturaRuleBasedPlaylist)
    meta_type = "RuleBasedKalturaPlaylist"
    schema = RuleBasedKalturaPlaylistSchema
    
    security = ClassSecurityInfo()
    
    def setTags(self, tagList):
        super(RuleBasedKalturaPlaylist, self).setTags(tagList)
        self.updateFilter()
        
    def setCategories(self, catList):
        super(RuleBasedKalturaPlaylist, self).setCategiroes(catList)
        self.updateFilter()

    def setDaysOld(self, days):
        #Hummm... is there a way to do this?
        pass
    
    def _setFilterTags(self, tagStr):
        kfilters = self.KalturaObject.getFilters()
        kfilters[0].setFreeText(tagStr)
        self.KalturaObject.setFilters(kfilters)
        
    def _setCategoryTags(self, catStr):
        kfilters = self.KalturaObject.getFilters()
        kfilters[0].setCategoriesMatchOr(catStr)
        self.KalturaObject.setFilters(kfilters)
        
    def updateFilter(self):
        tags = ','.join(self.getTags())
        cats = ','.join(self.getCategories())
        self._setFilterTags(tags)
        self._setCategoryTags(cats)
        self._updateRemote(Filters, self.KalturaFilterObject)
        
        
atapi.registerType(ManualKalturaPlaylist, PROJECTNAME)
atapi.registerType(RuleBasedKalturaPlaylist, PROJECTNAME)
