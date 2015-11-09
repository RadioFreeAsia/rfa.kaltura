from ZPublisher.HTTPRequest import FileUpload as FileUploadClass

from rfa.kaltura.interfaces import IKalturaPlaylist

from rfa.kaltura.kutils import kconnect
from rfa.kaltura.kutils import KalturaLoggerInstance as logger
from rfa.kaltura.kutils import kupload, kcreatePlaylist, kcreateVideo, kremoveVideo, krejectVideo
from rfa.kaltura.kutils import kdiff
from rfa.kaltura.kutils import kSetStatus, KalturaEntryModerationStatus

def initVideo(context, event):
    """Fired when the object is first populated"""
    pass
        
def modifyVideo(context, event):
    """Fired when the object is edited
       Any differences between plone object (context) and kaltura object
       are considered edits to the kaltura object, and are sent to kaltura
    """
    pass

def addVideo(context, event):
    """When a video is added to a container
       zope.lifecycleevent.interfaces.IObjectAddedEvent"""
    
def deleteVideo(context, event):
    #kremoveVideo(context)  #TODO - configure option to delete or reject plone deleted content.
    krejectVideo(context)
    
def workflowChange(context, event):
    workflow = event.workflow
    action = event.action
    status = None
    
    if action == 'publish':
        status = KalturaEntryModerationStatus.APPROVED
    elif action in ('retract', 'reject'):
        status = KalturaEntryModerationStatus.PENDING_MODERATION
    
    if status:
        context.setModerationStatus(status)
    
    
    
###Playlist Events###    
    
def initPlaylist(context, event):
    """Fired when the playlist object is created"""
    context.setKalturaObject(kcreatePlaylist(context))
    
def modifyPlaylist(context, event):
    """Fired when the playlist object itself is edited"""
    pass
    
