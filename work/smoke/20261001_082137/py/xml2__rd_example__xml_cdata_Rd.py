import lxml.etree as etree

# xml_new_root creates a document with a root element
# r2py:entity:x
doc = etree.ElementTree(etree.Element("root"))
x = doc.getroot()

# In R, xml_add_child(x, xml_cdata("<d/>")) adds the CDATA as a child.
# In lxml, CDATA is typically assigned to .text or .tail. 
# To make it a child "node" in the resulting string, we assign it to the root's text.
# r2py:entity:xml_add_child
x.text = etree.CDATA("<d/>")

# as.character(x) on an xml_node returns the XML string representation
# To include the XML declaration and trailing newline as R does:
# r2py:entity:as.character
as_character_x = etree.tostring(doc, encoding='UTF-8', xml_declaration=True).decode('utf-8') + '\n'
print(as_character_x)