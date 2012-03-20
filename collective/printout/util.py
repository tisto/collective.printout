# Code taken from zopyx.convert

import sys
import tempfile

from StringIO import StringIO

from lxml import etree

from subprocess import Popen, PIPE
from collective.printout import log


def cook_body(html, xslt):
    
    # Prepare XSLT stylesheet
    xslt_filename = tempfile.mktemp()
    xslt_file = open(xslt_filename, 'w')
    xslt_file.write(xslt)
    xslt_file.close()
    
    # Convert HTML -> elementtree

    # Parse HTML (try to recover if not valid HTML, remove blanks between two 
    # tags, clean up namespaces)
    parser = etree.HTMLParser(recover=True, 
                              remove_blank_text=True)
    htmltree = etree.parse(StringIO(html), parser)

    # Parse XSLT stylesheet
    styletree = etree.parse(xslt_filename)
    #try:
    #except etree.XMLSyntaxError, e:
    #    log.error(e)
    
    # load the xslt stylesheet
    transform = etree.XSLT(styletree)
    
    # transform the html tree
    resulttree = transform(htmltree)
    
    # strip whitespace inside two tags, e.g. <p> lorem ipsum </p> => <p>lorem ipsum</p>
    for element in resulttree.iter("*"):
        if element.text is not None and not element.text.strip():
            element.text = None
    
    return etree.tostring(resulttree)


def newTempfile(suffix=''):
    return tempfile.mktemp(suffix=suffix)


def runcmd(cmd):
    """ Execute a command using the subprocess module """


    stdin = open('/dev/null')
    stdout = stderr = PIPE

    p = Popen(cmd,
              shell=True,
              stdin=stdin,
              stdout=stdout,
              stderr=stderr,
              )

    status = p.wait()
    stdout_ = p.stdout.read().strip()
    stderr_ = p.stderr.read().strip()

    if stdout_:
        log.info(stdout_)
    if stderr_:
        log.info(stderr_)
    return status, stdout_ + stderr_
