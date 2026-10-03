from lxml import etree

# r2py:entity:xml_type
def xml_type(node):
    if isinstance(node, list):
        return [xml_type(n) for n in node]
    
    if isinstance(node, etree._Element):
        return "element"
    elif isinstance(node, (str, etree._ElementUnicodeResult)):
        return "text"
    elif isinstance(node, etree._CDATA):
        return "cdata"
    elif isinstance(node, etree._Comment):
        return "comment"
    elif isinstance(node, etree._ProcessingInstruction):
        return "processing instruction"
    return "unknown"

# r2py:entity:xml_type_1
def xml_contents(node):
    # xml2's xml_contents returns all children: text, elements, CDATA, etc.
    # In lxml, we must manually collect text and children.
    contents = []
    if node.text:
        # Split text into segments if there are intervening elements
        # However, for simple cases, node.text is the first child if it's text
        contents.append(node.text)
    
    for child in node:
        contents.append(child)
        if child.tail:
            contents.append(child.tail)
            
    return contents

# r2py:entity:x
x = etree.fromstring("<foo> a <b /> <![CDATA[ blah]]></foo>")

# r2py:entity:xml_type
res1 = xml_type(x)
# To match R's output format [1] "element"
print(f'[1] "{res1}"')

# r2py:entity:xml_type_1
contents = xml_contents(x)
res2 = xml_type(contents)
# res2 is a list: ["text", "element", "text", "cdata"]
# To match R's output format [1] "text"    "element" "text"    "cdata"
formatted_res2 = '    '.join([f'"{item}"' for item in res2])
print(f'[1] {formatted_res2}')