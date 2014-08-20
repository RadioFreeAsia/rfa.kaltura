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

class IKalturaStorage(IStorage):
    pass

class KalturaStorage(AnnotationStorage):
    """ TODO
        Store file on kaltura media center
        get file from kaltura media center
    """
    implements(IKalturaStorage)
    
    def initializeInstance(self, instance):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        self.storageMethod = settings.storageMethod
        
    def get(self, name, instance, **kwargs):
        """XXX TODO Retrieve video from Kaltura, 
           wrap it in a blob wrapper, and return it
        """
        #import pdb; pdb.set_trace()
        #return AnnotationStorage.get(self, name, instance, **kwargs)        

    def set(self, name, instance, value, **kwargs):
        """Store video on Kaltura, 
           create media entry if required
        """        
        value = aq_base(value)
        if value.filename is None:
            return #only interested in running set when instance is ready to save.
        
        mediaEntry = instance.KalturaObject
        if mediaEntry is None:
            mediaEntry = kcreateVideo(instance)
        
        #upload video content to Kaltura
        (client, ks) = kconnect()
        fh = value.getBlob().open()
        uploadTokenId = client.media.upload(fh)
        fh.close()
        mediaEntry = client.media.addFromUploadedFile(mediaEntry, uploadTokenId)   
        KalturaLoggerInstance.log("blob uploaded.  MediaEntry %s" % (mediaEntry.__repr__()))
        
        instance.setKalturaObject(mediaEntry)
        
        if self.storageMethod == u"No Local Storage":
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
        """### TODO:
           Remove from Kaltura
        """
        AnnotationStorage.unset(self, name, instance, **kwargs)

registerStorage(KalturaStorage)
