import copy
from Acquisition import aq_base
from zope.interface import implements
from zope.interface import Interface
from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from Products.Archetypes.interfaces.storage import IStorage
from Products.Archetypes.Storage.annotation import AnnotationStorage
from Products.Archetypes.Registry import registerStorage

from rfa.kaltura.kutils import kconnect
from rfa.kaltura.kutils import kupload
from rfa.kaltura.kutils import kcreateVideo
from rfa.kaltura.kutils import KalturaLoggerInstance
from rfa.kaltura.controlpanel import IRfaKalturaSettings

# annotation keys
KALTURA_STORAGE = 'rfa.kaltura.storage.KalturaStorage'


class IKalturaStorage(IStorage):
    pass

class KalturaStorage(AnnotationStorage):
    """ TODO
        Store file on kaltura media center
        get file from kaltura media center
    """
    implements(IKalturaStorage)
        
    def get(self, name, instance, **kwargs):
        """XXX TODO Retrieve video from Kaltura, 
           wrap it in a blob wrapper, and return it
        """
        value = AnnotationStorage.get(self, name, instance, **kwargs)        
        #get video file from Kaltura and replace the file in the blob.
        return value

    def set(self, name, instance, value, **kwargs):
        """Store video on Kaltura, 
           create media entry if required
        """        
        value = aq_base(value)
        initializing = kwargs.get('_initializing_', False)
        
        if initializing:
            AnnotationStorage.set(self, name, instance, value, **kwargs) 
            return
        
        if value.filename is None:
            #AnnotationStorage.set(self, name, instance, value, **kwargs)
            return #only interested in running set when instance is ready to save.
        
        mediaEntry = instance.KalturaObject
        if mediaEntry is None:
            mediaEntry = kcreateVideo(instance)
        
        #upload video content to Kaltura
        (client, ks) = kconnect()
        filename = '/tmp/'+value.filename
        
        #Find out a way to send client.media.upload a string instead of a filehandle
        with open(filename,'w') as fh:
            fh.write(str(value))
            
        with open(filename, 'r') as fh:
            uploadTokenId = client.media.upload(fh)
        
        mediaEntry = client.media.addFromUploadedFile(mediaEntry, uploadTokenId)   
        KalturaLoggerInstance.log("blob uploaded.  MediaEntry %s" % (mediaEntry.__repr__()))
        
        instance.setKalturaObject(mediaEntry)
        
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        
        if settings.storageMethod == u"No Local Storage":
            import pdb; pdb.set_trace()
            value.update_data(data = value.filename+"\nThis file is stored on kaltura only, and is not available via plone")
            
        AnnotationStorage.set(self, name, instance, value, **kwargs)        
        
    def unset(self, name, instance, **kwargs):
        """### TODO:
           Remove from Kaltura
        """
        AnnotationStorage.unset(self, name, instance, **kwargs)

registerStorage(KalturaStorage)
