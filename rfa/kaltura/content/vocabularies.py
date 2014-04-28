"""functions for populating vocabularies for various select or multiselect fields"""
from zope.schema.vocabulary import SimpleVocabulary

from rfa.kaltura.kutils import kGetPlaylistPlayers
from rfa.kaltura.kutils import kGetCategories
from rfa.kaltura.kutils import kGetVideoPlayers

from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.interfaces import IKalturaPlaylist

def getTagVocabulary():
    """Get Currently created tags on Kaltura server"""
    # Not implemented yet.
    pass

def getCategoryVocabulary(parent=None):
    """Get Currently created Categories on Kaltura server"""
    items = []
    
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
