import lxml.etree as etree

# r2py:entity:x
# xml_new_root in R creates a document and adds a root element
doc = etree.ElementTree(etree.Element("root"))
x = doc.getroot()

# r2py:entity:xml_add_child
# In R, xml_add_child(x, xml_cdata("<d/>")) adds a CDATA section as a child.
cdata_content = etree.CDATA("<d/>")
x.text = cdata_content

# r2py:entity:as.character
# R's as.character(x) for an xml_document includes the XML declaration and a newline.
# etree.tostring(doc, ...) returns bytes.
res_bytes = etree.tostring(doc, encoding="UTF-8", xml_declaration=True, pretty_print=False)
as_character_x = res_bytes.decode("utf-8")

# Fix the XML declaration quotes to match R (single quotes to double quotes)
if as_character_x.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
    as_character_x = as_character_x.replace("version='1.0'", 'version="1.0"').replace("encoding='UTF-8'", 'encoding="UTF-8"')

# R's xml2 as.character output for documents typically ends with a newline
if not as_character_x.endswith("\n"):
    as_character_x += "\n"

# To match R's print output [1] "...", we format it as a character vector
# R escapes double quotes as \" and newlines as \n inside the string literal
escaped_val = as_character_x.replace('"', '\\"').replace('\n', '\\n')
print(f'[1] "{escaped_val}"')