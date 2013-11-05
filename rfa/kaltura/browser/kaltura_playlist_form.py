from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')

class IKalturaPlaylistForm(Interface):    
    title = schema.TextLine(title=_(u'Title'), 
                            required=False)
    description = schema.Text(title=u'Description', 
                              required=False)
    filename = schema.TextLine(title=u'Filename')  
    url = schema.TextLine(title=u'URL', readonly=True)
    
    
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form, field

class KalturaPlaylistForm(form.Form):
    fields = field.Fields(IKalturaVideoForm)
    ignoreContext = True
    
    def updateWidgets(self):
        super(KalturaVideoForm, self).updateWidgets()


    @button.buttonAndHandler(u'Save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        
        if data['title'] is not None:
            title = data['title']
        else:
            title = ''
            IStatusMessage(self.request).addStatusMessage("you got away with not adding a title")
            
        if data['description'] is not None:
            description = data['description']
        else:
            description = ''
            
        IStatusMessage(self.request).addStatusMessage(
                "Playlist Saved",
                'info')
        
        redirect_url = "%s/@@kaltura_playlist_form" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)    


    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            "Canceled",
            'info')
        redirect_url = "%s/@@kaltura_playlist_form" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)    
        
        
from plone.z3cform.layout import wrap_form
KalturaVideoFormView = wrap_form(KalturaVideoForm)