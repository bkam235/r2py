# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# r2py:entity:x
# xml_new_root creates a document and adds a root element
# To include the XML declaration later, we create an ElementTree
x = etree.Element("root")
tree = etree.ElementTree(x)

# r2py:entity:xml_add_child
# In xml2, xml_add_child with xml_cdata adds a CDATA section as a child.
# In lxml, CDATA is treated as text content of an element.
xml_cdata_content = etree.CDATA("<d/>")
x.text = xml_cdata_content

# r2py:entity:as.character
# as.character(x) returns the XML string representation including the declaration
# we must use encoding="UTF-8" (bytes) to allow xml_declaration=True, then decode.
result = etree.tostring(tree, encoding="UTF-8", xml_declaration=True).decode("utf-8") + "\n"
print(result)