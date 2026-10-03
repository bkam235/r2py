import lxml.etree as etree

# r2py:entity:x
def format_xml_node(node):
    """Helper to mimic R's xml2 output for single nodes and nodesets."""
    if node is None:
        return "{xml_missing}\n<NA>"
    if isinstance(node, (list, tuple)):
        if not node:
            return "{xml_nodeset (0)}"
        res = []
        for i, n in enumerate(node):
            if isinstance(n, str):
                val = n
            else:
                # R's xml2 printing of elements often pretty-prints and ignores tail
                # For children/nodesets, we need to simulate the R output style
                val = etree.tostring(n, encoding='unicode', pretty_print=True).strip()
            res.append(f"[{i+1}] {val}")
        header = f"{{xml_nodeset ({len(node)})}}"
        return "\n".join([header] + res)
    
    if isinstance(node, str):
        return node
    
    # For single xml_node output
    return f"{{xml_node}}\n{etree.tostring(node, encoding='unicode', pretty_print=True).strip()}"

x = etree.fromstring("<foo> <bar><boo /></bar> <baz/> </foo>")

# xml_children(x)
# r2py:entity:xml_children
xml_children_x = list(x)
print(format_xml_node(xml_children_x))

# xml_children(xml_children(x))
# r2py:entity:xml_children_1
children_of_children = []
for node in xml_children_x:
    children_of_children.extend(list(node))
print(format_xml_node(children_of_children))

# xml_siblings(xml_children(x)[[1]])
# r2py:entity:xml_siblings
first_child = xml_children_x[0]
siblings = [el for el in first_child.getparent() if el is not first_child]
print(format_xml_node(siblings))

# xml_parent(xml_children(x))
# r2py:entity:xml_parent
parents_of_children = [node.getparent() for node in xml_children_x]
seen = set()
unique_parents = []
for p in parents_of_children:
    if p not in seen:
        unique_parents.append(p)
        seen.add(p)
print(format_xml_node(unique_parents))

# Mixed content
# r2py:entity:x_1
x = etree.fromstring("<foo> a <b/> c <d>e</d> f</foo>")

# xml_children(x)
# r2py:entity:xml_children_2
children_x_2 = list(x)
print(format_xml_node(children_x_2))

# xml_contents(x)
# r2py:entity:xml_contents
contents = []
if x.text:
    contents.append(x.text)
for child in x:
    contents.append(child)
    if child.tail:
        contents.append(child.tail)

def format_contents(nodes):
    res = []
    for n in nodes:
        if isinstance(n, str):
            res.append(n)
        else:
            # Elements in xml_contents are printed without their tails
            res.append(etree.tostring(n, encoding='unicode').strip())
    header = f"{{xml_nodeset ({len(nodes)})}}"
    return "\n".join([header] + [f"[{i+1}] {val}" for i, val in enumerate(res)])

print(format_contents(contents))

# xml_length(x)
# r2py:entity:xml_length
print(f"[1] {len(list(x))}")

# xml_length(x, only_elements = FALSE)
# r2py:entity:xml_length_1
all_nodes = []
if x.text: all_nodes.append(x.text)
for child in x:
    all_nodes.append(child)
    if child.tail: all_nodes.append(child.tail)
print(f"[1] {len(all_nodes)}")

# xml_child(x)
# r2py:entity:xml_child
node_child = x[0] if len(x) > 0 else None
print(format_xml_node(node_child))

# xml_child(x, 2)
# r2py:entity:xml_child_1
node_child_2 = x[1] if len(x) > 1 else None
print(format_xml_node(node_child_2))

# xml_child(x, "baz")
# r2py:entity:xml_child_2
baz_child = x.find("baz")
print(format_xml_node(baz_child))