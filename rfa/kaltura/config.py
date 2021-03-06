"""Common configuration constants
"""

PROJECTNAME = 'rfa.kaltura'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'KalturaVideo': 'rfa.kaltura: Add Kaltura Video',
    'RuleBasedKalturaPlaylist': 'rfa.kaltura: Add Kaltura Playlist',
    'ManualKalturaPlaylist': 'rfa.kaltura: Add Kaltura Playlist',
}


#if playlist size not set, this is the default.
DEFAULT_DYNAMIC_PLAYLIST_SIZE = 20