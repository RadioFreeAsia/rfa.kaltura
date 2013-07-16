from zope import component, interface
from Products.Kaltura import interfaces

class ATKalturaVideoKalturaVideo(object):
    """An IKalturaVideo adapter for IATKalturaVideo.
    """
    
    interface.implements(interfaces.IKalturaVideo)
    component.adapts(interfaces.IATKalturaVideo)
    
    def __init__(self, context):
        self.context = context
        
    def _get_title(self):
        return self.context.Title()    
    def _set_title(self,v):
        self.context.setTitle(v)
    title = property(_get_title, _set_title)
    
    def _get_description(self):
        return self.context.Description()
    def _set_description(self, v):
        self.context.setDescription(v)
    description = property(_get_description, _set_description)

    def _get_filename(self):
        return self.context.getFilename()
    def _set_filename(self,v):
        self.context.setFilename(v)
    
    @property
    def url(self):
        return self.context.getUrl()
    
    
def update_catalog(obj, evt):
    obj.reindexObject()
    
def update_id3(obj, evt):
    obj.save_tags()
    