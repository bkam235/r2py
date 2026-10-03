# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# xml_new_root("root") creates a document with a root element
# r2py:entity:x
x = etree.Element("root")

# xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section as a child.
# In lxml, to add CDATA content to an element, we assign it to the text attribute.
# r2py:entity:xml_add_child
x.text = etree.CDATA("<d/>")

# as.character(x) returns the XML string.
# etree.tostring produces the XML; we use encoding="unicode" for a string.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding="unicode")
print(as_character_x)