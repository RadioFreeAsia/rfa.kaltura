This is an attempt at some cleanup of Kaltura's Python API
For my own use (and hopefully others)

API_VERSION = '3.1.6'  (Aug 20 2013)

Changes from 3.1.6:

Plugin Interface (IKalturaClientPlugin) re-implemented with abc and moved to new interfaces.py
Removed all changes to sys.path on imports
Tightened up side-effect imports when importing other modules

TestCode/PythonTester.py updated to use stricter imports (gives better examples now of where stuff is)

Imports of symbols created by plugins now are accessable through an awkward, but more strict syntax:

    from KalturaClientBase import KalturaObjectFactory, KalturaEnumsFactory
  
    client = KalturaClient() #must instantiate client to populate Factories
  
    KalturaMetadataProfile = KalturaObjectFactory.objectFactories['KalturaMetadataProfile']
    KalturaMetadataObjectType = KalturaEnumsFactory.enumFactories['KalturaMetadataObjectType']

  
  (see PythonTester.py)
  

I will keep master updated with Kaltura's latest releases at http://www.kaltura.com/api_v3/testme/client-libs.php

Docs:

http://www.kaltura.com/api_v3/testmeDoc/index.php

ToDo:
 -  come up with a better way of importing plugins than above
 -  separate Factory loading from client instantiation - maybe do on import of KalturaClientBase?


Twitter:
follow @Kaltura_API for updates

IRC:
I am trying to make a habit of hanging out in #kaltura on freenode

This source contains:
 - The Kaltura client library (KalturaClient.py & KalturaClientBase.py)
 - Auto generated core APIs (KalturaCoreClient.py)
 - Auto generated plugin APIs (KalturaPlugins/*.py)
 - Python library test code and data files (TestCode/*)
 - The 'poster' python module (used by KalturaClient.py)

== DEPENDENCIES ==

The API library depends on the following builtin python libraries:
 - email.header
 - hashlib
 - httplib
 - mimetypes
 - socket
 - time
 - urllib
 - urllib2
 - uuid or random & sha
 - xml.dom
 - xml.parsers.expat
 
== TESTING THE CLIENT LIBRARY ==

to set up your credentials, copy `tests/secret_config_example.py` to `tests/secret_config.py`  and edit with your credentials.  All test files use this.

you may want to make sure that tests/.gitignore has secret_config.py in there, so you don't accidentally check in your credentials.

To run the entire test suite: 
  cd to the parent directory (Don't enter the KalturaClient package)
  `python -m unittest discover`
 
To run the original test script that accompanies this source:
 - Run `python KalturaClient/tests/PythonTester.py`

Note: 
 - The library was originally tested under ActivePython 2.5.5
 - The library is currently tested with Python 2.7.3 (default, Apr 10 2013, 06:20:15) [GCC 4.6.3] on linux2

