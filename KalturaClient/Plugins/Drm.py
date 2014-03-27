# ===================================================================================================
#                           _  __     _ _
#                          | |/ /__ _| | |_ _  _ _ _ __ _
#                          | ' </ _` | |  _| || | '_/ _` |
#                          |_|\_\__,_|_|\__|\_,_|_| \__,_|
#
# This file is part of the Kaltura Collaborative Media Suite which allows users
# to do with audio, video, and animation what Wiki platfroms allow them to do with
# text.
#
# Copyright (C) 2006-2011  Kaltura Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.
#
# @ignore
# ===================================================================================================
# @package External
# @subpackage Kaltura
from Core import *
from ..Base import *

########## enums ##########
# @package External
# @subpackage Kaltura
class KalturaDrmProfileStatus(object):
    ACTIVE = 1
    DELETED = 2

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

# @package External
# @subpackage Kaltura
class KalturaDrmProfileOrderBy(object):
    ID_ASC = "+id"
    NAME_ASC = "+name"
    ID_DESC = "-id"
    NAME_DESC = "-name"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

# @package External
# @subpackage Kaltura
class KalturaDrmProviderType(object):
    WIDEVINE = "widevine.WIDEVINE"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

########## classes ##########
# @package External
# @subpackage Kaltura
class KalturaDrmProfile(KalturaObjectBase):
    def __init__(self,
            id=NotImplemented,
            partnerId=NotImplemented,
            name=NotImplemented,
            description=NotImplemented,
            provider=NotImplemented,
            status=NotImplemented,
            licenseServerUrl=NotImplemented,
            defaultPolicy=NotImplemented,
            createdAt=NotImplemented,
            updatedAt=NotImplemented):
        KalturaObjectBase.__init__(self)

        # @var int
        # @readonly
        self.id = id

        # @var int
        # @insertonly
        self.partnerId = partnerId

        # @var string
        self.name = name

        # @var string
        self.description = description

        # @var KalturaDrmProviderType
        self.provider = provider

        # @var KalturaDrmProfileStatus
        self.status = status

        # @var string
        self.licenseServerUrl = licenseServerUrl

        # @var string
        self.defaultPolicy = defaultPolicy

        # @var int
        # @readonly
        self.createdAt = createdAt

        # @var int
        # @readonly
        self.updatedAt = updatedAt


    PROPERTY_LOADERS = {
        'id': getXmlNodeInt, 
        'partnerId': getXmlNodeInt, 
        'name': getXmlNodeText, 
        'description': getXmlNodeText, 
        'provider': (KalturaEnumsFactory.createString, "KalturaDrmProviderType"), 
        'status': (KalturaEnumsFactory.createInt, "KalturaDrmProfileStatus"), 
        'licenseServerUrl': getXmlNodeText, 
        'defaultPolicy': getXmlNodeText, 
        'createdAt': getXmlNodeInt, 
        'updatedAt': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaObjectBase.fromXml(self, node)
        self.fromXmlImpl(node, KalturaDrmProfile.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaObjectBase.toParams(self)
        kparams.put("objectType", "KalturaDrmProfile")
        kparams.addIntIfDefined("partnerId", self.partnerId)
        kparams.addStringIfDefined("name", self.name)
        kparams.addStringIfDefined("description", self.description)
        kparams.addStringEnumIfDefined("provider", self.provider)
        kparams.addIntEnumIfDefined("status", self.status)
        kparams.addStringIfDefined("licenseServerUrl", self.licenseServerUrl)
        kparams.addStringIfDefined("defaultPolicy", self.defaultPolicy)
        return kparams

    def getId(self):
        return self.id

    def getPartnerId(self):
        return self.partnerId

    def setPartnerId(self, newPartnerId):
        self.partnerId = newPartnerId

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getDescription(self):
        return self.description

    def setDescription(self, newDescription):
        self.description = newDescription

    def getProvider(self):
        return self.provider

    def setProvider(self, newProvider):
        self.provider = newProvider

    def getStatus(self):
        return self.status

    def setStatus(self, newStatus):
        self.status = newStatus

    def getLicenseServerUrl(self):
        return self.licenseServerUrl

    def setLicenseServerUrl(self, newLicenseServerUrl):
        self.licenseServerUrl = newLicenseServerUrl

    def getDefaultPolicy(self):
        return self.defaultPolicy

    def setDefaultPolicy(self, newDefaultPolicy):
        self.defaultPolicy = newDefaultPolicy

    def getCreatedAt(self):
        return self.createdAt

    def getUpdatedAt(self):
        return self.updatedAt


# @package External
# @subpackage Kaltura
class KalturaDrmProfileListResponse(KalturaObjectBase):
    def __init__(self,
            objects=NotImplemented,
            totalCount=NotImplemented):
        KalturaObjectBase.__init__(self)

        # @var array of KalturaDrmProfile
        # @readonly
        self.objects = objects

        # @var int
        # @readonly
        self.totalCount = totalCount


    PROPERTY_LOADERS = {
        'objects': (KalturaObjectFactory.createArray, KalturaDrmProfile), 
        'totalCount': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaObjectBase.fromXml(self, node)
        self.fromXmlImpl(node, KalturaDrmProfileListResponse.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaObjectBase.toParams(self)
        kparams.put("objectType", "KalturaDrmProfileListResponse")
        return kparams

    def getObjects(self):
        return self.objects

    def getTotalCount(self):
        return self.totalCount


# @package External
# @subpackage Kaltura
class KalturaDrmProfileBaseFilter(KalturaFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            partnerIdEqual=NotImplemented,
            partnerIdIn=NotImplemented,
            nameLike=NotImplemented,
            providerEqual=NotImplemented,
            providerIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented):
        KalturaFilter.__init__(self,
            orderBy,
            advancedSearch)

        # @var int
        self.idEqual = idEqual

        # @var string
        self.idIn = idIn

        # @var int
        self.partnerIdEqual = partnerIdEqual

        # @var string
        self.partnerIdIn = partnerIdIn

        # @var string
        self.nameLike = nameLike

        # @var KalturaDrmProviderType
        self.providerEqual = providerEqual

        # @var string
        self.providerIn = providerIn

        # @var KalturaDrmProfileStatus
        self.statusEqual = statusEqual

        # @var string
        self.statusIn = statusIn


    PROPERTY_LOADERS = {
        'idEqual': getXmlNodeInt, 
        'idIn': getXmlNodeText, 
        'partnerIdEqual': getXmlNodeInt, 
        'partnerIdIn': getXmlNodeText, 
        'nameLike': getXmlNodeText, 
        'providerEqual': (KalturaEnumsFactory.createString, "KalturaDrmProviderType"), 
        'providerIn': getXmlNodeText, 
        'statusEqual': (KalturaEnumsFactory.createInt, "KalturaDrmProfileStatus"), 
        'statusIn': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaDrmProfileBaseFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaFilter.toParams(self)
        kparams.put("objectType", "KalturaDrmProfileBaseFilter")
        kparams.addIntIfDefined("idEqual", self.idEqual)
        kparams.addStringIfDefined("idIn", self.idIn)
        kparams.addIntIfDefined("partnerIdEqual", self.partnerIdEqual)
        kparams.addStringIfDefined("partnerIdIn", self.partnerIdIn)
        kparams.addStringIfDefined("nameLike", self.nameLike)
        kparams.addStringEnumIfDefined("providerEqual", self.providerEqual)
        kparams.addStringIfDefined("providerIn", self.providerIn)
        kparams.addIntEnumIfDefined("statusEqual", self.statusEqual)
        kparams.addStringIfDefined("statusIn", self.statusIn)
        return kparams

    def getIdEqual(self):
        return self.idEqual

    def setIdEqual(self, newIdEqual):
        self.idEqual = newIdEqual

    def getIdIn(self):
        return self.idIn

    def setIdIn(self, newIdIn):
        self.idIn = newIdIn

    def getPartnerIdEqual(self):
        return self.partnerIdEqual

    def setPartnerIdEqual(self, newPartnerIdEqual):
        self.partnerIdEqual = newPartnerIdEqual

    def getPartnerIdIn(self):
        return self.partnerIdIn

    def setPartnerIdIn(self, newPartnerIdIn):
        self.partnerIdIn = newPartnerIdIn

    def getNameLike(self):
        return self.nameLike

    def setNameLike(self, newNameLike):
        self.nameLike = newNameLike

    def getProviderEqual(self):
        return self.providerEqual

    def setProviderEqual(self, newProviderEqual):
        self.providerEqual = newProviderEqual

    def getProviderIn(self):
        return self.providerIn

    def setProviderIn(self, newProviderIn):
        self.providerIn = newProviderIn

    def getStatusEqual(self):
        return self.statusEqual

    def setStatusEqual(self, newStatusEqual):
        self.statusEqual = newStatusEqual

    def getStatusIn(self):
        return self.statusIn

    def setStatusIn(self, newStatusIn):
        self.statusIn = newStatusIn


# @package External
# @subpackage Kaltura
class KalturaDrmProfileFilter(KalturaDrmProfileBaseFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            partnerIdEqual=NotImplemented,
            partnerIdIn=NotImplemented,
            nameLike=NotImplemented,
            providerEqual=NotImplemented,
            providerIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented):
        KalturaDrmProfileBaseFilter.__init__(self,
            orderBy,
            advancedSearch,
            idEqual,
            idIn,
            partnerIdEqual,
            partnerIdIn,
            nameLike,
            providerEqual,
            providerIn,
            statusEqual,
            statusIn)


    PROPERTY_LOADERS = {
    }

    def fromXml(self, node):
        KalturaDrmProfileBaseFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaDrmProfileFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaDrmProfileBaseFilter.toParams(self)
        kparams.put("objectType", "KalturaDrmProfileFilter")
        return kparams


########## services ##########

# @package External
# @subpackage Kaltura
class KalturaDrmProfileService(KalturaServiceBase):
    def __init__(self, client = None):
        KalturaServiceBase.__init__(self, client)

    def add(self, drmProfile):
        """Allows you to add a new DrmProfile object"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("drmProfile", drmProfile)
        self.client.queueServiceActionCall("drm_drmprofile", "add", KalturaDrmProfile, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfile)

    def get(self, drmProfileId):
        """Retrieve a KalturaDrmProfile object by ID"""

        kparams = KalturaParams()
        kparams.addIntIfDefined("drmProfileId", drmProfileId);
        self.client.queueServiceActionCall("drm_drmprofile", "get", KalturaDrmProfile, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfile)

    def update(self, drmProfileId, drmProfile):
        """Update an existing KalturaDrmProfile object"""

        kparams = KalturaParams()
        kparams.addIntIfDefined("drmProfileId", drmProfileId);
        kparams.addObjectIfDefined("drmProfile", drmProfile)
        self.client.queueServiceActionCall("drm_drmprofile", "update", KalturaDrmProfile, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfile)

    def delete(self, drmProfileId):
        """Mark the KalturaDrmProfile object as deleted"""

        kparams = KalturaParams()
        kparams.addIntIfDefined("drmProfileId", drmProfileId);
        self.client.queueServiceActionCall("drm_drmprofile", "delete", KalturaDrmProfile, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfile)

    def list(self, filter = NotImplemented, pager = NotImplemented):
        """List KalturaDrmProfile objects"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall("drm_drmprofile", "list", KalturaDrmProfileListResponse, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfileListResponse)

    def getByProvider(self, provider):
        """Retrieve a KalturaDrmProfile object by provider, if no specific profile defined return default profile"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("provider", provider)
        self.client.queueServiceActionCall("drm_drmprofile", "getByProvider", KalturaDrmProfile, kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaDrmProfile)

########## main ##########
class KalturaDrmClientPlugin(KalturaClientPlugin):
    # KalturaDrmClientPlugin
    instance = None

    # @return KalturaDrmClientPlugin
    @staticmethod
    def get():
        if KalturaDrmClientPlugin.instance == None:
            KalturaDrmClientPlugin.instance = KalturaDrmClientPlugin()
        return KalturaDrmClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
            'drmProfile': KalturaDrmProfileService,
        }

    def getEnums(self):
        return {
            'KalturaDrmProfileStatus': KalturaDrmProfileStatus,
            'KalturaDrmProfileOrderBy': KalturaDrmProfileOrderBy,
            'KalturaDrmProviderType': KalturaDrmProviderType,
        }

    def getTypes(self):
        return {
            'KalturaDrmProfile': KalturaDrmProfile,
            'KalturaDrmProfileListResponse': KalturaDrmProfileListResponse,
            'KalturaDrmProfileBaseFilter': KalturaDrmProfileBaseFilter,
            'KalturaDrmProfileFilter': KalturaDrmProfileFilter,
        }

    # @return string
    def getName(self):
        return 'drm'

