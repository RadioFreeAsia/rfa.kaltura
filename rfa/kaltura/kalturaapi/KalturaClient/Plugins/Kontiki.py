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
class KalturaKontikiStorageProfileOrderBy(object):
    CREATED_AT_ASC = "+createdAt"
    UPDATED_AT_ASC = "+updatedAt"
    CREATED_AT_DESC = "-createdAt"
    UPDATED_AT_DESC = "-updatedAt"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

########## classes ##########
# @package External
# @subpackage Kaltura
class KalturaKontikiStorageProfile(KalturaStorageProfile):
    def __init__(self,
            id=NotImplemented,
            createdAt=NotImplemented,
            updatedAt=NotImplemented,
            partnerId=NotImplemented,
            name=NotImplemented,
            systemName=NotImplemented,
            desciption=NotImplemented,
            status=NotImplemented,
            protocol=NotImplemented,
            storageUrl=NotImplemented,
            storageBaseDir=NotImplemented,
            storageUsername=NotImplemented,
            storagePassword=NotImplemented,
            storageFtpPassiveMode=NotImplemented,
            deliveryHttpBaseUrl=NotImplemented,
            deliveryHttpsBaseUrl=NotImplemented,
            deliveryRmpBaseUrl=NotImplemented,
            deliveryIisBaseUrl=NotImplemented,
            minFileSize=NotImplemented,
            maxFileSize=NotImplemented,
            flavorParamsIds=NotImplemented,
            maxConcurrentConnections=NotImplemented,
            pathManagerClass=NotImplemented,
            pathManagerParams=NotImplemented,
            urlManagerClass=NotImplemented,
            urlManagerParams=NotImplemented,
            trigger=NotImplemented,
            deliveryPriority=NotImplemented,
            deliveryStatus=NotImplemented,
            rtmpPrefix=NotImplemented,
            readyBehavior=NotImplemented,
            allowAutoDelete=NotImplemented,
            createFileLink=NotImplemented,
            rules=NotImplemented,
            serviceToken=NotImplemented):
        KalturaStorageProfile.__init__(self,
            id,
            createdAt,
            updatedAt,
            partnerId,
            name,
            systemName,
            desciption,
            status,
            protocol,
            storageUrl,
            storageBaseDir,
            storageUsername,
            storagePassword,
            storageFtpPassiveMode,
            deliveryHttpBaseUrl,
            deliveryHttpsBaseUrl,
            deliveryRmpBaseUrl,
            deliveryIisBaseUrl,
            minFileSize,
            maxFileSize,
            flavorParamsIds,
            maxConcurrentConnections,
            pathManagerClass,
            pathManagerParams,
            urlManagerClass,
            urlManagerParams,
            trigger,
            deliveryPriority,
            deliveryStatus,
            rtmpPrefix,
            readyBehavior,
            allowAutoDelete,
            createFileLink,
            rules)

        # @var string
        self.serviceToken = serviceToken


    PROPERTY_LOADERS = {
        'serviceToken': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaStorageProfile.fromXml(self, node)
        self.fromXmlImpl(node, KalturaKontikiStorageProfile.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaStorageProfile.toParams(self)
        kparams.put("objectType", "KalturaKontikiStorageProfile")
        kparams.addStringIfDefined("serviceToken", self.serviceToken)
        return kparams

    def getServiceToken(self):
        return self.serviceToken

    def setServiceToken(self, newServiceToken):
        self.serviceToken = newServiceToken


# @package External
# @subpackage Kaltura
class KalturaKontikiStorageDeleteJobData(KalturaStorageDeleteJobData):
    def __init__(self,
            serverUrl=NotImplemented,
            serverUsername=NotImplemented,
            serverPassword=NotImplemented,
            ftpPassiveMode=NotImplemented,
            srcFileSyncLocalPath=NotImplemented,
            srcFileSyncId=NotImplemented,
            destFileSyncStoredPath=NotImplemented,
            contentMoid=NotImplemented,
            serviceToken=NotImplemented):
        KalturaStorageDeleteJobData.__init__(self,
            serverUrl,
            serverUsername,
            serverPassword,
            ftpPassiveMode,
            srcFileSyncLocalPath,
            srcFileSyncId,
            destFileSyncStoredPath)

        # Unique Kontiki MOID for the content uploaded to Kontiki
        # @var string
        self.contentMoid = contentMoid

        # @var string
        self.serviceToken = serviceToken


    PROPERTY_LOADERS = {
        'contentMoid': getXmlNodeText, 
        'serviceToken': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaStorageDeleteJobData.fromXml(self, node)
        self.fromXmlImpl(node, KalturaKontikiStorageDeleteJobData.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaStorageDeleteJobData.toParams(self)
        kparams.put("objectType", "KalturaKontikiStorageDeleteJobData")
        kparams.addStringIfDefined("contentMoid", self.contentMoid)
        kparams.addStringIfDefined("serviceToken", self.serviceToken)
        return kparams

    def getContentMoid(self):
        return self.contentMoid

    def setContentMoid(self, newContentMoid):
        self.contentMoid = newContentMoid

    def getServiceToken(self):
        return self.serviceToken

    def setServiceToken(self, newServiceToken):
        self.serviceToken = newServiceToken


# @package External
# @subpackage Kaltura
class KalturaKontikiStorageExportJobData(KalturaStorageExportJobData):
    def __init__(self,
            serverUrl=NotImplemented,
            serverUsername=NotImplemented,
            serverPassword=NotImplemented,
            ftpPassiveMode=NotImplemented,
            srcFileSyncLocalPath=NotImplemented,
            srcFileSyncId=NotImplemented,
            destFileSyncStoredPath=NotImplemented,
            force=NotImplemented,
            createLink=NotImplemented,
            flavorAssetId=NotImplemented,
            contentMoid=NotImplemented,
            serviceToken=NotImplemented):
        KalturaStorageExportJobData.__init__(self,
            serverUrl,
            serverUsername,
            serverPassword,
            ftpPassiveMode,
            srcFileSyncLocalPath,
            srcFileSyncId,
            destFileSyncStoredPath,
            force,
            createLink)

        # Holds the id of the exported asset
        # @var string
        self.flavorAssetId = flavorAssetId

        # Unique Kontiki MOID for the content uploaded to Kontiki
        # @var string
        self.contentMoid = contentMoid

        # @var string
        self.serviceToken = serviceToken


    PROPERTY_LOADERS = {
        'flavorAssetId': getXmlNodeText, 
        'contentMoid': getXmlNodeText, 
        'serviceToken': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaStorageExportJobData.fromXml(self, node)
        self.fromXmlImpl(node, KalturaKontikiStorageExportJobData.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaStorageExportJobData.toParams(self)
        kparams.put("objectType", "KalturaKontikiStorageExportJobData")
        kparams.addStringIfDefined("flavorAssetId", self.flavorAssetId)
        kparams.addStringIfDefined("contentMoid", self.contentMoid)
        kparams.addStringIfDefined("serviceToken", self.serviceToken)
        return kparams

    def getFlavorAssetId(self):
        return self.flavorAssetId

    def setFlavorAssetId(self, newFlavorAssetId):
        self.flavorAssetId = newFlavorAssetId

    def getContentMoid(self):
        return self.contentMoid

    def setContentMoid(self, newContentMoid):
        self.contentMoid = newContentMoid

    def getServiceToken(self):
        return self.serviceToken

    def setServiceToken(self, newServiceToken):
        self.serviceToken = newServiceToken


# @package External
# @subpackage Kaltura
class KalturaKontikiStorageProfileBaseFilter(KalturaStorageProfileFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            createdAtGreaterThanOrEqual=NotImplemented,
            createdAtLessThanOrEqual=NotImplemented,
            updatedAtGreaterThanOrEqual=NotImplemented,
            updatedAtLessThanOrEqual=NotImplemented,
            partnerIdEqual=NotImplemented,
            partnerIdIn=NotImplemented,
            systemNameEqual=NotImplemented,
            systemNameIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented,
            protocolEqual=NotImplemented,
            protocolIn=NotImplemented):
        KalturaStorageProfileFilter.__init__(self,
            orderBy,
            advancedSearch,
            idEqual,
            idIn,
            createdAtGreaterThanOrEqual,
            createdAtLessThanOrEqual,
            updatedAtGreaterThanOrEqual,
            updatedAtLessThanOrEqual,
            partnerIdEqual,
            partnerIdIn,
            systemNameEqual,
            systemNameIn,
            statusEqual,
            statusIn,
            protocolEqual,
            protocolIn)


    PROPERTY_LOADERS = {
    }

    def fromXml(self, node):
        KalturaStorageProfileFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaKontikiStorageProfileBaseFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaStorageProfileFilter.toParams(self)
        kparams.put("objectType", "KalturaKontikiStorageProfileBaseFilter")
        return kparams


# @package External
# @subpackage Kaltura
class KalturaKontikiStorageProfileFilter(KalturaKontikiStorageProfileBaseFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            createdAtGreaterThanOrEqual=NotImplemented,
            createdAtLessThanOrEqual=NotImplemented,
            updatedAtGreaterThanOrEqual=NotImplemented,
            updatedAtLessThanOrEqual=NotImplemented,
            partnerIdEqual=NotImplemented,
            partnerIdIn=NotImplemented,
            systemNameEqual=NotImplemented,
            systemNameIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented,
            protocolEqual=NotImplemented,
            protocolIn=NotImplemented):
        KalturaKontikiStorageProfileBaseFilter.__init__(self,
            orderBy,
            advancedSearch,
            idEqual,
            idIn,
            createdAtGreaterThanOrEqual,
            createdAtLessThanOrEqual,
            updatedAtGreaterThanOrEqual,
            updatedAtLessThanOrEqual,
            partnerIdEqual,
            partnerIdIn,
            systemNameEqual,
            systemNameIn,
            statusEqual,
            statusIn,
            protocolEqual,
            protocolIn)


    PROPERTY_LOADERS = {
    }

    def fromXml(self, node):
        KalturaKontikiStorageProfileBaseFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaKontikiStorageProfileFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaKontikiStorageProfileBaseFilter.toParams(self)
        kparams.put("objectType", "KalturaKontikiStorageProfileFilter")
        return kparams


########## services ##########
########## main ##########
class KalturaKontikiClientPlugin(KalturaClientPlugin):
    # KalturaKontikiClientPlugin
    instance = None

    # @return KalturaKontikiClientPlugin
    @staticmethod
    def get():
        if KalturaKontikiClientPlugin.instance == None:
            KalturaKontikiClientPlugin.instance = KalturaKontikiClientPlugin()
        return KalturaKontikiClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
        }

    def getEnums(self):
        return {
            'KalturaKontikiStorageProfileOrderBy': KalturaKontikiStorageProfileOrderBy,
        }

    def getTypes(self):
        return {
            'KalturaKontikiStorageProfile': KalturaKontikiStorageProfile,
            'KalturaKontikiStorageDeleteJobData': KalturaKontikiStorageDeleteJobData,
            'KalturaKontikiStorageExportJobData': KalturaKontikiStorageExportJobData,
            'KalturaKontikiStorageProfileBaseFilter': KalturaKontikiStorageProfileBaseFilter,
            'KalturaKontikiStorageProfileFilter': KalturaKontikiStorageProfileFilter,
        }

    # @return string
    def getName(self):
        return 'kontiki'

