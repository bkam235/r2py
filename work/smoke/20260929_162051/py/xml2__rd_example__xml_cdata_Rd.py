import lxml.etree as etree

# xml_new_root("root") creates a document and a root element.
# r2py:entity:x
x = etree.Element("root")

# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA node.
# In lxml, CDATA is handled as text. To get <root><![CDATA[<d/>]]></root>,
# we set the text of the root element to a CDATA object.
# r2py:entity:xml_add_child
x.text = etree.CDATA("<d/>")

# R's as.character(x) returns the XML string and auto-prints it.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')
print(as_character_x)