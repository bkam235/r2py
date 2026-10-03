import lxml.etree as etree

# r2py:entity:x
x = etree.Element("root")

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA node as a child.
# In lxml, CDATA is placed in .text or .tail. To simulate a child CDATA node, 
# we set the root's text to the CDATA object.
x.text = etree.CDATA("<d/>")

# r2py:entity:as.character
# R's as.character(x) for an xml_node returns the XML string representation.
as_character_x = etree.tostring(x, encoding='unicode')
print(as_character_x)