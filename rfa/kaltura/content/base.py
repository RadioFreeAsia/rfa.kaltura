"""Base Schemas and classes for Kaltura AT Classes"""
from Products.Archetypes import atapi

from AccessControl import ClassSecurityInfo

from rfa.kaltura.content import vocabularies
from rfa.kaltura.credentials import getCredentials

KalturaBaseSchema = atapi.Schema(
    (atapi.StringField('entryId',
                       searchable=0,
                       mode='r',
                       accesssor="getEntryId",
                       widget=atapi.ComputedWidget(label="Entry Id",
                                                 description="Entry Id set by Kaltura after upload (read only)",
                                                 visible = { 'edit' :'visible', 'view' : 'visible' },
                                                 i18n_domain="kaltura_video"),
                       ),
     
     #sub-classes that use this schema may alter this field 
     # to use a selection widget and a vocabulary
     # if not, it's a simple string field where you type in the playerId (aka ui_conf) manually.
     atapi.StringField('playerId',
                       searchable=0,
                       accessor="getPlayer",
                       mutator="setPlayer", 
                       mode='rw',
                       default_method="getDefaultPlayerId",
                       widget=atapi.StringWidget(label="Player Id",
                                                label_msgid="label_kplayerid_msgid",
                                                description="Enter the Player Id to use",
                                                description_msgid="desc_kplayerid_msgid",
                                                i18n_domain="kaltura_video"),
                      ),         
     
     atapi.StringField('partnerId',
                       searchable=0,
                       mode='rw',
                       default_method="getDefaultPartnerId",
                       widget=atapi.StringWidget(label="Partner Id",
                                                 label_msgid="label_kpartnerid_msgid",
                                                 description="Kaltura Partner Id (use default if unsure)",
                                                 description_msgid="desc_kpartnerid_msgid",
                                                 i18n_domain="kaltura_video"),
                       
                                             
                       ),
     )
     
)

#this seems misnamed
KalturaMetadataSchema = atapi.Schema(
    (atapi.LinesField('categories',
                      multiValued = True,
                      searchable=0,
                      required=False,
                      vocabulary="getCategoryVocabulary",
                      accessor="getCategories",
                      mutator="setCategories",
                      widget=atapi.MultiSelectionWidget(label="Categories",
                                                        label_msgid="label_kvideofile_categories",
                                                        description="Select video category(ies) this playlist will provide",
                                                        description_msgid="desc_kvideofile_categories",
                                                        i18n_domain="kaltura_video"),
                          ),       
    
     atapi.LinesField('tags',
                      multiValued = True,
                      searchable=0,
                      required=False,
                      accessor="getTags",
                      mutator="setTags",
                      widget=atapi.LinesWidget(label="Tags",
                                               label_msgid="label_kvideofile_tags",
                                               description="Add keyword tag(s) this playlist will provide (one per line)",
                                               description_msgid="desc_kvideofile_title",
                                               i18n_domain="kaltura_video"),
                      ),
     )
)

###XXX Todo: create base class ExternalMediaEntry 
##based off of http://www.kaltura.com/api_v3/testmeDoc/index.php?object=KalturaExternalMediaEntry

class KalturaContentMixin(object):
    
    security = ClassSecurityInfo()
    KalturaObject = None    
    categories = []
    tags = []    
    
    def __init__(self, oid, **kwargs):
        super(KalturaContentMixin, self).__init__(oid, **kwargs)
        self.KalturaObject = None

    security.declarePrivate("setKalturaObject")
    def setKalturaObject(self, obj):
        self.KalturaObject = obj
        self.KalturaObject.referenceId = self.UID()
        
    security.declarePublic("getEntryId")
    def getEntryId(self):
        if self.KalturaObject is not None:
            return self.KalturaObject.getId()
        else:
            return None     
    entryId = property(getEntryId)            
        
    security.declarePrivate('getDefaultPartnerId')
    def getDefaultPartnerId(self):
        return getCredentials()['PARTNER_ID']    

    def getTags(self):
        return self.tags
    
    def setTags(self, tags):
        self.tags = tags
        
    def getCategories(self):
        return self.categories
    
    def setCategories(self, categories):
        self.categories = categories    

    def getTagVocabulary(self):
        return vocabularies.getTagVoculabulary()
        
    def getCategoryVocabulary(self):
        return vocabularies.getCategoryVocabulary()
    