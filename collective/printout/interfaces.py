# -*- coding: utf-8 -*-
import os

from zope import schema
from zope.interface import Interface

from collective.printout import CollectivePrintoutMessageFactory as _

dirname = os.path.dirname(__file__)

filename_default = os.path.abspath(
    os.path.join(dirname, 'templates', 'default.pt'))
fileObj = open(filename_default, "r")
DEFAULT_TEMPLATE = u"%s" % fileObj.read()
fileObj.close()


filename_default = os.path.abspath(
    os.path.join(dirname, 'templates', 'body.xsl'))
fileObj = open(filename_default, "r")
DEFAULT_BODY_STYLESHEET = u"%s" % fileObj.read()
fileObj.close()


class IPrintoutLayer(Interface):
    """Request marker installed via browserlayer.xml.
    """


class IPrintable(Interface):
    """Marker interface for printout content objects.
    """


class IPrintoutSettings(Interface):

    use_default_template = schema.Bool(
        title=_(u"label_use_default_template",
                default=u"Use default template"),
        description=_(u"help_use_default_template",
                default=u""),
        required=False,
        default=True,
        )

    default_template = schema.Text(
        title=_(u"Default template"),
        description=_(u"help_default_template",
                      default=u"Zope Page Template (ZPT). The following variables are available: context, plone_portal_state, plone_tools, and plone_context_state. Make sure you use Python syntax for expressions since we are using Chameleon to render this template."),
        required=False,
        default=DEFAULT_TEMPLATE,
    )

    use_default_body_stylesheet = schema.Bool(
        title=_(u"label_use_default_body_stylesheet",
                default=u"Use default template"),
        description=_(u"help_use_default_body_stylesheet",
                default=u"If enabled, a default template for the body text is used."),
        required=False,
        default=True,
        )

    default_body_stylesheet = schema.Text(
        title=_(u"Default body stylesheet"),
        description=_(u"help_default_body_stylesheet",
                      default=u"XSLT stylesheet to transform the HTML of the document body text to XSL-FO which is later transformed to PDF."),
        required=False,
        default=DEFAULT_BODY_STYLESHEET,
    )
