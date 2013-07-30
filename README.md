Kaltura Python Native Client Library

Master is at API_VERSION = '3.1.6'  (June 30 2013)

I (or anyone please!) will keep master updated with Kaltura's latest releases.

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
 - Edit your Partner ID, Service Secret, Admin Secret and User Name in 'TestCode/PythonTester.py'
 - Run "python PythonTester.py"

Note: The library was tested under ActivePython 2.5.5
