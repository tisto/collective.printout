import doctest
import unittest2 as unittest
import pprint
import interlude

from plone.testing import layered

from collective.printout.testing import \
    COLLECTIVE_PRINTOUT_FUNCTIONAL_TESTING

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
normal_testfiles = [
    '../README.txt',
]

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(test ,
                                     optionflags=optionflags,
                                     globs={'interact': interlude.interact,
                                            'pprint': pprint.pprint,
                                            }
                                     ),
                layer=COLLECTIVE_PRINTOUT_FUNCTIONAL_TESTING)
        for test in normal_testfiles])
    return suite
