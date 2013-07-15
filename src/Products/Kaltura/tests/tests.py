import unittest
from zope.testing import doctest


def test_suite():
    return unittest.TestSuite((
           doctest.DocFileSuite('kvideo.txt',
                                package='Products.Kaltura',
                                optionflags=doctest.ELLIPSIS),
            ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')
