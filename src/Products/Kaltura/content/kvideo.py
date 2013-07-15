### kvideo.py: Provides handling of kalutra video objects in a Plone site
### Copyright (c) 2013 Michael McFadden [flipmcf] and Radio Free Asia 
###   
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""kvideo allows you to manage video files with Kaltura and Plone.
   The video file is stored on your Kaltura account.
   Plone will store idetification of this File on Kaltura, and any url's used to render.
"""

__author__  = 'Michael McFadden <flip@rfa.org>'
__docformat__ = 'restructuredtext'

from zope import interface
from zope import component
from Products.Kaltura import interfaces
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo
from ZODB.PersistentMapping import PersistentMapping
from Acquisition import aq_base


from Products.Archetypes.Storage import Storage

try:
    from Products.LinguaPlone.public import *
except:
    # no multilingual support
    from Products.Archetypes.public import *
    
#KVideoSchema =  ATFileSchema.copy() + Schema().copy() + Schema(( ###BASE THIS OFF OF SOMETHING RELEVANT!

KVideoSchema = Schema((
    StringField('title',
                searchable=1,
                required=False,
                languageIndependent=1,
                default_method="getVideoTitle",
                accessor="Title",
                widget=StringWidget(label="Title",
                                    label_msgid="label_kvideofile_title",
                                    description="The title of this video.",
                                    description_msgid="desc_kvideofile_title",
                                    i18n_domain="kvideo"),
                schemata="Metadata",
                ),
    
    ),
    marshall=PrimaryFieldMarshaller(),
)
   
   



class KalturaVideo(ATFile):  ###ATFile is probably not the best base
    """
    Content type to handle Videos stored and maintained on Kaltura
    """
    
    interface.implements(interfaces.IKalturaVideo)
    
    schema = KVideoSchema
    
    def getVideoURL():
        return "this would be the url where the video is"
    
    
registerType(KalturaVideo, 'KalturaVideo')   ### Need config.py