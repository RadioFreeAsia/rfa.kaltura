from ZPublisher.HTTPRequest import FileUpload as FileUploadClass

from rfa.kaltura.interfaces import IKalturaPlaylist

from rfa.kaltura.kutils import kconnect
from rfa.kaltura.kutils import KalturaLoggerInstance as logger
from rfa.kaltura.kutils import kupload, kcreatePlaylist, kcreateVideo, kremoveVideo
from rfa.kaltura.kutils import kdiff

def initVideo(context, event):
    """Fired when the object is first populated"""
    context.updateCategories()
        
def modifyVideo(context, event):
    """Fired when the object is edited
       Any differences between plone object (context) and kaltura object
       are considered edits to the kaltura object, and are sent to kaltura
    """
    changed_fields = kdiff(context, context.KalturaObject)
    if changed_fields:
        for (pfield, kfield) in changed_fields:
            #get value from plone object
            val = getattr(context, pfield)
            if callable(val):
                val = val()
           
            #make sure that kfield is an attribute name:
            #not the name of the getter method
            kfieldAttr = getattr(context.KalturaObject, kfield)
            if callable(kfieldAttr):
                #it's a setter or getter.
                if kfield.startswith('get'):
                    kfield = kfield[3:]
                else:
                    #it's simply the name of the attribute... do nothing
                    pass
                
            #can't use updateRemote() with these properties
            if kfield == 'CategoriesIds': #handle categories separately
                context.updateCategories(val)
            if kfield == "Tags":
                context.updateTags(val)            
               
            #these we can use updateRemote()
            kwargs = {}
            if kfield in ['Name', 'Description', 'PartnerId']:
                kwargs[kfield] = val
            
        if kwargs:
            context._updateRemote(**kwargs)
            
        #file field storage (KalturaStorage) should handle changes to video file.

def addVideo(context, event):
    """When a video is added to a container
       zope.lifecycleevent.interfaces.IObjectAddedEvent"""
    pass
    
def deleteVideo(context, event):
    kremoveVideo(context)
    
    
###Playlist Events###    
    
def initPlaylist(context, event):
    """Fired when the playlist object is created"""
    context.setKalturaObject(kcreatePlaylist(context))
    
def modifyPlaylist(context, event):
    """Fired when the playlist object itself is edited"""
    pass
    
