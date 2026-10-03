# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# r2py:entity:x
x = etree.Element("root")

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a child node that is a CDATA section.
# In lxml, to create a child that is just CDATA, we create an element with no tag 
# or handle it as text. However, xml2's xml_add_child with xml_cdata typically 
# creates a child node containing the CDATA. 
# Since the R code results in <root><![CDATA[<d/>]]></root>, 
# we set the text of the root element as CDATA.
x.text = etree.CDATA("<d/>")

# r2py:entity:as.character
as_character_x = etree.tostring(x, encoding='unicode')