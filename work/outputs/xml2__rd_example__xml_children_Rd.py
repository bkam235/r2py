from lxml import etree

def format_node(node):
    """Helper to mimic R's xml2 printing of nodes."""
    if node is None:
        return "<NA>"
    if isinstance(node, str):
        return f" {node} " # R's xml_contents prints text with surrounding whitespace
    # etree.tostring returns bytes, decode to string
    return etree.tostring(node, encoding='unicode', pretty_print=True).strip()

def print_nodeset(nodes):
    """Helper to mimic R's printing of xml_nodeset."""
    if not nodes:
        print("{xml_nodeset (0)}")
        return
    print(f"{{xml_nodeset ({len(nodes)})}}")
    for i, node in enumerate(nodes, 1):
        print(f"[{i}] {format_node(node)}")

# suppressPackageStartupMessages(library(xml2))
# No action needed for library import in Python.

# x <- read_xml("<foo> <bar><boo /></bar> <baz/> </foo>")
# r2py:entity:x
x = etree.fromstring("<foo> <bar><boo /></bar> <baz/> </foo>")

# xml_children(x)
# r2py:entity:xml_children
children = list(x)
print_nodeset(children)

# xml_children(xml_children(x))
# In R, xml_children(nodeset) returns a flattened nodeset of all children
# r2py:entity:xml_children_1
all_grand_children = []
for child in children:
    all_grand_children.extend(list(child))
print_nodeset(all_grand_children)

# xml_siblings(xml_children(x)[[1]])
# xml_siblings in R returns siblings of the node, excluding itself.
# r2py:entity:xml_siblings
first_child = children[0]
siblings = [sib for sib in x if sib != first_child]
print_nodeset(siblings)

# xml_parent(xml_children(x))
# R's xml_parent on a nodeset returns a nodeset of unique parents.
# r2py:entity:xml_parent
parents = []
seen = set()
for child in children:
    p = child.getparent()
    if p is not None and p not in seen:
        parents.append(p)
        seen.add(p)
print_nodeset(parents)

# Mixed content
# x <- read_xml("<foo> a <b/> c <d>e</d> f</foo>")
# r2py:entity:x_1
x = etree.fromstring("<foo> a <b/> c <d>e</d> f</foo>")

# xml_children(x)
# r2py:entity:xml_children_2
children_mixed = list(x)
print_nodeset(children_mixed)

# xml_contents(x)
# xml_contents returns all child nodes including text nodes.
# r2py:entity:xml_contents
contents = x.xpath("node()")
print_nodeset(contents)

# xml_length(x)
# By default, xml_length counts elements only.
# r2py:entity:xml_length
print(f"[1] {len(list(x))}")

# xml_length(x, only_elements = FALSE)
# r2py:entity:xml_length_1
print(f"[1] {len(x.xpath('node()'))}")

# xml_child makes it easier to select specific children
# xml_child(x)
# r2py:entity:xml_child
child_1 = x[0] if len(x) > 0 else None
print(f"{{xml_node}}\n{format_node(child_1)}")

# xml_child(x, 2)
# r2py:entity:xml_child_1
child_2 = x[1] if len(x) > 1 else None
print(f"{{xml_node}}\n{format_node(child_2)}")

# xml_child(x, "baz")
# This looks for a direct child with the tag "baz"
# r2py:entity:xml_child_2
res = x.xpath("./baz")
child_baz = res[0] if res else None
if child_baz is None:
    print(f"{{xml_missing}}\n<NA>")
else:
    print(f"{{xml_node}}\n{format_node(child_baz)}")