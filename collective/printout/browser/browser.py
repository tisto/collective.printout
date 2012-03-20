# -*- coding: utf-8 -*-
import os
import tempfile

from chameleon.zpt.template import PageTemplate

from types import UnicodeType

from xml.parsers.expat import ExpatError
from xml.sax.saxutils import escape

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage

from ZPublisher.Iterators import filestream_iterator

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides

from plone.registry.interfaces import IRegistry

from collective.printout import log
from collective.printout import CollectivePrintoutMessageFactory as _
from collective.printout.fop import Fop 
from collective.printout.interfaces import IPrintable
from collective.printout.interfaces import IPrintoutSettings
from collective.printout.interfaces import DEFAULT_TEMPLATE 
from collective.printout.interfaces import DEFAULT_BODY_STYLESHEET
from collective.printout.util import cook_body


class Printable(BrowserView):
    """Returns True if content object (context) is printout.
    """
    def __call__(self):
        context = aq_inner(self.context)
        return IPrintable.providedBy(context)


class MakePrintable(BrowserView):
    """View to create a print version of the content object.
    """
    
    def __call__(self):
        context = aq_inner(self.context)
        request = context.REQUEST
        alsoProvides(context, IPrintable)
        IStatusMessage(request).addStatusMessage(
            _("This document is now printable. Click on the 'print' tab for the printed version."),
            type="info")
        request.response.redirect(context.absolute_url())


class Printout(BrowserView):
    """Printout version of the content object.
    """
    
    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request
        # Fetch templates
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IPrintoutSettings)
        # Fetch default template
        if settings.use_default_template:
            self.default_template = DEFAULT_TEMPLATE
        else:
            self.default_template = settings.default_template
        # Fetch body template
        if settings.use_default_body_stylesheet:
            self.default_body_stylesheet = DEFAULT_BODY_STYLESHEET
        else:
            self.default_body_stylesheet = settings.default_body_stylesheet
            
    def __call__(self):
        """Returns the PDF printout.
        """
        context = aq_inner(self.context)
        body = context.getRawText()
                
        # Check there is a template
        if self.default_template == '':
            IStatusMessage(self.request).addStatusMessage(
            _("Template is empty. Check your Printout control panel."),
            type="info")
            return self.request.response.redirect(context.absolute_url())
        
        # Render Chameleon Template
        plone_portal_state = getMultiAdapter((context, self.request), 
                                             name='plone_portal_state')
        plone_tools = getMultiAdapter((context, self.request), 
                                      name='plone_tools')
        plone_context_state = getMultiAdapter((context, self.request), 
                                              name='plone_portal_state')        
        try:
            pt = PageTemplate(self.default_template, 
                              format="xml", 
                              encoding="utf-8", 
                              debug=True)
            cooked_body = cook_body(body, self.default_body_stylesheet)
            output = pt.render(context=context,
                               plone_portal_state=plone_portal_state,
                               plone_tools=plone_tools,
                               plone_context_state=plone_context_state,
                               body=cooked_body)
        except ExpatError, e:
            error = {
                'title'         : "Error rendering the default (chameleon/zpt) template",
                'message'       : str(e),
                'fo_output'     : "",
                'template'      : escape(self.default_template),
                'stylesheet'    : escape(self.default_body_stylesheet),
                'body'          : "",
                'cooked_body'   : ""
            }
            return self.error(error)
        
        # Write Chameleon template output to file for further processing
        log.info("FO OUTPUT:\n\n" + output + "\n")
        fo_filename = tempfile.mktemp()
        fo_file = open(fo_filename, 'w')
        fo_file.write(output)
        fo_file.close()
        
        # Create PDF
        output_filename = self.context.id + ".pdf"
        try:
            fop = Fop()
            output_filename = fop.convert(fo_filename,
                                          output_filename=output_filename)
        except RuntimeError, e:
            log.info("TEMPLATE")
            log.info("--------")
            log.info("\n\n" + self.default_template + "\n\n")
            log.info("--------")
            error = {
                'title'         : "Error running FOP (XSL-FO to PDF transformation)",
                'message'       : str(e),
                'fo_output'     : escape(output),
                'template'      : escape(self.default_template),
                'stylesheet'    : escape(self.default_body_stylesheet),
                'body'          : "",
                'cooked_body'   : ""
            }
            return self.error(error)            

        # Set status message
        IStatusMessage(self.request).addStatusMessage(
            _("Printout"),
            type="info")
        
        # Deliver PDF
        return self.deliver(output_filename)

    def deliver(self, pdf_filename):
        """Stream generated PDF file back to client.
        """
        log.info("Deliver %s" % pdf_filename)
        request = self.request.RESPONSE
        request.setHeader('content-type', 'application/pdf')
        request.setHeader('content-length', os.stat(pdf_filename)[6])
        request.setHeader('content-disposition', 'attachment; filename=%s' % pdf_filename)
        return filestream_iterator(pdf_filename, 'rb')

    def error(self, error):
        """Returns a simple error page with debugging informations.
        """
        dirname = os.path.dirname(__file__)
        
        filename_default = os.path.abspath(os.path.join(dirname, 'error.pt'))
        fileObj = open(filename_default,"r")
        template = u"%s" % fileObj.read()
        fileObj.close()
        pt = PageTemplate(template)
        return pt.render(context=self.context, error=error)
