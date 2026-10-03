# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# xml_new_root("root")
# r2py:entity:x
x = etree.Element("root")

# xml_add_child(x, xml_cdata("<d/>"))
# r2py:entity:xml_add_child
cdata_content = etree.CDATA("<d/>")
x.text = cdata_content

# as.character(x)
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding="unicode")