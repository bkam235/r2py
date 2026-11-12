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

def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = dict(x.attrib)
    if isinstance(ns, dict):
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
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

res_xml_attr = xml_attr(x, "id")
print(res_xml_attr)

res_xml_attr_1 = xml_attr(x, "apple")
print(res_xml_attr_1)

res_xml_attrs = xml_attrs(x)
print(res_xml_attrs)

kids = xml_children(x)
print(kids)

res_xml_attr_2 = xml_attr(kids, "id")
print(res_xml_attr_2)

res_xml_has_attr = xml_has_attr(kids, "id")
print(res_xml_has_attr)

res_xml_attrs_1 = xml_attrs(kids)
print(res_xml_attrs_1)

# Missing attributes
res_xml_attr_3 = xml_attr(xml_children(x), "d")
print(res_xml_attr_3)

res_xml_has_attr_1 = xml_has_attr(xml_children(x), "d")
print(res_xml_has_attr_1)

# Namespace example
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
doc = xml_children(x)[0]

ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
ns = list(ns_map.values())

res_xml_attrs_2 = xml_attrs(doc)
print(res_xml_attrs_2)

res_xml_attrs_3 = xml_attrs(doc, ns_map)
print(res_xml_attrs_3)

res_xml_attr_4 = xml_attr(doc, "id")
print(res_xml_attr_4)

res_xml_attr_5 = xml_attr(doc, "b:id", ns_map)
print(res_xml_attr_5)

res_xml_attr_6 = xml_attr(doc, "id", ns_map)
print(res_xml_attr_6)

# Set attributes
xml_set_attr(doc, "id", "one") 
xml_set_attr(doc, "id", "two")

# Set multiple attributes
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
xml_set_attrs(doc, attrs_val, ns_map)