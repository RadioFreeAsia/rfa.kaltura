"""functions for populating vocabularies for various select or multiselect fields"""
from rfa.kaltura.kutils import kGetPlaylistPlayers
from rfa.kaltura.kutils import kGetCategories


def getTagVoculabulary():
    return ('tag1', 'tag2', 'tag3') #for testing / development only
    #items = []
    
    #tags = kGetTags()
    #for tag in tags:
        #items.append( (tag.getId(), tag.getName()))
        
    #return SimpleVocabulary.fromItems(items)

def getCategoryVocabulary():
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
