"""functions for populating vocabularies for various select or multiselect fields"""

from rfa.kaltura.kutils import kGetPlaylistPlayers


def getTagVoculabulary():    
    items = []
    
    tags = kGetTags()
    for tag in tags:
        items.append( (tag.getId(), tag.getName()))
        
    return SimpleVocabulary.fromItems(tags)

def getCategoryVoculabulary():    
    items = []
    
    tags = kGetCategories()
    for tag in tags:
        items.append( (tag.getId(), tag.getName()))
        
    return SimpleVocabulary.fromItems(tags)


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
