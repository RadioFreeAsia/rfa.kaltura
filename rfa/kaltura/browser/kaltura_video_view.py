from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class KalturaVideoView(BrowserView):
    
    template = ViewPageTemplateFile('KalturaVideo.pt')
    
    def __call__(self):
        """
        """
        
        self.info = {'something': "special",
                     'another': "very special",
                     'testing': "you bet!"
                     }
        return self.template()
    
    