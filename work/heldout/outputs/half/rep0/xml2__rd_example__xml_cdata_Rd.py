# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# r2py:entity:x
# xml_new_root("root") creates a document with a root element
x = etree.Element("root")

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a child node containing the CDATA.
# Since CDATA is a text node in XML, we create an empty element and set its text as CDATA.
# However, looking at R's xml2 behavior, xml_add_child with a cdata object 
# creates a child with no tag name (a text node of type CDATA).
# In lxml, to add a CDATA section as a child, we can use a dummy element or 
# just set the text of the parent if it's the first child.
# To correctly emulate xml_add_child(x, xml_cdata(...)), we append the CDATA object.
# But lxml.etree.Element.append() requires an Element.
# The correct way to add CDATA in lxml is to set the .text of an element.
# Since the R source suggests adding a child that IS the CDATA, 
# and the resulting as.character(x) is likely '<root><![CDATA[<d/>]]></root>',
# we assign the CDATA to the text of the root.

cdata_content = etree.CDATA("<d/>")
x.text = cdata_content

# r2py:entity:as.character
# as.character(x) returns the XML string representation.
as_character_x = etree.tostring(x, encoding='unicode')