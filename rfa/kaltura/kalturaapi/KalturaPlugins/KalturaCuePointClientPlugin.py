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
import os.path
import sys

clientRoot = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

from KalturaCoreClient import *
from KalturaClientBase import *

########## enums ##########
# @package External
# @subpackage Kaltura
class KalturaCuePointStatus:
    READY = 1
    DELETED = 2

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

# @package External
# @subpackage Kaltura
class KalturaCuePointOrderBy:
    CREATED_AT_ASC = "+createdAt"
    PARTNER_SORT_VALUE_ASC = "+partnerSortValue"
    START_TIME_ASC = "+startTime"
    UPDATED_AT_ASC = "+updatedAt"
    CREATED_AT_DESC = "-createdAt"
    PARTNER_SORT_VALUE_DESC = "-partnerSortValue"
    START_TIME_DESC = "-startTime"
    UPDATED_AT_DESC = "-updatedAt"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

# @package External
# @subpackage Kaltura
class KalturaCuePointType:
    AD = "adCuePoint.Ad"
    ANNOTATION = "annotation.Annotation"
    CODE = "codeCuePoint.Code"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

########## classes ##########
# @package External
# @subpackage Kaltura
class KalturaCuePoint(KalturaObjectBase):
    def __init__(self,
            id=NotImplemented,
            cuePointType=NotImplemented,
            status=NotImplemented,
            entryId=NotImplemented,
            partnerId=NotImplemented,
            createdAt=NotImplemented,
            updatedAt=NotImplemented,
            tags=NotImplemented,
            startTime=NotImplemented,
            userId=NotImplemented,
            partnerData=NotImplemented,
            partnerSortValue=NotImplemented,
            forceStop=NotImplemented,
            thumbOffset=NotImplemented,
            systemName=NotImplemented):
        KalturaObjectBase.__init__(self)

        # @var string
        # @readonly
        self.id = id

        # @var KalturaCuePointType
        # @readonly
        self.cuePointType = cuePointType

        # @var KalturaCuePointStatus
        # @readonly
        self.status = status

        # @var string
        # @insertonly
        self.entryId = entryId

        # @var int
        # @readonly
        self.partnerId = partnerId

        # @var int
        # @readonly
        self.createdAt = createdAt

        # @var int
        # @readonly
        self.updatedAt = updatedAt

        # @var string
        self.tags = tags

        # Start time in milliseconds
        # @var int
        self.startTime = startTime

        # @var string
        # @readonly
        self.userId = userId

        # @var string
        self.partnerData = partnerData

        # @var int
        self.partnerSortValue = partnerSortValue

        # @var KalturaNullableBoolean
        self.forceStop = forceStop

        # @var int
        self.thumbOffset = thumbOffset

        # @var string
        self.systemName = systemName


    PROPERTY_LOADERS = {
        'id': getXmlNodeText, 
        'cuePointType': (KalturaEnumsFactory.createString, "KalturaCuePointType"), 
        'status': (KalturaEnumsFactory.createInt, "KalturaCuePointStatus"), 
        'entryId': getXmlNodeText, 
        'partnerId': getXmlNodeInt, 
        'createdAt': getXmlNodeInt, 
        'updatedAt': getXmlNodeInt, 
        'tags': getXmlNodeText, 
        'startTime': getXmlNodeInt, 
        'userId': getXmlNodeText, 
        'partnerData': getXmlNodeText, 
        'partnerSortValue': getXmlNodeInt, 
        'forceStop': (KalturaEnumsFactory.createInt, "KalturaNullableBoolean"), 
        'thumbOffset': getXmlNodeInt, 
        'systemName': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaObjectBase.fromXml(self, node)
        self.fromXmlImpl(node, KalturaCuePoint.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaObjectBase.toParams(self)
        kparams.put("objectType", "KalturaCuePoint")
        kparams.addStringIfDefined("entryId", self.entryId)
        kparams.addStringIfDefined("tags", self.tags)
        kparams.addIntIfDefined("startTime", self.startTime)
        kparams.addStringIfDefined("partnerData", self.partnerData)
        kparams.addIntIfDefined("partnerSortValue", self.partnerSortValue)
        kparams.addIntEnumIfDefined("forceStop", self.forceStop)
        kparams.addIntIfDefined("thumbOffset", self.thumbOffset)
        kparams.addStringIfDefined("systemName", self.systemName)
        return kparams

    def getId(self):
        return self.id

    def getCuePointType(self):
        return self.cuePointType

    def getStatus(self):
        return self.status

    def getEntryId(self):
        return self.entryId

    def setEntryId(self, newEntryId):
        self.entryId = newEntryId

    def getPartnerId(self):
        return self.partnerId

    def getCreatedAt(self):
        return self.createdAt

    def getUpdatedAt(self):
        return self.updatedAt

    def getTags(self):
        return self.tags

    def setTags(self, newTags):
        self.tags = newTags

    def getStartTime(self):
        return self.startTime

    def setStartTime(self, newStartTime):
        self.startTime = newStartTime

    def getUserId(self):
        return self.userId

    def getPartnerData(self):
        return self.partnerData

    def setPartnerData(self, newPartnerData):
        self.partnerData = newPartnerData

    def getPartnerSortValue(self):
        return self.partnerSortValue

    def setPartnerSortValue(self, newPartnerSortValue):
        self.partnerSortValue = newPartnerSortValue

    def getForceStop(self):
        return self.forceStop

    def setForceStop(self, newForceStop):
        self.forceStop = newForceStop

    def getThumbOffset(self):
        return self.thumbOffset

    def setThumbOffset(self, newThumbOffset):
        self.thumbOffset = newThumbOffset

    def getSystemName(self):
        return self.systemName

    def setSystemName(self, newSystemName):
        self.systemName = newSystemName


# @package External
# @subpackage Kaltura
class KalturaCuePointListResponse(KalturaObjectBase):
    def __init__(self,
            objects=NotImplemented,
            totalCount=NotImplemented):
        KalturaObjectBase.__init__(self)

        # @var array of KalturaCuePoint
        # @readonly
        self.objects = objects

        # @var int
        # @readonly
        self.totalCount = totalCount


    PROPERTY_LOADERS = {
        'objects': (KalturaObjectFactory.createArray, KalturaCuePoint), 
        'totalCount': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaObjectBase.fromXml(self, node)
        self.fromXmlImpl(node, KalturaCuePointListResponse.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaObjectBase.toParams(self)
        kparams.put("objectType", "KalturaCuePointListResponse")
        return kparams

    def getObjects(self):
        return self.objects

    def getTotalCount(self):
        return self.totalCount


# @package External
# @subpackage Kaltura
class KalturaCuePointBaseFilter(KalturaFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            cuePointTypeEqual=NotImplemented,
            cuePointTypeIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented,
            entryIdEqual=NotImplemented,
            entryIdIn=NotImplemented,
            createdAtGreaterThanOrEqual=NotImplemented,
            createdAtLessThanOrEqual=NotImplemented,
            updatedAtGreaterThanOrEqual=NotImplemented,
            updatedAtLessThanOrEqual=NotImplemented,
            tagsLike=NotImplemented,
            tagsMultiLikeOr=NotImplemented,
            tagsMultiLikeAnd=NotImplemented,
            startTimeGreaterThanOrEqual=NotImplemented,
            startTimeLessThanOrEqual=NotImplemented,
            userIdEqual=NotImplemented,
            userIdIn=NotImplemented,
            partnerSortValueEqual=NotImplemented,
            partnerSortValueIn=NotImplemented,
            partnerSortValueGreaterThanOrEqual=NotImplemented,
            partnerSortValueLessThanOrEqual=NotImplemented,
            forceStopEqual=NotImplemented,
            systemNameEqual=NotImplemented,
            systemNameIn=NotImplemented):
        KalturaFilter.__init__(self,
            orderBy,
            advancedSearch)

        # @var string
        self.idEqual = idEqual

        # @var string
        self.idIn = idIn

        # @var KalturaCuePointType
        self.cuePointTypeEqual = cuePointTypeEqual

        # @var string
        self.cuePointTypeIn = cuePointTypeIn

        # @var KalturaCuePointStatus
        self.statusEqual = statusEqual

        # @var string
        self.statusIn = statusIn

        # @var string
        self.entryIdEqual = entryIdEqual

        # @var string
        self.entryIdIn = entryIdIn

        # @var int
        self.createdAtGreaterThanOrEqual = createdAtGreaterThanOrEqual

        # @var int
        self.createdAtLessThanOrEqual = createdAtLessThanOrEqual

        # @var int
        self.updatedAtGreaterThanOrEqual = updatedAtGreaterThanOrEqual

        # @var int
        self.updatedAtLessThanOrEqual = updatedAtLessThanOrEqual

        # @var string
        self.tagsLike = tagsLike

        # @var string
        self.tagsMultiLikeOr = tagsMultiLikeOr

        # @var string
        self.tagsMultiLikeAnd = tagsMultiLikeAnd

        # @var int
        self.startTimeGreaterThanOrEqual = startTimeGreaterThanOrEqual

        # @var int
        self.startTimeLessThanOrEqual = startTimeLessThanOrEqual

        # @var string
        self.userIdEqual = userIdEqual

        # @var string
        self.userIdIn = userIdIn

        # @var int
        self.partnerSortValueEqual = partnerSortValueEqual

        # @var string
        self.partnerSortValueIn = partnerSortValueIn

        # @var int
        self.partnerSortValueGreaterThanOrEqual = partnerSortValueGreaterThanOrEqual

        # @var int
        self.partnerSortValueLessThanOrEqual = partnerSortValueLessThanOrEqual

        # @var KalturaNullableBoolean
        self.forceStopEqual = forceStopEqual

        # @var string
        self.systemNameEqual = systemNameEqual

        # @var string
        self.systemNameIn = systemNameIn


    PROPERTY_LOADERS = {
        'idEqual': getXmlNodeText, 
        'idIn': getXmlNodeText, 
        'cuePointTypeEqual': (KalturaEnumsFactory.createString, "KalturaCuePointType"), 
        'cuePointTypeIn': getXmlNodeText, 
        'statusEqual': (KalturaEnumsFactory.createInt, "KalturaCuePointStatus"), 
        'statusIn': getXmlNodeText, 
        'entryIdEqual': getXmlNodeText, 
        'entryIdIn': getXmlNodeText, 
        'createdAtGreaterThanOrEqual': getXmlNodeInt, 
        'createdAtLessThanOrEqual': getXmlNodeInt, 
        'updatedAtGreaterThanOrEqual': getXmlNodeInt, 
        'updatedAtLessThanOrEqual': getXmlNodeInt, 
        'tagsLike': getXmlNodeText, 
        'tagsMultiLikeOr': getXmlNodeText, 
        'tagsMultiLikeAnd': getXmlNodeText, 
        'startTimeGreaterThanOrEqual': getXmlNodeInt, 
        'startTimeLessThanOrEqual': getXmlNodeInt, 
        'userIdEqual': getXmlNodeText, 
        'userIdIn': getXmlNodeText, 
        'partnerSortValueEqual': getXmlNodeInt, 
        'partnerSortValueIn': getXmlNodeText, 
        'partnerSortValueGreaterThanOrEqual': getXmlNodeInt, 
        'partnerSortValueLessThanOrEqual': getXmlNodeInt, 
        'forceStopEqual': (KalturaEnumsFactory.createInt, "KalturaNullableBoolean"), 
        'systemNameEqual': getXmlNodeText, 
        'systemNameIn': getXmlNodeText, 
    }

    def fromXml(self, node):
        KalturaFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaCuePointBaseFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaFilter.toParams(self)
        kparams.put("objectType", "KalturaCuePointBaseFilter")
        kparams.addStringIfDefined("idEqual", self.idEqual)
        kparams.addStringIfDefined("idIn", self.idIn)
        kparams.addStringEnumIfDefined("cuePointTypeEqual", self.cuePointTypeEqual)
        kparams.addStringIfDefined("cuePointTypeIn", self.cuePointTypeIn)
        kparams.addIntEnumIfDefined("statusEqual", self.statusEqual)
        kparams.addStringIfDefined("statusIn", self.statusIn)
        kparams.addStringIfDefined("entryIdEqual", self.entryIdEqual)
        kparams.addStringIfDefined("entryIdIn", self.entryIdIn)
        kparams.addIntIfDefined("createdAtGreaterThanOrEqual", self.createdAtGreaterThanOrEqual)
        kparams.addIntIfDefined("createdAtLessThanOrEqual", self.createdAtLessThanOrEqual)
        kparams.addIntIfDefined("updatedAtGreaterThanOrEqual", self.updatedAtGreaterThanOrEqual)
        kparams.addIntIfDefined("updatedAtLessThanOrEqual", self.updatedAtLessThanOrEqual)
        kparams.addStringIfDefined("tagsLike", self.tagsLike)
        kparams.addStringIfDefined("tagsMultiLikeOr", self.tagsMultiLikeOr)
        kparams.addStringIfDefined("tagsMultiLikeAnd", self.tagsMultiLikeAnd)
        kparams.addIntIfDefined("startTimeGreaterThanOrEqual", self.startTimeGreaterThanOrEqual)
        kparams.addIntIfDefined("startTimeLessThanOrEqual", self.startTimeLessThanOrEqual)
        kparams.addStringIfDefined("userIdEqual", self.userIdEqual)
        kparams.addStringIfDefined("userIdIn", self.userIdIn)
        kparams.addIntIfDefined("partnerSortValueEqual", self.partnerSortValueEqual)
        kparams.addStringIfDefined("partnerSortValueIn", self.partnerSortValueIn)
        kparams.addIntIfDefined("partnerSortValueGreaterThanOrEqual", self.partnerSortValueGreaterThanOrEqual)
        kparams.addIntIfDefined("partnerSortValueLessThanOrEqual", self.partnerSortValueLessThanOrEqual)
        kparams.addIntEnumIfDefined("forceStopEqual", self.forceStopEqual)
        kparams.addStringIfDefined("systemNameEqual", self.systemNameEqual)
        kparams.addStringIfDefined("systemNameIn", self.systemNameIn)
        return kparams

    def getIdEqual(self):
        return self.idEqual

    def setIdEqual(self, newIdEqual):
        self.idEqual = newIdEqual

    def getIdIn(self):
        return self.idIn

    def setIdIn(self, newIdIn):
        self.idIn = newIdIn

    def getCuePointTypeEqual(self):
        return self.cuePointTypeEqual

    def setCuePointTypeEqual(self, newCuePointTypeEqual):
        self.cuePointTypeEqual = newCuePointTypeEqual

    def getCuePointTypeIn(self):
        return self.cuePointTypeIn

    def setCuePointTypeIn(self, newCuePointTypeIn):
        self.cuePointTypeIn = newCuePointTypeIn

    def getStatusEqual(self):
        return self.statusEqual

    def setStatusEqual(self, newStatusEqual):
        self.statusEqual = newStatusEqual

    def getStatusIn(self):
        return self.statusIn

    def setStatusIn(self, newStatusIn):
        self.statusIn = newStatusIn

    def getEntryIdEqual(self):
        return self.entryIdEqual

    def setEntryIdEqual(self, newEntryIdEqual):
        self.entryIdEqual = newEntryIdEqual

    def getEntryIdIn(self):
        return self.entryIdIn

    def setEntryIdIn(self, newEntryIdIn):
        self.entryIdIn = newEntryIdIn

    def getCreatedAtGreaterThanOrEqual(self):
        return self.createdAtGreaterThanOrEqual

    def setCreatedAtGreaterThanOrEqual(self, newCreatedAtGreaterThanOrEqual):
        self.createdAtGreaterThanOrEqual = newCreatedAtGreaterThanOrEqual

    def getCreatedAtLessThanOrEqual(self):
        return self.createdAtLessThanOrEqual

    def setCreatedAtLessThanOrEqual(self, newCreatedAtLessThanOrEqual):
        self.createdAtLessThanOrEqual = newCreatedAtLessThanOrEqual

    def getUpdatedAtGreaterThanOrEqual(self):
        return self.updatedAtGreaterThanOrEqual

    def setUpdatedAtGreaterThanOrEqual(self, newUpdatedAtGreaterThanOrEqual):
        self.updatedAtGreaterThanOrEqual = newUpdatedAtGreaterThanOrEqual

    def getUpdatedAtLessThanOrEqual(self):
        return self.updatedAtLessThanOrEqual

    def setUpdatedAtLessThanOrEqual(self, newUpdatedAtLessThanOrEqual):
        self.updatedAtLessThanOrEqual = newUpdatedAtLessThanOrEqual

    def getTagsLike(self):
        return self.tagsLike

    def setTagsLike(self, newTagsLike):
        self.tagsLike = newTagsLike

    def getTagsMultiLikeOr(self):
        return self.tagsMultiLikeOr

    def setTagsMultiLikeOr(self, newTagsMultiLikeOr):
        self.tagsMultiLikeOr = newTagsMultiLikeOr

    def getTagsMultiLikeAnd(self):
        return self.tagsMultiLikeAnd

    def setTagsMultiLikeAnd(self, newTagsMultiLikeAnd):
        self.tagsMultiLikeAnd = newTagsMultiLikeAnd

    def getStartTimeGreaterThanOrEqual(self):
        return self.startTimeGreaterThanOrEqual

    def setStartTimeGreaterThanOrEqual(self, newStartTimeGreaterThanOrEqual):
        self.startTimeGreaterThanOrEqual = newStartTimeGreaterThanOrEqual

    def getStartTimeLessThanOrEqual(self):
        return self.startTimeLessThanOrEqual

    def setStartTimeLessThanOrEqual(self, newStartTimeLessThanOrEqual):
        self.startTimeLessThanOrEqual = newStartTimeLessThanOrEqual

    def getUserIdEqual(self):
        return self.userIdEqual

    def setUserIdEqual(self, newUserIdEqual):
        self.userIdEqual = newUserIdEqual

    def getUserIdIn(self):
        return self.userIdIn

    def setUserIdIn(self, newUserIdIn):
        self.userIdIn = newUserIdIn

    def getPartnerSortValueEqual(self):
        return self.partnerSortValueEqual

    def setPartnerSortValueEqual(self, newPartnerSortValueEqual):
        self.partnerSortValueEqual = newPartnerSortValueEqual

    def getPartnerSortValueIn(self):
        return self.partnerSortValueIn

    def setPartnerSortValueIn(self, newPartnerSortValueIn):
        self.partnerSortValueIn = newPartnerSortValueIn

    def getPartnerSortValueGreaterThanOrEqual(self):
        return self.partnerSortValueGreaterThanOrEqual

    def setPartnerSortValueGreaterThanOrEqual(self, newPartnerSortValueGreaterThanOrEqual):
        self.partnerSortValueGreaterThanOrEqual = newPartnerSortValueGreaterThanOrEqual

    def getPartnerSortValueLessThanOrEqual(self):
        return self.partnerSortValueLessThanOrEqual

    def setPartnerSortValueLessThanOrEqual(self, newPartnerSortValueLessThanOrEqual):
        self.partnerSortValueLessThanOrEqual = newPartnerSortValueLessThanOrEqual

    def getForceStopEqual(self):
        return self.forceStopEqual

    def setForceStopEqual(self, newForceStopEqual):
        self.forceStopEqual = newForceStopEqual

    def getSystemNameEqual(self):
        return self.systemNameEqual

    def setSystemNameEqual(self, newSystemNameEqual):
        self.systemNameEqual = newSystemNameEqual

    def getSystemNameIn(self):
        return self.systemNameIn

    def setSystemNameIn(self, newSystemNameIn):
        self.systemNameIn = newSystemNameIn


# @package External
# @subpackage Kaltura
class KalturaCuePointFilter(KalturaCuePointBaseFilter):
    def __init__(self,
            orderBy=NotImplemented,
            advancedSearch=NotImplemented,
            idEqual=NotImplemented,
            idIn=NotImplemented,
            cuePointTypeEqual=NotImplemented,
            cuePointTypeIn=NotImplemented,
            statusEqual=NotImplemented,
            statusIn=NotImplemented,
            entryIdEqual=NotImplemented,
            entryIdIn=NotImplemented,
            createdAtGreaterThanOrEqual=NotImplemented,
            createdAtLessThanOrEqual=NotImplemented,
            updatedAtGreaterThanOrEqual=NotImplemented,
            updatedAtLessThanOrEqual=NotImplemented,
            tagsLike=NotImplemented,
            tagsMultiLikeOr=NotImplemented,
            tagsMultiLikeAnd=NotImplemented,
            startTimeGreaterThanOrEqual=NotImplemented,
            startTimeLessThanOrEqual=NotImplemented,
            userIdEqual=NotImplemented,
            userIdIn=NotImplemented,
            partnerSortValueEqual=NotImplemented,
            partnerSortValueIn=NotImplemented,
            partnerSortValueGreaterThanOrEqual=NotImplemented,
            partnerSortValueLessThanOrEqual=NotImplemented,
            forceStopEqual=NotImplemented,
            systemNameEqual=NotImplemented,
            systemNameIn=NotImplemented):
        KalturaCuePointBaseFilter.__init__(self,
            orderBy,
            advancedSearch,
            idEqual,
            idIn,
            cuePointTypeEqual,
            cuePointTypeIn,
            statusEqual,
            statusIn,
            entryIdEqual,
            entryIdIn,
            createdAtGreaterThanOrEqual,
            createdAtLessThanOrEqual,
            updatedAtGreaterThanOrEqual,
            updatedAtLessThanOrEqual,
            tagsLike,
            tagsMultiLikeOr,
            tagsMultiLikeAnd,
            startTimeGreaterThanOrEqual,
            startTimeLessThanOrEqual,
            userIdEqual,
            userIdIn,
            partnerSortValueEqual,
            partnerSortValueIn,
            partnerSortValueGreaterThanOrEqual,
            partnerSortValueLessThanOrEqual,
            forceStopEqual,
            systemNameEqual,
            systemNameIn)


    PROPERTY_LOADERS = {
    }

    def fromXml(self, node):
        KalturaCuePointBaseFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaCuePointFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaCuePointBaseFilter.toParams(self)
        kparams.put("objectType", "KalturaCuePointFilter")
        return kparams


########## services ##########

# @package External
# @subpackage Kaltura
class KalturaCuePointService(KalturaServiceBase):
    """Cue Point service"""

    def __init__(self, client = None):
        KalturaServiceBase.__init__(self, client)

    def add(self, cuePoint):
        """Allows you to add an cue point object associated with an entry"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("cuePoint", cuePoint)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "add", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePoint)

    def addFromBulk(self, fileData):
        """Allows you to add multiple cue points objects by uploading XML that contains multiple cue point definitions"""

        kparams = KalturaParams()
        kfiles = KalturaFiles()
        kfiles.put("fileData", fileData);
        self.client.queueServiceActionCall("cuepoint_cuepoint", "addFromBulk", kparams, kfiles)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePointListResponse)

    def serveBulk(self, filter = NotImplemented, pager = NotImplemented):
        """Download multiple cue points objects as XML definitions"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall('cuepoint_cuepoint', 'serveBulk', kparams)
        return self.client.getServeUrl()

    def get(self, id):
        """Retrieve an CuePoint object by id"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "get", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePoint)

    def list(self, filter = NotImplemented, pager = NotImplemented):
        """List cue point objects by filter and pager"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "list", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePointListResponse)

    def count(self, filter = NotImplemented):
        """count cue point objects by filter"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "count", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return getXmlNodeInt(resultNode)

    def update(self, id, cuePoint):
        """Update cue point by id"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        kparams.addObjectIfDefined("cuePoint", cuePoint)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "update", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePoint)

    def delete(self, id):
        """delete cue point by id, and delete all children cue points"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        self.client.queueServiceActionCall("cuepoint_cuepoint", "delete", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()

########## main ##########
class KalturaCuePointClientPlugin(KalturaClientPlugin):
    # KalturaCuePointClientPlugin
    instance = None

    # @return KalturaCuePointClientPlugin
    @staticmethod
    def get():
        if KalturaCuePointClientPlugin.instance == None:
            KalturaCuePointClientPlugin.instance = KalturaCuePointClientPlugin()
        return KalturaCuePointClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
            'cuePoint': KalturaCuePointService,
        }

    def getEnums(self):
        return {
            'KalturaCuePointStatus': KalturaCuePointStatus,
            'KalturaCuePointOrderBy': KalturaCuePointOrderBy,
            'KalturaCuePointType': KalturaCuePointType,
        }

    def getTypes(self):
        return {
            'KalturaCuePoint': KalturaCuePoint,
            'KalturaCuePointListResponse': KalturaCuePointListResponse,
            'KalturaCuePointBaseFilter': KalturaCuePointBaseFilter,
            'KalturaCuePointFilter': KalturaCuePointFilter,
        }

    # @return string
    def getName(self):
        return 'cuePoint'

