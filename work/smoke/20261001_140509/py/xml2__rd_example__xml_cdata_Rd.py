import lxml.etree as etree

# r2py:entity:x
# xml_new_root creates a document and adds the root element
doc = etree.ElementTree(etree.Element("root"))
x = doc.getroot()

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA node as a child of x.
# In lxml, we can't append a CDATA object directly as a child element.
# We must use etree.CDATA and assign it to the text of a new child or the element itself.
# However, to get the exact XML output <root><![CDATA[<d/>]]></root>, 
# we set the text of the root element to the CDATA object.
x.text = etree.CDATA("<d/>")

# r2py:entity:as.character
as_character_result = etree.tostring(x, encoding="unicode")
print(as_character_result)