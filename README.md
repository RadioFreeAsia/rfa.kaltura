Products.Kaltura
================
but call it rfa.kaltura right now (company name).(package name)

This is so alpha, but it's working.


Kaltura Video Integration with Plone
----

Just barely functional, but it works.

Here are some installation 'suggestions' because I haven't run through a full installation test:

Buildout:
--
You're probably going to want to do something like this:

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
rfa.kaltura = git https://github.com/flipmcf/Products.Kaltura.git


</code></pre>

and run ./bin/buildout


From Source
--
git clone this repository into the src/ directory in your plone instance.<br>
run setup.py<br>



Once it's built into zope
--
Restart your zope instance<br>
you _should_ see 'rfa.kaltura' as an available product to install<br>
Install it.<br>


Once it's installed
--
As the portal manager, visit the site config and configure the add-on. 
*Add your Kaltura API credentials


To test, navigate to somewhere in plone, and "Create->Kaltura Video"<br>
upload a test video to plone like any other file object (there is one in the kalturaapi/TestCode directory)<br>
hit 'save'<br>
note the url (that's from kaltura)<br>
go login to your kaltura console and note the file is there too.<br>

when you request that object with the default view (or '/video_view') 
you should get the default template that will play the video in an iframe.


---Document Skin layers---

---Document Macros---


---

Fork this repository and help!!!!


--------
Contact: flip@rfa.org
Website: http://www.rfa.org/

Feel free to contact me.
