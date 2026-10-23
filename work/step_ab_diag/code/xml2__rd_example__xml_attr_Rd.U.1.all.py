# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/xml2__rd_example__xml_attr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__rd_example__xml_attr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['kids']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import lxml.etree as ET

# Helper functions to mimic xml2 behavior
# r2py:entity:xml_attr
def xml_attr(x, attr, ns=None, default=None):
    if isinstance(x, list):
        res = [xml_attr(node, attr, ns, default) for node in x]
        return res
    
    # In xml2, if ns is not provided, it looks for the attribute as is.
    # If ns is provided and the attribute is namespaced (e.g., "b:id"), 
    # it resolves the prefix.
    
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            if val is not None:
                return val
    
    val = x.get(attr)
    return val if val is not None else default

# r2py:entity:xml_attrs
def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = x.attrib
    if ns is not None:
        # Map {url}local -> prefix:local
        inv_ns = {v: k for k, v in ns.items()}
        new_attrs = {}
        for k, v in attrs.items():
            if '}' in k:
                url, local = k.split('}', 1)
                url = url[1:]
                prefix = inv_ns.get(url, 'unknown')
                new_attrs[f"{prefix}:{local}"] = v
            else:
                new_attrs[k] = v
        return new_attrs
    return dict(attrs)

# r2py:entity:xml_children
def xml_children(x):
    return list(x)

# r2py:entity:xml_has_attr
def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None

# r2py:entity:xml_set_attr
def xml_set_attr(x, attr, value, ns=None):
    target_attr = attr
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            target_attr = f"{{{ns[prefix]}}}{local}"
    x.set(target_attr, value)

# r2py:entity:xml_set_attrs
def xml_set_attrs(x, value, ns=None):
    for attr, val in value.items():
        xml_set_attr(x, attr, val, ns)

# Main script
# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")
# r2py:entity:xml_attr
print(f"[1] {xml_attr(x, 'id')}")
# r2py:entity:xml_attr_1
print(f"[1] {None if (res := xml_attr(x, 'apple')) is None else res}") # Simulating NA
# r2py:entity:xml_attrs
print(xml_attrs(x))

# r2py:entity:kids_1
kids = xml_children(x)
print(f"{{xml_nodeset ({len(kids)})}}")
for i, kid in enumerate(kids, 1):
    print(f"[{i}] {ET.tostring(kid, encoding='unicode').strip()}")

# r2py:entity:xml_attr_2
print(f"[1] {xml_attr(kids, 'id')}")
# r2py:entity:xml_has_attr
print(f"[1] {xml_has_attr(kids, 'id')}")
# r2py:entity:xml_attrs_1
attrs_kids = xml_attrs(kids)
for i, a in enumerate(attrs_kids, 1):
    print(f"[[{i}]]")
    for k, v in a.items():
        print(f" {k} \n\"{v}\"")

# Missing attributes
# r2py:entity:xml_attr_3
print(f"[1] {xml_attr(xml_children(x), 'd')}")
# r2py:entity:xml_has_attr_1
print(f"[1] {xml_has_attr(xml_children(x), 'd')}")

# Namespace example
# r2py:entity:x_1
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
# r2py:entity:doc
doc = xml_children(x)[0]
# r2py:entity:ns
ns = x.nsmap.copy()
if None in ns:
    del ns[None]

# r2py:entity:xml_attrs_2
print(xml_attrs(doc))
# r2py:entity:xml_attrs_3
print(xml_attrs(doc, ns))

# Attribute access
# r2py:entity:xml_attr_4
print(f"[1] {xml_attr(doc, 'id')}")
# r2py:entity:xml_attr_5
print(f"[1] {xml_attr(doc, 'b:id', ns)}")
# r2py:entity:xml_attr_6
print(f"[1] {xml_attr(doc, 'id', ns)}")

# Set attributes
# r2py:entity:xml_attr(doc, "id")
xml_set_attr(doc, "id", "one")
# r2py:entity:xml_set_attr
xml_set_attr(doc, "id", "two")

# Set multiple attributes
# r2py:entity:xml_attrs(doc)
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
# r2py:entity:xml_set_attrs
xml_set_attrs(doc, attrs_val, ns)