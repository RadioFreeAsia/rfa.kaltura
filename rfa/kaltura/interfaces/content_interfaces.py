from zope.interface import Interface
# -*- Additional Imports Here -*-


class IKalturaVideo(Interface):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""


class IKalturaPlaylist(Interface):
    """Kaltura Playlist Content Type - 
       contains Kaltura Media and renders them all as a playlist"""
    
class IKalturaRuleBasedPlaylist(IKalturaPlaylist):
    """Kaltura Rule-Based Playlist
       For creating dynamic playlists configured by rules
       such as matching tags, categories, a date range, etc"""
    
class IKalturaManualPlaylist(IKalturaPlaylist):
    """Kaltura Manual Playlist
       for creating playlists by manually specifying the media
       that the playlist contains"""
    

    
    
    