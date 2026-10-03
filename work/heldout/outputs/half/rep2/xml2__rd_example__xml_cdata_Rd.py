import lxml.etree as etree

# xml_new_root("root") creates a document with a root element
# r2py:entity:x
doc = etree.ElementTree(etree.Element("root"))
x = doc.getroot()

# xml_cdata("<d/>") creates a CDATA section. 
# In lxml, we can't append a CDATA object directly as a child element.
# We add it as the text of a new child element, but since the R output 
# for xml_add_child with cdata is a CDATA node, we use a trick:
# we create a child element with no tag (which is not possible) or 
# simply use the fact that text/tail can be CDATA.
# However, the most equivalent way to produce the XML string is:
# r2py:entity:xml_add_child
cdata_content = etree.CDATA("<d/>")
# We create an empty element and set its text to CDATA, but R's xml_add_child
# with xml_cdata creates a node that looks like <root><![CDATA[<d/>]]></root>
# In lxml, this is simply adding the CDATA to the text of the root.
x.text = cdata_content

# Convert the element to string. unicode encoding handles the decoding.
# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')
print(as_character_x)