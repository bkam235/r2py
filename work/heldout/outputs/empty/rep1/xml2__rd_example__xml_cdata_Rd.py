# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# xml_new_root in R creates a root element within a document
# r2py:entity:x
x = etree.Element("root")

# xml_cdata creates a CDATA section. In lxml, to add CDATA as a child,
# we can create an empty element and set its text as a CDATA object, 
# but the R xml2 behavior for xml_add_child(x, xml_cdata(...)) 
# is to add the CDATA block directly as a child node.
# r2py:entity:xml_add_child
cdata_content = etree.CDATA("<d/>")
x.text = cdata_content

# as.character(x) on an xml_node returns the XML representation as a string.
# We use tostring and decode to get the string representation.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')