from zope.interface import Interface
# -*- Additional Imports Here -*-


class IKalturaVideo(Interface):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""


class IKalturaPlaylist(Interface):
    """Kaltura Playlist Content Type - 
       Folderish, contains (Kaltura) Videos and renders them all as a playlist"""