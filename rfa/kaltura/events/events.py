from ZPublisher.HTTPRequest import FileUpload as FileUploadClass

from rfa.kaltura.kutils import KalturaLoggerInstance as logger
from rfa.kaltura.kutils import kupload

def initVideo(context, event):
    """Fired when the object is first saved"""

    datafile = context.REQUEST.form.get('file_file')
    if isinstance(datafile, FileUploadClass):
        KMediaEntry = kupload(context)    
        context.setMediaEntry(KMediaEntry)
    else:
        logger.warning("no file uploaded on init of kaltura object %s" % (context.UID(),))

def modifyVideo(context, event):
    """Fired when the object is edited"""
    
    status = context.REQUEST.form.get('file_delete')
    if status in ("nochange", None):
        pass #not modified
    else:
        #File Modification Occured
        KMediaEntry = kupload(context)    
        context.setMediaEntry(KMediaEntry)        

    