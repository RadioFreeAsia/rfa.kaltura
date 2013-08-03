import logging

from zope.lifecycleevent.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from rfa.kaltura.kalturaapi.KalturaClient import *

from rfa.kaltura.config import PARTNER_ID, SECRET, ADMIN_SECRET, SERVICE_URL, USER_NAME

logger = logging.getLogger("rfa.kaltura")

class KalturaLogger(IKalturaLogger):
    def log(self, msg, summary='', level=logging.INFO):
        logger.log(level, '%s \n%s', summary, msg)    
    
    
LoggerInstance = KalturaLogger()

def modifyVideo(context, event):
    
    LoggerInstance.log("modifyVideo Event!",
                       summary="events.modifyVideo")
    
    url = kupload(context)
    LoggerInstance.log("uploaded.  URL is %s" % (url,),
                        summary="events.modifyVideo")    
    
    context.setPlaybackUrl(url)
    
def kupload(FileObject):
    """Provide an ATCTFileContent based object
       Upload attached contents to Kaltura
       Currently Treats all objects as 'videos' - this should change
    """
    
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
    
    config = KalturaConfiguration(PARTNER_ID)
    config.serviceUrl = SERVICE_URL
    config.setLogger(LoggerInstance)
    
    client = KalturaClient(config)
    
    

    # start new session (client session is enough when we do operations in a users scope)
    ks = client.generateSession(ADMIN_SECRET, USER_NAME, KalturaSessionType.ADMIN, PARTNER_ID, 86400, "")    
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
    
    #grab the playback url
    return mediaEntry.dataUrl

    