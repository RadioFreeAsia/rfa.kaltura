from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoView(BrowserView):
    
    def playbackUrl(self):
        return self.context.getPlaybackUrl()
    
    
    