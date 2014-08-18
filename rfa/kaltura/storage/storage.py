from Acquisition import aq_base
from zope.interface import implements
from zope.component.zcml import interface
from Products.Archetypes.interfaces.storage import IStorage
from Products.Archetypes.Storage.annotation import AnnotationStorage
from zope.interface import Interface

from Products.Archetypes.Registry import registerStorage

class INoStorage(IStorage):
    pass

class IKalturaStorage(IStorage):
    pass

class KalturaStorage(AnnotationStorage):
    """ TODO
        Store file on kaltura media center
        get file from kaltura media center
    """
    def __init__(self):
        raise NotImplemented

class NoStorage(AnnotationStorage):
    """Remove blob file data from plone - store a zero-length blob  
       Rely solely on storage remotely on Kaltura Media Center
    """
    implements(INoStorage)
    
    def get(self, name, instance, **kwargs):
        value = AnnotationStorage.get(self, name, instance, **kwargs)
        return value
    
    def set(self, name, instance, value, **kwargs):
        value = aq_base(value)
        #remove file data from blob
        
        if value.filename is not None:    
            #create plain text file containing filename for the blob to consume
            dummyFile = '/tmp/dummy'        
            fh = open(dummyFile, mode='w+')
            fh.writelines([value.filename,
                           "\nThis file is stored on kaltura only, and is not available via plone"])
            fh.close()
            
            #tell the blob this is really your file
            value.blob.consumeFile(dummyFile)
            
        AnnotationStorage.set(self, name, instance, value, **kwargs)
    
    def unset(self, name, instance, **kwargs):
        AnnotationStorage.unset(self, name, instance, **kwargs)
    
registerStorage(NoStorage)