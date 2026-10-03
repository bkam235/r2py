# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# r2py:entity:x
x = etree.Element("root")

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section as a child of x.
# In lxml, CDATA is treated as text content.
x.text = etree.CDATA("<d/>")

# r2py:entity:as.character
# as.character(x) in xml2 returns the XML string representation.
as_character_x = etree.tostring(x, encoding='unicode')