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
########## classes ##########
########## services ##########

# @package External
# @subpackage Kaltura
class KalturaAsperaService(KalturaServiceBase):
    """Aspera service"""

    def __init__(self, client = None):
        KalturaServiceBase.__init__(self, client)

    def getFaspUrl(self, flavorAssetId):
        kparams = KalturaParams()
        kparams.addStringIfDefined("flavorAssetId", flavorAssetId)
        self.client.queueServiceActionCall("aspera_aspera", "getFaspUrl", kparams)
        if self.client.isMultiRequest():
            return self.client.getMultiRequestResult()
        resultNode = self.client.doQueue()
        return getXmlNodeText(resultNode)

########## main ##########
class KalturaAsperaClientPlugin(KalturaClientPlugin):
    # KalturaAsperaClientPlugin
    instance = None

    # @return KalturaAsperaClientPlugin
    @staticmethod
    def get():
        if KalturaAsperaClientPlugin.instance == None:
            KalturaAsperaClientPlugin.instance = KalturaAsperaClientPlugin()
        return KalturaAsperaClientPlugin.instance

    # @return array<KalturaServiceBase>
    def getServices(self):
        return {
            'aspera': KalturaAsperaService,
        }

    def getEnums(self):
        return {
        }

    def getTypes(self):
        return {
        }

    # @return string
    def getName(self):
        return 'aspera'

