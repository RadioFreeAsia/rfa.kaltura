from zope.interface import Interface
from zope import schema


class IATKalturaVideo(Interface):
    """Interface for handling a KalturaVideo content type
    """
    
    def getVideoURL():
        """ Get the URL for the video"""
        
    
class IKalturaVideo(Interface):
    """A pythonic representation of an object that 
    contains a KalturaVideo reference
    """
    
    title = schema.TextLine(title=u'Title')
    description = schema.Text(title=u'Description', 
                              required=False)
    filename = schema.TextLine(title=u'Filename')  
    url = schema.TextLine(title=u'URL', readonly=True)
    