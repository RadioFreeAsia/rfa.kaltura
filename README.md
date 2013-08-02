This is an attempt at some cleanup of Kaltura's Python API
For my own use (and hopefully others)

Master is at API_VERSION = '3.1.6'  (June 30 2013)

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
  
TODO: come up with a better way of importing plugins than above
TODO: separate Factory loading from client instantiation - maybe do on import of KalturaClientBase?

I will keep master updated with Kaltura's latest releases.

http://www.kaltura.com/api_v3/testme/client-libs.php

Docs:

http://www.kaltura.com/api_v3/testmeDoc/index.php

Twitter:
follow @Kaltura_API for updates

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
 - os
 - re
 - socket
 - sys
 - time
 - urllib
 - urllib2
 - uuid or random & sha
 - xml.dom
 - xml.parsers.expat
 
== TESTING THE CLIENT LIBRARY ==
  
To run the test script that accompanies this source:
 - Copy TestCode/PythonTester.py to TestCode/PythonTester-secret.py
 - Edit your Partner ID, Service Secret, Admin Secret and User Name in 'TestCode/PythonTester-secret.py'
 - Run "python PythonTester-secret.py"

Note: The library was tested under ActivePython 2.5.5
