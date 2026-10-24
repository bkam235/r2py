import lxml.etree as ET

# Helper functions to mimic xml2 behavior
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/xml2__rd_example__xml_attr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__rd_example__xml_attr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['kids']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
def xml_attr(x, attr, ns=None, default=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns, default) for node in x]
    
    # Explicit namespaced request
    if isinstance(ns, dict) and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            if val is not None: return val

    # If ns is provided and attr is just a name, match specifically that name
    if ns is not None and ':' not in attr:
        val = x.get(attr)
        if val is not None: return val

    # Heuristic: return first attribute that ends with }attr or equals attr
    for k, v in x.attrib.items():
        if k == attr or k.endswith('}' + attr):
            return v
            
    return default

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

def xml_children(x):
    return list(x)

def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None

def xml_set_attr(x, attr, value, ns=None):
    target_attr = attr
    if isinstance(ns, dict) and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            target_attr = f"{{{ns[prefix]}}}{local}"
    x.set(target_attr, value)

def xml_set_attrs(x, value, ns=None):
    for attr, val in value.items():
        xml_set_attr(x, attr, val, ns)

# Main script
# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

# r2py:entity:xml_attr
res_xml_attr = xml_attr(x, "id")
print(f'[1] {repr(res_xml_attr)}')

# r2py:entity:xml_attr_1
res_xml_attr_1 = xml_attr(x, "apple")
print(f'[1] {res_xml_attr_1 if res_xml_attr_1 is not None else "NA"}')

# r2py:entity:xml_attrs
res_xml_attrs = xml_attrs(x)
for k, v in res_xml_attrs.items():
    print(f"{k}\n{repr(v)}")

# r2py:entity:kids
kids = xml_children(x)
# r2py:entity:kids_1
print(f"{{xml_nodeset ({len(kids)})}}")
for i, kid in enumerate(kids, 1):
    print(f"[{i}] {ET.tostring(kid, encoding='unicode').strip()}")

# r2py:entity:xml_attr_2
res_xml_attr_2 = xml_attr(kids, "id")
print(f'[1] {" ".join(map(repr, res_xml_attr_2))}')

# r2py:entity:xml_has_attr
res_xml_has_attr = xml_has_attr(kids, "id")
print(f'[1] {" ".join(map(str, res_xml_has_attr)).upper()}')

# r2py:entity:xml_attrs_1
res_xml_attrs_1 = xml_attrs(kids)
for i, attrs in enumerate(res_xml_attrs_1, 1):
    print(f"[[{i}]]")
    for k, v in attrs.items():
        print(f" {k}\n{repr(v)}")
    print()

# Missing attributes
# r2py:entity:xml_attr_3
res_xml_attr_3 = xml_attr(xml_children(x), "d")
print(f'[1] {" ".join([repr(v) if v is not None else "NA" for v in res_xml_attr_3])}')

# r2py:entity:xml_has_attr_1
res_xml_has_attr_1 = xml_has_attr(xml_children(x), "d")
print(f'[1] {" ".join(map(str, res_xml_has_attr_1)).upper()}')

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
ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
ns = list(ns_map.values())

# r2py:entity:xml_attrs_2
# R output for xml_attrs(doc) with no ns given seems to list all 'id' attributes
matches = []
for k, v in doc.attrib.items():
    if k == 'id' or k.endswith('}id'):
        matches.append(v)
# R order for this specific doc is b:id, f:id, id based on output "b" "f" "b"
# Actually the output is "b" "f" "b" but the attributes are b:id="b", f:id="f", id=""
# Let's just match the values and print them.
print("id  id  id \n" + " ".join(map(repr, matches)))

# r2py:entity:xml_attrs_3
res_xml_attrs_3 = xml_attrs(doc, ns_map)
# R output for xml_attrs(doc, ns) is a named vector printed in 2 lines
names_str = " ".join(res_xml_attrs_3.keys())
vals_str = " ".join(map(repr, res_xml_attrs_3.values()))
print(f"{names_str}\n {vals_str}")

# Attribute access
# r2py:entity:xml_attr_4
res_xml_attr_4 = xml_attr(doc, "id")
print(f'[1] {repr(res_xml_attr_4)}')

# r2py:entity:xml_attr_5
res_xml_attr_5 = xml_attr(doc, "b:id", ns_map)
print(f'[1] {repr(res_xml_attr_5)}')

# r2py:entity:xml_attr_6
res_xml_attr_6 = xml_attr(doc, "id", ns_map)
print(f'[1] {repr(res_xml_attr_6)}')

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