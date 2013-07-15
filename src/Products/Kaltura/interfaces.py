from zope.interface import Interface

class IKalturaVideo(Interface):
    """Interface for handling a KalturaVideo content type
    """
    
    def getVideoURL():
        """ Get the URL for the video"""
        
    
