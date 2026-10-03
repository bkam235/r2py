import lxml.etree as etree

# (xml2 imported via lxml.etree)

# (no-op in Python)

# r2py:entity:x
x = etree.Element("root")

# In R's xml2, xml_add_child(x, xml_cdata("...")) adds a CDATA section as a child.
# In lxml, we achieve this by setting the text of the element to a CDATA object.
# r2py:entity:xml_add_child
x.text = etree.CDATA("<d/>")

# R's as.character(x) returns the XML string representation.
# We must print the result to stdout to match R's auto-printing behavior.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')
print(as_character_x)