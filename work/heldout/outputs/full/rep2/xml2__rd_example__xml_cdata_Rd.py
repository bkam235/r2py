# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# xml_new_root creates a document and returns the root element
# r2py:entity:x
x = etree.Element("root")

# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section as a child.
# In lxml, CDATA is part of the text/tail of an element. 
# To simulate adding a CDATA child to a root, we assign it to the root's text.
# r2py:entity:xml_add_child
xml_cdata_val = etree.CDATA("<d/>")
x.text = xml_cdata_val

# as.character(x) on an xml_node returns the XML string representation.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')