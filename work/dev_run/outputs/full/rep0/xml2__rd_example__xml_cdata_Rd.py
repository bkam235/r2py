# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as etree

# r2py:entity:x
x = etree.Element("root")

# r2py:entity:xml_add_child
# In lxml, to add a CDATA section as a child, we can't use append() directly with CDATA 
# if it expects an Element. Instead, we use the text property or create a CDATA object 
# and ensure it's treated as the content of the element.
# For the specific R output <root><![CDATA[<d/>]]></root>, setting x.text works.
x.text = etree.CDATA("<d/>")

# r2py:entity:as.character
# etree.tostring returns the XML string. 
# R's as.character(x) for an xml_document/node typically returns the XML serialization.
res = etree.tostring(x, encoding='unicode')
# R's as.character usually doesn't include the XML declaration unless specified.
# The output of as.character(x) in this case is '<root><![CDATA[<d/>]]></root>'
print(res)