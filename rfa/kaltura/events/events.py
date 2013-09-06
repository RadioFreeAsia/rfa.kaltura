import logging

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from rfa.kaltura.kalturaapi.KalturaClient import *

from rfa.kaltura import credentials

logger = logging.getLogger("rfa.kaltura")

class KalturaLogger(IKalturaLogger):
    def log(self, msg, summary='', level=logging.INFO):
        logger.log(level, '%s \n%s', summary, msg)    
    
    
LoggerInstance = KalturaLogger()

def modifyVideo(context, event):
    
    KMediaEntry = kupload(context)
    LoggerInstance.log("uploaded.  MediaEntry %s" % (KMediaEntry.__repr__()),
                        summary="events.modifyVideo")    
    
    context.setMediaEntry(KMediaEntry)
    
def kupload(FileObject):
    """Provide an ATCTFileContent based object
       Upload attached contents to Kaltura
       Currently Treats all objects as 'videos' - this should change
    """
    
    creds = credentials.getCredentials()
    
    #this check can be done better
    if not hasattr(FileObject, 'get_data'):
        print "nothing to upload to kaltura from object %s" % (str(FileObject),)
        return 1;
    
    #XXX Configure Temporary Directory and name better
    #XXX Turn into a file stream from context.get_data to avoid write to file...        
    tempfh = open('/tmp/tempfile', 'wr')
    tempfh.write(FileObject.get_data())
    tempfh.close()    
    
    name = FileObject.Title()
    ProviderId = FileObject.UID()
    
    config = KalturaConfiguration(creds['PARTNER_ID'])
    config.serviceUrl = creds['SERVICE_URL']
    config.setLogger(LoggerInstance)
    
    client = KalturaClient(config)
    
    

    # start new session (client session is enough when we do operations in a users scope)
    ks = client.generateSession(creds['ADMIN_SECRET'], 
                                creds['USER_NAME'],
                                KalturaSessionType.ADMIN, 
                                creds['PARTNER_ID'],
                                86400,   #XXX look up what this does...
                                "")    
    client.setKs(ks)
        
    #create an entry
    mediaEntry = KalturaMediaEntry()
    mediaEntry.setName(name)
    mediaEntry.setMediaType(KalturaMediaType(KalturaMediaType.VIDEO))
    mediaEntry.searchProviderId = ProviderId

    
    #do the upload
    uploadTokenId = client.media.upload(file('/tmp/tempfile', 'rb'))  
    
    #del the temp file
    os.remove('/tmp/tempfile')
    
    mediaEntry = client.media.addFromUploadedFile(mediaEntry, uploadTokenId)
    
    return mediaEntry

    