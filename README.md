rfa.kaltura
================

**DEPRICATON WARNING:** 

Due to heavy ATContentTypes (archetypes) dependencies in this package, it will be re-written using Dexterity Content Types for Python3 compatability.
For this, a new project has been created for the extensive rewrite: https://github.com/RadioFreeAsia/rfa.kaltura2

Use this package only for Archetypes based installs and only if rfa.kaltura2 does not satisfy your needs.
In which case, please open a bug against rfa.kaltura2 describing the functionality gaps.

-------

Kaltura Video Integration with Plone
Version 0.9 - Functional Beta

CONTRIBUTORS:  PLEASE READ THE DEVELOPMENT SECTION BELOW!

=======
Create Videos in Plone, automatically uploaded to your Kaltura account.
Create Playlists in Plone automatically synced with your Kaltura account.

Customize your Kaltura view templates in skins

Add Kaltura Videos to a composite page layout.


Installation:
----

VIA BUILDOUT:<br/>

edit your buildout.cfg to include this git repository as a source with auto-checkout using mr.developer.<br/>
And add it to your list of eggs to install.

<pre><code>
[buildout]
...
extensions = mr.developer

auto-checkout = 
...
   rfa.kaltura
eggs =
...
   rfa.kaltura

[sources]
...
rfa.kaltura = git https://github.com/RadioFreeAsia/rfa.kaltura.git


</code></pre>

Run ./bin/buildout


FROM SOURCE

git clone this repository into the src/ directory in your plone instance.<br>
run setup.py<br>

Remember to edit the sys.path line in bin/instance to include the path to the rfa.kaltura source.


Once it's built into zope
--
Restart your zope instance<br>
you _should_ see 'rfa.kaltura' as an available product to install<br>
Install it.<br>


Once it's installed
--
As the portal manager, visit the site config and configure the add-on. 


To retrieve the Credentials for filling out the add-on configuration:

Service URL: Set this as the same url you use to login to the Kaltura Management Console<br>
Username: the username you use to login to the Kaltura Management Console<br>

Partner ID, Admin Secret, User Secret:

1: Login to kaltura management console.<br>
2: Go to Settings->Integration Settings<br>
3: Retrieve Partner ID, UserSecret and Admin secret from here.<br>


To test, navigate to somewhere in plone, and "Create->Kaltura Video"<br>
upload a test video to plone like any other file object (there is one in the kalturaapi/TestCode directory)<br>
hit 'save'<br>
note the url (that's from kaltura)<br>
go login to your kaltura console and note the file is there too.<br>

when you request that object with the default view (or '/video_view') 
you should get the default template that will play the video in an iframe.


---Document Skin layers---

---Document Macros---


Development
---

Note that this repository contains a subtree of another git repository: the Kaltura API

This repository uses the subtree-merge method to manage external repositories see https://help.github.com/articles/working-with-subtree-merge

In a Nutshell, follow these rules of the road:
 - 1.  Never change and commit code under the kalturaapi directory, this code is maintained as a subtree.
 - - if you wish to change code in the api, see https://github.com/flipmcf/Kaltura_API_Python/
 - 2.  The 'best working state' will always be what's in rfa.kaltura - even if the kalturaapi directory is behind a few revisions.  Trust THIS repository implicitly - it is in effect 'pinning' to a version of Kaltura_API_Python.
 - 3.  In the event changes from Kaltura_API_Python must be merged into Products.Kaltura follow this:
 - - checkout / pull a clean local copy of Products.Kaltura with no local changes
 - - git pull -s subtree kalturaapi master




--------
Contact: flip@rfa.org
Website: http://www.rfa.org/

Feel free to contact me.
