"""Definition of the Kaltura Video content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from rfa.kaltura.interfaces import IKalturaVideo
from rfa.kaltura.config import PROJECTNAME

KalturaVideoSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

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
     
     atapi.FileField('Video File',
                     searchable=0,
                     required=True,
                     ),
     
     atapi.ComputedField('url',
                 searchable=1,
                 ),
                 
     
     
    
    ),

)

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

KalturaVideoSchema['title'].storage = atapi.AnnotationStorage()
KalturaVideoSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(KalturaVideoSchema, moveDiscussion=False)


class KalturaVideo(base.ATCTContent):
    """Kaltura Video Content Type - stores the video file on your Kaltura account"""
    implements(IKalturaVideo)

    meta_type = "KalturaVideo"
    schema = KalturaVideoSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(KalturaVideo, PROJECTNAME)
