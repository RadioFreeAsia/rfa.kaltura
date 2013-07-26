"""Definition of the Kaltura Video content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.ATContentTypes.interface.file import IATFile
from Products.ATContentTypes.interface.file import IFileContent
from plone.app.blob.content import ATBlob
from plone.app.blob.interfaces import IATBlobFile

# -*- Message Factory Imported Here -*-

from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.config import PROJECTNAME

KalturaVideoSchema = ATBlob.schema.copy() + atapi.Schema((

     atapi.StringField('title',
                       searchable=1,
                       required=True,
                       languageIndependent=1,
                       accessor="Title",
                       widget=atapi.StringWidget(label="Title",
                                                 label_msgid="label_kvideofile_title",
                                                 description="The title of this video.",
                                                 description_msgid="desc_kvideofile_title",
                                                 i18n_domain="kaltura_video"),

                       ),
     
     atapi.StringField('description',
                       searchable=1,
                       required=False,
                       widget=atapi.StringWidget(label="Description",
                                                 label_msgid="label_kvideofile_desc",
                                                 description="Enter a description",
                                                 description_msgid="desc_kvideofile_title",
                                                 i18n_domain="kaltura_video"),
                       ),
     
     atapi.FileField('VideoFile',
                     searchable=0,
                     required=True,
                     mutator='setVideoFile',
                     ),
     
     atapi.ComputedField('playbackUrl',
                 searchable=1,
                 ),
                 
     
     
    
    ),

)

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema['title'].storage = atapi.AnnotationStorage()
KalturaVideoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(KalturaVideoSchema, moveDiscussion=False)


class KalturaVideo(ATBlob):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""
    implements(IKalturaVideo, IATBlobFile, IATFile, IFileContent)

    meta_type = "KalturaVideo"
    schema = KalturaVideoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
        
        

atapi.registerType(KalturaVideo, PROJECTNAME)
