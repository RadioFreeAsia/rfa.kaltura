from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoView(BrowserView):
    
    template = ViewPageTemplateFile('../skins/default/VideoView.pt')
    
    def __call__(self):
        """
        """
        return self.template()
    

class MetaView(BrowserView):
    
    template = ViewPageTemplateFile('../skins/default/VideoMeta.pt')
    
    def __call__(self):
        """
        """
        
        self.info = {'something': "Meta",
                     'another': "Metadata",
                     'testing': "you bet!"
                     }
        return self.template()
    