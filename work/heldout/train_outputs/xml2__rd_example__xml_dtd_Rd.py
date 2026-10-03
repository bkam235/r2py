# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import lxml.etree as etree

# r2py:entity:r
# xml_new_root(xml_dtd(...)) in R creates a document with a DOCTYPE and a root element of that name.
dtd_name = "html"
external_id = "-//W3C//DTD XHTML 1.0 Transitional//EN"
system_id = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"

# Construct the XML string with DOCTYPE to mimic xml2's behavior
r_string = f'<!DOCTYPE {dtd_name} PUBLIC "{external_id}" "{system_id}"><{dtd_name}/>'
parser_r = etree.XMLParser(resolve_entities=True)
r = etree.fromstring(r_string.encode('utf-8'), parser=parser_r)

# r2py:entity:d
d_xml_string = '''<!DOCTYPE doc [
<!ELEMENT doc (#PCDATA)>
<!ENTITY foo " test ">
]>
<doc>This is a valid document &foo; !</doc>'''

# To resolve internal entities like &foo;, we use a parser with resolve_entities=True
parser_d = etree.XMLParser(resolve_entities=True)
d = etree.fromstring(d_xml_string.encode('utf-8'), parser=parser_d)