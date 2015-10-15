import tempfile

from Acquisition import aq_base
from zope.interface import implements
from zope.interface import Interface
from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from Products.Archetypes.interfaces.storage import IStorage
from Products.Archetypes.Storage.annotation import AnnotationStorage
from Products.Archetypes.Registry import registerStorage

from plone.app.blob.utils import openBlob


from rfa.kaltura.kutils import kconnect
from rfa.kaltura.kutils import kupload
from rfa.kaltura.kutils import kcreateVideo
from rfa.kaltura.kutils import KalturaLoggerInstance
from rfa.kaltura.controlpanel import IRfaKalturaSettings

from rfa.kaltura.kutils import KalturaUploadToken, KalturaUploadedFileTokenResource
from rfa.kaltura.kutils import kSetStatus, KalturaEntryModerationStatus

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
        
        #get a filehandle for the video content we are uploading to Kaltura Server
        fh = openBlob(value.blob, mode='r')

        #connect to Kaltura Server
        (client, ks) = kconnect()
        #upload video content.     
        
        token = KalturaUploadToken()
        token = client.uploadToken.add(token)            
        token = client.uploadToken.upload(token.getId(), fh)
        
        instance.uploadToken = token
        instance.fileChanged = True
        #now, the instance should take over to do addFromUploadedFile or updateContent
        #and associate this uploaded file with a media entry.
        
        #if "no local storage" is set, we clobber the blob file.
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        import pdb; pdb.set_trace()
        if settings.storageMethod == u"No Local Storage":
            replace = tempfile
            fh = openBlob(value.blob, mode='w') 
            fh.write(value.filename+"\n\nThis file is stored on kaltura only, and is not available via plone")
            fh.close()

        AnnotationStorage.set(self, name, instance, value, **kwargs)

        
    def unset(self, name, instance, **kwargs):
        
        (client, ks) = kconnect()
        mediaEntry = instance.KalturaObject
        try:
            client.media.delete(mediaEntry.getId)
        except: #XXX ENTRY_ID_NOT_FOUND exception, specifically
            pass
        
        AnnotationStorage.unset(self, name, instance, **kwargs)

registerStorage(KalturaStorage)
