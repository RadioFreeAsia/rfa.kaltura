import fixpypath
from utils import GetConfig
from utils import KalturaBaseTest

class MediaTests(KalturaBaseTest):
    pass


import unittest
def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(MediaTests),
        ))

if __name__ == "__main__":
    suite = test_suite()
    unittest.TextTestRunner(verbosity=2).run(suite)