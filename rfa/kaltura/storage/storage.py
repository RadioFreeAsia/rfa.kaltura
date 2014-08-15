import ZODB.POSException
from zope.interface import implements
from zope.component.zcml import interface
from Products.Archetypes.interfaces.storage import IStorage
from Products.Archetypes.Storage.annotation import AnnotationStorage
from zope.interface import Interface

from Products.Archetypes.Registry import registerStorage

class INoStorage(IStorage):
    pass 


class NoStorage(AnnotationStorage):
    """Completely skip storage on Plone.  
       Rely solely on storage remotely on Kaltura Media Center
    """
    implements(INoStorage)
    
    def get(self, name, instance, **kwargs):
        return None
    
    def set(self, name, instance, value, **kwargs):
        pass
    
    def unset(self, name, instance, **kwargs):
        pass
    
        
registerStorage(NoStorage)