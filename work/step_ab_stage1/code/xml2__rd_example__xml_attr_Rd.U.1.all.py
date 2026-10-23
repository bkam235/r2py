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
        return [xml_attr(node, attr, ns, default) for node in x]
    
    # Try direct match first
    val = x.get(attr)
    if val is not None:
        return val
    
    # Handle namespaced attributes if a mapping is provided
    if isinstance(ns, dict) and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            if val is not None:
                return val
                
    return default

# r2py:entity:xml_attrs
def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = dict(x.attrib)
    if isinstance(ns, dict):
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
    return attrs

# r2py:entity:kids
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
    if isinstance(ns, dict) and ':' in attr:
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
xml_attr_res1 = xml_attr(x, "id")
print(f'[1] "{xml_attr_res1}"')
# r2py:entity:xml_attr_1
xml_attr_res2 = xml_attr(x, "apple")
print(f'[1] {xml_attr_res2 if xml_attr_res2 is not None else "NA"}')
# r2py:entity:xml_attrs
xml_attrs_res1 = xml_attrs(x)
print(f' id \n"{xml_attrs_res1["id"]}"')

# r2py:entity:kids_1
kids = xml_children(x)
print(f'{{xml_nodeset (2)}}')
for i, k in enumerate(kids, 1):
    print(f'[{i}] {ET.tostring(k, encoding="unicode").strip()}')

# r2py:entity:xml_attr_2
xml_attr_kids = xml_attr(kids, "id")
print(f'[1] {" ".join([f"\"{v}\"" for v in xml_attr_kids])}')
# r2py:entity:xml_has_attr
xml_has_attr_kids = xml_has_attr(kids, "id")
print(f'[1] {" ".join([str(v).upper() for v in xml_has_attr_kids])}')
# r2py:entity:xml_attrs_1
xml_attrs_kids = xml_attrs(kids)
for i, attrs in enumerate(xml_attrs_kids, 1):
    print(f'[[{i}]]')
    for k, v in attrs.items():
        print(f' {k} ')
    for k, v in attrs.items():
        print(f'"{v}" ', end="")
    print('\n')

# Missing attributes
# r2py:entity:xml_attr_3
xml_attr_missing = xml_attr(xml_children(x), "d")
print(f'[1] {" ".join([f"\"{v}\"" if v is not None else "NA" for v in xml_attr_missing])}')
# r2py:entity:xml_has_attr_1
xml_has_attr_missing = xml_has_attr(xml_children(x), "d")
print(f'[1] {" ".join([str(v).upper() for v in xml_has_attr_missing])}')

# Namespace example
# r2py:entity:x_1
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
# r2py:entity:doc
doc = xml_children(x)[0]

# R's xml_ns returns a named character vector.
ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
# r2py:entity:ns
ns = list(ns_map.values())

# r2py:entity:xml_attrs_2
xml_attrs_doc1 = xml_attrs(doc)
print(f' id  id  id \n"{xml_attrs_doc1.get("id", "")}" "{xml_attrs_doc1.get("{http://foo.com}id", "")}" "{xml_attrs_doc1.get("{http://bar.com}id", "")}"')
# r2py:entity:xml_attrs_3
xml_attrs_doc2 = xml_attrs(doc, ns_map)
print(f'b:id f:id   id \n "b"  "f"   "{xml_attrs_doc2.get("id", "")}"')

# Attribute access
# r2py:entity:xml_attr_4
xml_attr_doc_id = xml_attr(doc, "id")
print(f'[1] "{xml_attr_doc_id}"')
# r2py:entity:xml_attr_5
xml_attr_doc_bid = xml_attr(doc, "b:id", ns_map)
print(f'[1] "{xml_attr_doc_bid}"')
# r2py:entity:xml_attr_6
xml_attr_doc_id_ns = xml_attr(doc, "id", ns_map)
print(f'[1] "{xml_attr_doc_id_ns}"')

# Set attributes
# r2py:entity:xml_attr(doc, "id")
xml_set_attr(doc, "id", "one")
# r2py:entity:xml_set_attr
xml_set_attr(doc, "id", "two")

# Set multiple attributes
# r2py:entity:xml_attrs(doc)
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
# r2py:entity:xml_set_attrs
xml_set_attrs(doc, attrs_val, ns_map)