
from chameleon.zpt.template import PageTemplate
from collective.printout.util import cook_body
from collective.printout.fop import Fop 

# default.pt
file = open("default.pt", "r")
default_template = file.read()
file.close()

# body.xsl
file = open("body.xsl", "r")
default_body_stylesheet = file.read()
file.close()

# input.html
file = open("input.html", "r")
body = file.read()
file.close()

class Context:
    pass

context = Context()
context.Title = "This is a title"
context.Description = "Description"


pt = PageTemplate(default_template)

output = pt.render(context=context, 
                   body=cook_body(body, 
                   default_body_stylesheet))

fo_filename = "tmp.fo"
file = open(fo_filename, "w")
file.write(output)
file.close()

fop = Fop()
output_filename = fop.convert(fo_filename, output_filename="out.pdf")
print output_filename

