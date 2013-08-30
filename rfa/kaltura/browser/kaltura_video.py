from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoView(BrowserView):
    template = ViewPageTemplateFile('../skins/default/VideoView.pt')

    def __call__(self):
        """
        """
        return self.template()

    