# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
_ = CollectivePrintoutMessageFactory = MessageFactory('collective.printout')

import logging
log = logging.getLogger("collective.printout")

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
