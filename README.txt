Introduction
============

collective.printout is a PDF-generation solution for Plone.

out-of-the box (like produce and publish) but with more control.

you have to learn/know XSL-FO (standard technology W3C standard).

uses apache FOP, no expensive processors required.

familiar: zpt, xsl-fo

works for custom content types: context.getMyArchetypesField()

the only complicated thing: render the body text (html -> fo -> pdf): 
as long as you are happy with the body, you don't have to touch it. 

fast?: chameleon


default_template:
available: context, plone_portal_state, plone_tools, plone_context_state