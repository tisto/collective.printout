# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility
from zope.component import getMultiAdapter

from zope.interface import alsoProvides

from collective.printout.testing import \
    COLLECTIVE_PRINTOUT_INTEGRATION_TESTING

from plone.app.testing import TEST_USER_ID, setRoles

from collective.printout.interfaces import IPrintable

class SetupTest(unittest.TestCase):

    layer = COLLECTIVE_PRINTOUT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Document', 'doc')
        self.doc = self.folder.doc
        
    def test_printout_view(self):
        alsoProvides(self.doc, IPrintable)
        #view = getMultiAdapter((self.doc, self.doc.REQUEST), name="printout")
        #view = view.__of__(self.doc)
        #self.assertFail(view())
        
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
