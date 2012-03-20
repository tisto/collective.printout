import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility
from zope.component import getMultiAdapter

from plone.registry import Registry

from collective.printout.testing import \
    COLLECTIVE_PRINTOUT_INTEGRATION_TESTING

from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.testing import logout

from collective.printout.interfaces import IPrintoutSettings


class RegistryTest(unittest.TestCase):

    layer = COLLECTIVE_PRINTOUT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
  
        self.registry = Registry()
        self.registry.registerInterface(IPrintoutSettings)
        
    #def test_printout_controlpanel_view(self):
    #    view = getMultiAdapter((self.portal, self.portal.REQUEST), 
    #                           name="printout-settings")
    #    view = view.__of__(self.portal)
    #    import ipdb; ipdb.set_trace()
    #    self.failUnless(view())
        
    def test_printout_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@printout-settings')
    
    def test_use_default_template_template(self):
        self.failUnless('use_default_template' in IPrintoutSettings)
        self.assertEquals(self.registry[
            'collective.printout.interfaces.IPrintoutSettings.' +
            'use_default_template'], 
            True)
    
    def test_record_default_template(self):
        record_default_template = self.registry.records[
            'collective.printout.interfaces.IPrintoutSettings.default_template']
        self.failUnless('default_template' in IPrintoutSettings)
        self.assertTrue("xml" in record_default_template.value)
    
    def test_use_default_body_stylesheet(self):
        self.failUnless('use_default_body_stylesheet' in IPrintoutSettings)
        self.assertEquals(self.registry[
            'collective.printout.interfaces.IPrintoutSettings.' +
            'use_default_body_stylesheet'],
            True)
    
    def test_record_default_body_stylesheet(self):
        record_default_body_stylesheet = self.registry.records[
            'collective.printout.interfaces.IPrintoutSettings.default_body_stylesheet']
        self.failUnless('default_body_stylesheet' in IPrintoutSettings)
        self.assertTrue("xml" in record_default_body_stylesheet.value)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
                                