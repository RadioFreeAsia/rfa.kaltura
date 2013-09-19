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
########## classes ##########
########## services ##########

# @package External
# @subpackage Kaltura
class KalturaBulkService(KalturaServiceBase):
    """Bulk upload service is used to upload & manage bulk uploads using CSV files"""

    def __init__(self, client = None):
        KalturaServiceBase.__init__(self, client)

    def get(self, id):
        """Get bulk upload batch job by id"""

        kparams = KalturaParams()
        kparams.addIntIfDefined("id", id);
        self.client.queueServiceActionCall("bulkupload_bulk", "get", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaBulkUpload)

    def list(self, bulkUploadFilter = NotImplemented, pager = NotImplemented):
        """List bulk upload batch jobs"""

        kparams = KalturaParams()
        kparams.addObjectIfDefined("bulkUploadFilter", bulkUploadFilter)
        kparams.addObjectIfDefined("pager", pager)
        self.client.queueServiceActionCall("bulkupload_bulk", "list", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaBulkUploadListResponse)

    def serve(self, id):
        """serve action returns the original file."""

        kparams = KalturaParams()
        kparams.addIntIfDefined("id", id);
        self.client.queueServiceActionCall('bulkupload_bulk', 'serve', kparams)
        return self.client.getServeUrl()

    def serveLog(self, id):
        """serveLog action returns the log file for the bulk-upload job."""

        kparams = KalturaParams()
        kparams.addIntIfDefined("id", id);
        self.client.queueServiceActionCall('bulkupload_bulk', 'serveLog', kparams)
        return self.client.getServeUrl()

    def abort(self, id):
        """Aborts the bulk upload and all its child jobs"""

        kparams = KalturaParams()
        kparams.addIntIfDefined("id", id);
        self.client.queueServiceActionCall("bulkupload_bulk", "abort", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return KalturaObjectFactory.create(resultNode, KalturaBulkUpload)

########## main ##########
class KalturaBulkUploadClientPlugin(KalturaClientPlugin):
    # KalturaBulkUploadClientPlugin
    instance = None

    # @return KalturaBulkUploadClientPlugin
    @staticmethod
    def get():
        if KalturaBulkUploadClientPlugin.instance == None:
            KalturaBulkUploadClientPlugin.instance = KalturaBulkUploadClientPlugin()
        return KalturaBulkUploadClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
            'bulk': KalturaBulkService,
        }

    def getEnums(self):
        return {
        }

    def getTypes(self):
        return {
        }

    # @return string
    def getName(self):
        return 'bulkUpload'

