import tempfile
import os
from Acquisition import aq_base
from zope.interface import implements, Interface

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
    """ Designed specifically to work on the file field defined in kaltura.file
        Works on BlobField instances from plone.app.blob
        Connects and delivers blob binary data (videos, etc) to Kaltura as an uploaded file
        Hands off the uploaded token to the Archetype instance to finalize creation of the KalturaEntry
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
        initializing = kwargs.get('_initializing_', False)
        
        if initializing:
            AnnotationStorage.set(self, name, instance, value, **kwargs) 
            return
        
        self.value = aq_base(value)
        if self.value.filename is None:
            return #only interested in running set when instance is ready to save.
        
        #get a filehandle for the video content we are uploading to Kaltura Server
        fh_blob = openBlob(self.value.blob, mode='r')
        
        #find the temp dir that ZODB is using.
        tempdir = os.path.dirname(fh_blob.name)

        #connect to Kaltura Server
        (client, ks) = kconnect()
        #upload video content.     
        
        token = KalturaUploadToken()
        token = client.uploadToken.add(token)            
        token = client.uploadToken.upload(token.getId(), fh_blob)
        
        fh_blob.close()
        #instance needs to know the upload token to finalize the media entry
        # typically, a call to Kaltura's addFromUploadedFile or updateContent services does this.
        instance.uploadToken = token
        instance.fileChanged = True
        
        #if "no local storage" is set, we clobber the blob file.
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRfaKalturaSettings)
        if settings.storageMethod == u"No Local Storage":
            filename_aside = self.makeDummyData(dir=tempdir)
            value.blob.consumeFile(filename_aside)

        AnnotationStorage.set(self, name, instance, value, **kwargs)

    def makeDummyData(self, dir=None):
        if dir is None:
            dir = tempfile.tempdir
        fd, filename = tempfile.mkstemp(dir=dir)
        fh = os.fdopen(fd, 'w+b')
        fh.write(self.value.filename+"\n\nThis file is stored on kaltura only, and is not available via plone")
        fh.close()
        return filename
        
    def unset(self, name, instance, **kwargs):
        
        (client, ks) = kconnect()
        mediaEntry = instance.KalturaObject
        try:
            client.media.delete(mediaEntry.getId)
        except: #XXX ENTRY_ID_NOT_FOUND exception, specifically
            pass
        
        AnnotationStorage.unset(self, name, instance, **kwargs)

registerStorage(KalturaStorage)
