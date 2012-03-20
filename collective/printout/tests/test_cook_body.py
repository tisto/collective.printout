import unittest2 as unittest

from lxml import etree

from collective.printout.util import cook_body
from collective.printout.interfaces import DEFAULT_BODY_STYLESHEET


class CookBodyTest(unittest.TestCase):

    def setUp(self):
        self.ns = 'http://www.w3.org/1999/XSL/Format'
    
    def test_paragraph(self):
        html = "<html><body><p>a simple paragraph</p></body></html>"
        tree = etree.XML(cook_body(html, DEFAULT_BODY_STYLESHEET))
        self.assertEquals(tree.xpath("child::*")[0].text, 'a simple paragraph')
        self.assertEquals(len(tree.xpath("child::*")), 1)
    
    def test_h1(self):
        html = "<html><body><h1>headline</h1></body></html>"
        tree = etree.XML(cook_body(html, DEFAULT_BODY_STYLESHEET))
        self.assertEquals(tree.xpath("child::*")[0].text, 'headline')
        self.assertEquals(len(tree.xpath("/*")), 1)
    
    def test_ul(self):
        html = "<html><body><ul><li>foo</li><li>bar</li></html>"
        tree = etree.XML(cook_body(html, DEFAULT_BODY_STYLESHEET))
        self.assertEquals(tree.xpath("child::*")[0].tag, 
                          "{%s}list-block" % self.ns)
        self.assertEquals(len(tree.findall(".//{%s}list-item" % self.ns)), 2)
        self.assertEquals(len(tree.findall(".//{%s}list-item-label" % self.ns)), 2)
        self.assertEquals(len(tree.findall(".//{%s}list-item-body" % self.ns)), 2)
        
    def test_combination(self):
        html = "<html><body><h2>headline</h2><p>paragraph</p></body></html>"
        tree = etree.XML(cook_body(html, DEFAULT_BODY_STYLESHEET))
        result = etree.tostring(tree)
        self.assertEquals(len(tree.findall(".//*")), 2)
    
    def test_full(self):
        html = "<h2>headline</h2><p>paragraph</p><ul><li>one</li><li>two</li></ul><p>paragraph</p><ol><li>foo</li><li>bar</li></ol>"
        tree = etree.XML(cook_body(html, DEFAULT_BODY_STYLESHEET))
        result = etree.tostring(tree)
        self.assertEquals(len(tree.findall(".//*")), 16)
        
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
