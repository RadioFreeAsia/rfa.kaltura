
from zope.interface import implements
from rfa.kaltura.storage import KalturaStorage
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('kaltura_video')
from Products.Archetypes.atapi import FileWidget
from Products.validation import V_REQUIRED
from archetypes.schemaextender.interfaces import ISchemaExtender

from plone.app.blob.subtypes.file import ExtensionBlobField

from Products.validation.config import validation
from Products.validation.validators.SupplValidators import MaxSizeValidator

validation.register(MaxSizeValidator('checkKalturaFileMaxSize', title='Kaltura Maximum video size', 
                                     description='', maxsize=500))

class SchemaExtender(object):
    implements(ISchemaExtender)

    fields = [
        ExtensionBlobField('file',
            required = True,
            primary = True,
            searchable = True,
            accessor = 'getFile',
            mutator = 'setFile',
            index_method = 'getIndexValue',
            languageIndependent = True,
            storage = KalturaStorage(migrate=True),
            default_content_type = 'application/octet-stream',
            validators = (('isNonEmptyFile', V_REQUIRED),
                          ('checkKalturaFileMaxSize', V_REQUIRED)),
            widget = FileWidget(label = _(u'label_file', default=u'Video File'),
                                description=_(u'Video File'),
                                show_content_type = False,)
            ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
