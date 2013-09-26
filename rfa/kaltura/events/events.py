from ZPublisher.HTTPRequest import FileUpload as FileUploadClass

from rfa.kaltura.interfaces import IKalturaPlaylist

from rfa.kaltura.kutils import KalturaLoggerInstance as logger
from rfa.kaltura.kutils import kupload, kcreatePlaylist

def initVideo(context, event):
    """Fired when the object is first saved"""

    datafile = context.REQUEST.form.get('file_file')
    if isinstance(datafile, FileUploadClass):
        KMediaEntry = kupload(context)    
        context.setMediaEntry(KMediaEntry)
    else:
        logger.warning("no file uploaded on init of kaltura object %s" % (context.UID(),))

def modifyVideo(context, event):
    """Fired when the object is edited"""
    
    status = context.REQUEST.form.get('file_delete')
    if status in ("nochange", None):
        pass #not modified
    else:
        #File Modification Occured
        context.setMediaEntry(kupload(context))        

def addVideo(context, event):
    parent = event.newParent
    if IKalturaPlaylist.providedBy(parent): #and make sure we don't add it 5 times!!! this event gets called a lot.
        parent.addToPlaylist(context)
    else:
        pass
    
def initPlaylist(context, event):
    """Fired when the playlist object is created"""
    
    context.setPlaylist(kcreatePlaylist(context))
    
    
def modifyPlaylist(context, event):
    """Fired when the playlist object itself is edited"""
    
    