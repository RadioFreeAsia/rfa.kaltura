"""functions for populating vocabularies for various select or multiselect fields"""
from zope.schema.vocabulary import SimpleVocabulary

from rfa.kaltura.kutils import kGetPlaylistPlayers
from rfa.kaltura.kutils import kGetCategories


def getTagVoculabulary():
    return ('tag1', 'tag2', 'tag3')
    #items = []
    
    #tags = kGetTags()
    #for tag in tags:
        #items.append( (tag.getId(), tag.getName()))
        
    #return SimpleVocabulary.fromItems(tags)

def getCategoryVoculabulary():
    categoryObjs = kGetCategories()
    for cat in categoryObjs:
        items.append( (cat.getId(), cat.getName()))
        
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
