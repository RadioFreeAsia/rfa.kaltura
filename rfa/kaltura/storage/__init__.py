"""
Alternative Storage Methods for Video files uploaded to Plone

By default, Plone will store any videos added as content types to the ZODB as blob files.
Here, we define alternative IStorage providers to allow videos to be saved to other locations,
or not saved to plone at all.

All files are uploaded to Kaltura, regardless of the local storage method used.
"""

from storage import KalturaStorage
