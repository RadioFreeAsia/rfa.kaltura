from ZPublisher.HTTPRequest import FileUpload as FileUploadClass

from rfa.kaltura.interfaces import IKalturaPlaylist

from rfa.kaltura.kutils import KalturaLoggerInstance as logger
from rfa.kaltura.kutils import kupload, kcreatePlaylist

def initVideo(context, event):
    """Fired when the object is first populated"""

    datafile = context.REQUEST.form.get('file_file')
    if isinstance(datafile, FileUploadClass):
        KMediaEntry = kupload(context)    
        context.setMediaEntry(KMediaEntry)
        _updatePlaylists(context)
        
def modifyVideo(context, event):
    """Fired when the object is edited"""
    
    status = context.REQUEST.form.get('file_delete')
    if status in ("nochange", None):
        pass #not modified
    else:
        #File Modification Occured
        context.setMediaEntry(kupload(context))

def addVideo(context, event):
    """When a video is added to a container
       zope.lifecycleevent.interfaces.IObjectAddedEvent"""
    pass
    
    
###Playlist Events###    
    
def initPlaylist(context, event):
    """Fired when the playlist object is created"""
    context.setKalturaObject(kcreatePlaylist(context))
    
def modifyPlaylist(context, event):
    """Fired when the playlist object itself is edited"""
    context._updateRemote()
    
def _updatePlaylists(context):
    parent = context.aq_parent
    if IKalturaPlaylist.providedBy(parent):
        if context.getEntryId() is not None:
            parent.appendVideo(context.getEntryId())
        #else:
            #logger.warning("playlist not appended to - no entryId on object")    
    
    