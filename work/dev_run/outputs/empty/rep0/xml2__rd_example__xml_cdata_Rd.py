import lxml.etree as ET

# (imported via lxml.etree)

# r2py:entity:x
x = ET.Element("root")

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section as a child.
# In lxml, CDATA is handled as a special type of text. 
# To match the R behavior of adding it as a child, we can use an empty element 
# or just set the text of the root if it's the only child.
# However, to be most accurate to "adding a child", we create an element with no tag
# which isn't allowed, so we use a helper or simply assign the CDATA to the root's text.
x.text = ET.CDATA("<d/>")

# r2py:entity:as.character
# R's as.character(x) returns the XML string representation.
print(ET.tostring(x, encoding='unicode'))