# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import lxml.etree as ET

# r2py:entity:x
# xml_new_root in R creates a document with a root element.
x = ET.Element("root")

# r2py:entity:xml_add_child
# xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section.
# In lxml, appending a CDATA object directly to an element is not supported; 
# it must be assigned to text or tail.
x.text = ET.CDATA("<d/>")

# r2py:entity:as.character
# as.character(x) in R's xml2 includes the XML declaration and a trailing newline.
# ET.tostring with xml_declaration=True requires encoding to be bytes (not unicode).
xml_bytes = ET.tostring(x, encoding='UTF-8', xml_declaration=True)
as_character_x = xml_bytes.decode('utf-8') + "\n"
print(as_character_x)