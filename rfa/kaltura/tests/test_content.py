"""content tests"""

#important tests to write
# content.kalturavideo.KalturaVideo.updateCategories
# content.kalturavideo.KalturaVideo.updateTags
import unittest

from zope.component.testing import PlacelessSetup
from Testing import ZopeTestCase



class KalturaVideoTests(PlacelessSetup, unittest.TestCase):
    
    def _getTargetClass(self):
        
        from rfa.kaltura.content.kalturavideo import KalturaVideo
        return KalturaVideo 
        

    def _makeOne(self, id='test_video', *args, **kw):
        _registerSchemaAdapter()
        return self._getTargetClass()(id, *args, **kw)
    
    def test_class_conforms_to_IKalturaVideo(self):
        from zope.interface.verify import verifyClass
        from rfa.kaltura.interfaces import IKalturaVideo
        verifyClass(IKalturaVideo, self._getTargetClass())
   
    def test_syncMetadata(self):
        ZopeTestCase.installProduct('MimetypesRegistry')
        ZopeTestCase.installProduct('mimetypes_registry')
        import rfa.kaltura.content.kalturavideo
        with _Monkey(rfa.kaltura.content.kalturavideo, kconnect=dummyConnect):
            import pdb; pdb.set_trace()
            
            #stupidly failing with exception: 	"AttributeError: mimetypes_registry"
            video = self._makeOne()
            video.setTitle('fooTitle')
            video.setDescription('fooDescription')
            video.setTags(['fooTag'])
            video.syncMetadata()
        

class DummyClient(object):
    pass

class DummySession(object):
    pass

def dummyConnect():
    """ don't connect to kaltura server"""
    return (DummyClient, DummySession)

        
class _Monkey(object):
    # context-manager for replacing module names in the scope of a test.

    def __init__(self, module, **kw):
        self.module = module
        self.to_restore = dict([(key, getattr(module, key)) for key in kw])
        for key, value in kw.items():
            setattr(module, key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key, value in self.to_restore.items():
            setattr(self.module, key, value)

def _registerSchemaAdapter():
    from zope.interface import Interface
    from zope.component import provideAdapter
    from Products.Archetypes.interfaces import ISchema
    def _adapter(context):
        return context.schema
    provideAdapter(_adapter, (Interface,), ISchema)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(KalturaVideoTests),
        ))