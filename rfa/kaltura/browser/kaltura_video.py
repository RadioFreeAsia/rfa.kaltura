from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoView(BrowserView):
    
    template = ViewPageTemplateFile('../skins/default/KalturaVideo.pt')
    
    def __call__(self):
        """
        """
        
        self.info = {'something': "Video Player",
                     'another': "Video Player",
                     'testing': "you bet!"
                     }
        return self.template()
    

class MetaView(BrowserView):
    
    template = ViewPageTemplateFile('../skins/default/KalturaVideo.pt')
    
    def __call__(self):
        """
        """
        
        self.info = {'something': "Meta",
                     'another': "Metadata",
                     'testing': "you bet!"
                     }
        return self.template()
    