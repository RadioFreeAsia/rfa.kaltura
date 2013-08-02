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
from KalturaCuePointClientPlugin import *
from KalturaClientBase import *

########## enums ##########
# @package External
# @subpackage Kaltura
class KalturaAnnotationOrderBy:
    CREATED_AT_ASC = "+createdAt"
    DURATION_ASC = "+duration"
    END_TIME_ASC = "+endTime"
    PARTNER_SORT_VALUE_ASC = "+partnerSortValue"
    START_TIME_ASC = "+startTime"
    UPDATED_AT_ASC = "+updatedAt"
    CREATED_AT_DESC = "-createdAt"
    DURATION_DESC = "-duration"
    END_TIME_DESC = "-endTime"
    PARTNER_SORT_VALUE_DESC = "-partnerSortValue"
    START_TIME_DESC = "-startTime"
    UPDATED_AT_DESC = "-updatedAt"

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

########## classes ##########
# @package External
# @subpackage Kaltura
class KalturaAnnotation(KalturaCuePoint):
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
            systemName=NotImplemented,
            parentId=NotImplemented,
            text=NotImplemented,
            endTime=NotImplemented,
            duration=NotImplemented,
            depth=NotImplemented,
            childrenCount=NotImplemented,
            directChildrenCount=NotImplemented):
        KalturaCuePoint.__init__(self,
            id,
            cuePointType,
            status,
            entryId,
            partnerId,
            createdAt,
            updatedAt,
            tags,
            startTime,
            userId,
            partnerData,
            partnerSortValue,
            forceStop,
            thumbOffset,
            systemName)

        # @var string
        # @insertonly
        self.parentId = parentId

        # @var string
        self.text = text

        # End time in milliseconds
        # @var int
        self.endTime = endTime

        # Duration in milliseconds
        # @var int
        # @readonly
        self.duration = duration

        # Depth in the tree
        # @var int
        # @readonly
        self.depth = depth

        # Number of all descendants
        # @var int
        # @readonly
        self.childrenCount = childrenCount

        # Number of children, first generation only.
        # @var int
        # @readonly
        self.directChildrenCount = directChildrenCount


    PROPERTY_LOADERS = {
        'parentId': getXmlNodeText, 
        'text': getXmlNodeText, 
        'endTime': getXmlNodeInt, 
        'duration': getXmlNodeInt, 
        'depth': getXmlNodeInt, 
        'childrenCount': getXmlNodeInt, 
        'directChildrenCount': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaCuePoint.fromXml(self, node)
        self.fromXmlImpl(node, KalturaAnnotation.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaCuePoint.toParams(self)
        kparams.put("objectType", "KalturaAnnotation")
        kparams.addStringIfDefined("parentId", self.parentId)
        kparams.addStringIfDefined("text", self.text)
        kparams.addIntIfDefined("endTime", self.endTime)
        return kparams

    def getParentId(self):
        return self.parentId

    def setParentId(self, newParentId):
        self.parentId = newParentId

    def getText(self):
        return self.text

    def setText(self, newText):
        self.text = newText

    def getEndTime(self):
        return self.endTime

    def setEndTime(self, newEndTime):
        self.endTime = newEndTime

    def getDuration(self):
        return self.duration

    def getDepth(self):
        return self.depth

    def getChildrenCount(self):
        return self.childrenCount

    def getDirectChildrenCount(self):
        return self.directChildrenCount


# @package External
# @subpackage Kaltura
class KalturaAnnotationListResponse(KalturaObjectBase):
    def __init__(self,
            objects=NotImplemented,
            totalCount=NotImplemented):
        KalturaObjectBase.__init__(self)

        # @var array of KalturaAnnotation
        # @readonly
        self.objects = objects

        # @var int
        # @readonly
        self.totalCount = totalCount


    PROPERTY_LOADERS = {
        'objects': (KalturaObjectFactory.createArray, KalturaAnnotation), 
        'totalCount': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaObjectBase.fromXml(self, node)
        self.fromXmlImpl(node, KalturaAnnotationListResponse.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaObjectBase.toParams(self)
        kparams.put("objectType", "KalturaAnnotationListResponse")
        return kparams

    def getObjects(self):
        return self.objects

    def getTotalCount(self):
        return self.totalCount


# @package External
# @subpackage Kaltura
class KalturaAnnotationBaseFilter(KalturaCuePointFilter):
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
            systemNameIn=NotImplemented,
            parentIdEqual=NotImplemented,
            parentIdIn=NotImplemented,
            textLike=NotImplemented,
            textMultiLikeOr=NotImplemented,
            textMultiLikeAnd=NotImplemented,
            endTimeGreaterThanOrEqual=NotImplemented,
            endTimeLessThanOrEqual=NotImplemented,
            durationGreaterThanOrEqual=NotImplemented,
            durationLessThanOrEqual=NotImplemented):
        KalturaCuePointFilter.__init__(self,
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

        # @var string
        self.parentIdEqual = parentIdEqual

        # @var string
        self.parentIdIn = parentIdIn

        # @var string
        self.textLike = textLike

        # @var string
        self.textMultiLikeOr = textMultiLikeOr

        # @var string
        self.textMultiLikeAnd = textMultiLikeAnd

        # @var int
        self.endTimeGreaterThanOrEqual = endTimeGreaterThanOrEqual

        # @var int
        self.endTimeLessThanOrEqual = endTimeLessThanOrEqual

        # @var int
        self.durationGreaterThanOrEqual = durationGreaterThanOrEqual

        # @var int
        self.durationLessThanOrEqual = durationLessThanOrEqual


    PROPERTY_LOADERS = {
        'parentIdEqual': getXmlNodeText, 
        'parentIdIn': getXmlNodeText, 
        'textLike': getXmlNodeText, 
        'textMultiLikeOr': getXmlNodeText, 
        'textMultiLikeAnd': getXmlNodeText, 
        'endTimeGreaterThanOrEqual': getXmlNodeInt, 
        'endTimeLessThanOrEqual': getXmlNodeInt, 
        'durationGreaterThanOrEqual': getXmlNodeInt, 
        'durationLessThanOrEqual': getXmlNodeInt, 
    }

    def fromXml(self, node):
        KalturaCuePointFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaAnnotationBaseFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaCuePointFilter.toParams(self)
        kparams.put("objectType", "KalturaAnnotationBaseFilter")
        kparams.addStringIfDefined("parentIdEqual", self.parentIdEqual)
        kparams.addStringIfDefined("parentIdIn", self.parentIdIn)
        kparams.addStringIfDefined("textLike", self.textLike)
        kparams.addStringIfDefined("textMultiLikeOr", self.textMultiLikeOr)
        kparams.addStringIfDefined("textMultiLikeAnd", self.textMultiLikeAnd)
        kparams.addIntIfDefined("endTimeGreaterThanOrEqual", self.endTimeGreaterThanOrEqual)
        kparams.addIntIfDefined("endTimeLessThanOrEqual", self.endTimeLessThanOrEqual)
        kparams.addIntIfDefined("durationGreaterThanOrEqual", self.durationGreaterThanOrEqual)
        kparams.addIntIfDefined("durationLessThanOrEqual", self.durationLessThanOrEqual)
        return kparams

    def getParentIdEqual(self):
        return self.parentIdEqual

    def setParentIdEqual(self, newParentIdEqual):
        self.parentIdEqual = newParentIdEqual

    def getParentIdIn(self):
        return self.parentIdIn

    def setParentIdIn(self, newParentIdIn):
        self.parentIdIn = newParentIdIn

    def getTextLike(self):
        return self.textLike

    def setTextLike(self, newTextLike):
        self.textLike = newTextLike

    def getTextMultiLikeOr(self):
        return self.textMultiLikeOr

    def setTextMultiLikeOr(self, newTextMultiLikeOr):
        self.textMultiLikeOr = newTextMultiLikeOr

    def getTextMultiLikeAnd(self):
        return self.textMultiLikeAnd

    def setTextMultiLikeAnd(self, newTextMultiLikeAnd):
        self.textMultiLikeAnd = newTextMultiLikeAnd

    def getEndTimeGreaterThanOrEqual(self):
        return self.endTimeGreaterThanOrEqual

    def setEndTimeGreaterThanOrEqual(self, newEndTimeGreaterThanOrEqual):
        self.endTimeGreaterThanOrEqual = newEndTimeGreaterThanOrEqual

    def getEndTimeLessThanOrEqual(self):
        return self.endTimeLessThanOrEqual

    def setEndTimeLessThanOrEqual(self, newEndTimeLessThanOrEqual):
        self.endTimeLessThanOrEqual = newEndTimeLessThanOrEqual

    def getDurationGreaterThanOrEqual(self):
        return self.durationGreaterThanOrEqual

    def setDurationGreaterThanOrEqual(self, newDurationGreaterThanOrEqual):
        self.durationGreaterThanOrEqual = newDurationGreaterThanOrEqual

    def getDurationLessThanOrEqual(self):
        return self.durationLessThanOrEqual

    def setDurationLessThanOrEqual(self, newDurationLessThanOrEqual):
        self.durationLessThanOrEqual = newDurationLessThanOrEqual


# @package External
# @subpackage Kaltura
class KalturaAnnotationFilter(KalturaAnnotationBaseFilter):
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
            systemNameIn=NotImplemented,
            parentIdEqual=NotImplemented,
            parentIdIn=NotImplemented,
            textLike=NotImplemented,
            textMultiLikeOr=NotImplemented,
            textMultiLikeAnd=NotImplemented,
            endTimeGreaterThanOrEqual=NotImplemented,
            endTimeLessThanOrEqual=NotImplemented,
            durationGreaterThanOrEqual=NotImplemented,
            durationLessThanOrEqual=NotImplemented):
        KalturaAnnotationBaseFilter.__init__(self,
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
            systemNameIn,
            parentIdEqual,
            parentIdIn,
            textLike,
            textMultiLikeOr,
            textMultiLikeAnd,
            endTimeGreaterThanOrEqual,
            endTimeLessThanOrEqual,
            durationGreaterThanOrEqual,
            durationLessThanOrEqual)


    PROPERTY_LOADERS = {
    }

    def fromXml(self, node):
        KalturaAnnotationBaseFilter.fromXml(self, node)
        self.fromXmlImpl(node, KalturaAnnotationFilter.PROPERTY_LOADERS)

    def toParams(self):
        kparams = KalturaAnnotationBaseFilter.toParams(self)
        kparams.put("objectType", "KalturaAnnotationFilter")
        return kparams


########## services ##########

# @package External
# @subpackage Kaltura
class KalturaAnnotationService(KalturaServiceBase):
    """Annotation service - Video Annotation"""

    def __init__(self, client = None):
        KalturaServiceBase.__init__(self, client)

    def add(self, annotation):
        """Allows you to add an annotation object associated with an entry"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("annotation", annotation)
        self.client.queueServiceActionCall("annotation_annotation", "add", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaAnnotation)

    def update(self, id, annotation):
        """Update annotation by id"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        kparams.addObjectIfDefined("annotation", annotation)
        self.client.queueServiceActionCall("annotation_annotation", "update", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaAnnotation)

    def list(self, filter = NotImplemented, pager = NotImplemented):
        """List annotation objects by filter and pager"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall("annotation_annotation", "list", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaAnnotationListResponse)

    def addFromBulk(self, fileData):
        """Allows you to add multiple cue points objects by uploading XML that contains multiple cue point definitions"""

        kparams = KalturaParams()
        kfiles = KalturaFiles()
        kfiles.put("fileData", fileData);
        self.client.queueServiceActionCall("annotation_annotation", "addFromBulk", kparams, kfiles)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePointListResponse)

    def serveBulk(self, filter = NotImplemented, pager = NotImplemented):
        """Download multiple cue points objects as XML definitions"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall('annotation_annotation', 'serveBulk', kparams)
        return self.client.getServeUrl()

    def get(self, id):
        """Retrieve an CuePoint object by id"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        self.client.queueServiceActionCall("annotation_annotation", "get", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaCuePoint)

    def count(self, filter = NotImplemented):
        """count cue point objects by filter"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("filter", filter)
        self.client.queueServiceActionCall("annotation_annotation", "count", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return getXmlNodeInt(resultNode)

    def delete(self, id):
        """delete cue point by id, and delete all children cue points"""

        kparams = KalturaParams()
        kparams.addStringIfDefined("id", id)
        self.client.queueServiceActionCall("annotation_annotation", "delete", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()

########## main ##########
class KalturaAnnotationClientPlugin(KalturaClientPlugin):
    # KalturaAnnotationClientPlugin
    instance = None

    # @return KalturaAnnotationClientPlugin
    @staticmethod
    def get():
        if KalturaAnnotationClientPlugin.instance == None:
            KalturaAnnotationClientPlugin.instance = KalturaAnnotationClientPlugin()
        return KalturaAnnotationClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
            'annotation': KalturaAnnotationService,
        }

    def getEnums(self):
        return {
            'KalturaAnnotationOrderBy': KalturaAnnotationOrderBy,
        }

    def getTypes(self):
        return {
            'KalturaAnnotation': KalturaAnnotation,
            'KalturaAnnotationListResponse': KalturaAnnotationListResponse,
            'KalturaAnnotationBaseFilter': KalturaAnnotationBaseFilter,
            'KalturaAnnotationFilter': KalturaAnnotationFilter,
        }

    # @return string
    def getName(self):
        return 'annotation'

