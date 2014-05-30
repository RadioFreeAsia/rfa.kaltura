"""functions for populating vocabularies for various select or multiselect fields"""
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from rfa.kaltura.controlpanel import IRfaKalturaSettings
from rfa.kaltura.kutils import kGetPlaylistPlayers, kGetVideoPlayers
from rfa.kaltura.kutils import kGetCategories, kGetCategoryId
from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.interfaces import IKalturaPlaylist

def getTagVocabulary():
    """Get Currently created tags on Kaltura server"""
    # Not implemented yet.
    pass

def getCategoryVocabulary(parent=None):
    """Get Currently created Categories on Kaltura server"""
    
    items = []
    if parent is None:
        #check settings for 'top level category'
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        tlc = settings.topLevelCategory
        if tlc:
            parent = kGetCategoryId(categoryName=tlc)
            #place the top-level category at the top of the list, so it's selectable.
            items.append( (str(parent), tlc,) )
        
    categoryObjs = kGetCategories(parent)
    for cat in categoryObjs:
        items.append( (str(cat.getId()), cat.getName(),) )
        
    return items


def PlayerVocabularyFactory(context):
    players=[]
    if IKalturaVideo.providedBy(context):
        players = kGetVideoPlayers()
    elif IKalturaPlaylist.providedBy(context):
        players = kGetPlaylistPlayers()
        
    items = []
    for player in players:
        #simpleVocabulary doesn't like unicode!
        name = player.getName()
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        items.append( (name, str(player.getId())) )
        
    return SimpleVocabulary.fromItems(items)
