"""functions for populating vocabularies for various select or multiselect fields"""
from rfa.kaltura.kutils import kGetPlaylistPlayers
from rfa.kaltura.kutils import kGetCategories


def getTagVoculabulary():
    """Get Currently created tags on Kaltura server"""
    # Not implemented yet.
    pass

def getCategoryVocabulary():
    """Get Currently created Categories on Kaltura server"""
    items = []
    
    categoryObjs = kGetCategories()
    for cat in categoryObjs:
        items.append( (str(cat.getId()), cat.getName(),) )
        
    return items


def getVideoPlayerVocabulary():
    items = []
    players = kGetPlaylistPlayers()
    
    for player in players:
        items.append( (player.getId(), player.getName()) )
        
    return SimpleVocabulary.fromItems(items)

def getPlaylistPlayerVocabulary():
    items = []
    players = kGetPlaylistPlayers()
    
    for player in players:
        items.append( (player.getId(), player.getName()) )
        
    return SimpleVocabulary.fromItems(items)
