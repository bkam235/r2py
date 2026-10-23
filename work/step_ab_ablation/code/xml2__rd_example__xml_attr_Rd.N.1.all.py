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
def xml_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns) for node in x]
    
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            return x.get(f"{{{ns[prefix]}}}{local}")
    
    return x.get(attr)

def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = x.attrib
    if ns is not None:
        # Map {url}local -> prefix:local
        inv_ns = {v: k for k, v in ns.items()}
        res = {}
        for k, v in attrs.items():
            if k.startswith('{'):
                url, local = k[1:].split('}', 1)
                prefix = inv_ns.get(url, 'unknown')
                res[f"{prefix}:{local}"] = v
            else:
                res[k] = v
        return res
    return dict(attrs)

def xml_children(x):
    return list(x)

def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None

def xml_set_attr(x, attr, value, ns=None):
    target_attr = attr
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            target_attr = f"{{{ns[prefix]}}}{local}"
    x.set(target_attr, value)

def xml_set_attrs(x, values, ns=None):
    for attr, val in values.items():
        xml_set_attr(x, attr, val, ns)

# Main script
# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")
# r2py:entity:xml_attr
xml_attr_res1 = xml_attr(x, "id")
# r2py:entity:xml_attr_1
xml_attr_res2 = xml_attr(x, "apple")
# r2py:entity:xml_attrs
xml_attrs_res1 = xml_attrs(x)

# r2py:entity:kids
kids = xml_children(x)
# r2py:entity:kids_1
# (kids is already defined above)
# r2py:entity:xml_attr_2
xml_attr_kids = xml_attr(kids, "id")
# r2py:entity:xml_has_attr
xml_has_attr_kids = xml_has_attr(kids, "id")
# r2py:entity:xml_attrs_1
xml_attrs_kids = xml_attrs(kids)

# Missing attributes
# r2py:entity:xml_attr_3
xml_attr_missing = xml_attr(xml_children(x), "d")
# r2py:entity:xml_has_attr_1
xml_has_attr_missing = xml_has_attr(xml_children(x), "d")

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
xml_attrs_doc1 = xml_attrs(doc)
# r2py:entity:xml_attrs_3
xml_attrs_doc2 = xml_attrs(doc, ns)

# Attribute access
# r2py:entity:xml_attr_4
xml_attr_doc_id = xml_attr(doc, "id")
# r2py:entity:xml_attr_5
xml_attr_doc_bid = xml_attr(doc, "b:id", ns)
# r2py:entity:xml_attr_6
xml_attr_doc_id_ns = xml_attr(doc, "id", ns)

# Set attributes
# r2py:entity:xml_attr(doc, "id")
# Simulation of xml_attr(doc, "id") <- "one"
xml_set_attr(doc, "id", "one")
# r2py:entity:xml_set_attr
xml_set_attr(doc, "id", "two")

# Set multiple attributes
# r2py:entity:xml_attrs(doc)
# Simulation of xml_attrs(doc) <- c(...)
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
xml_set_attrs(doc, attrs_val, ns)
# r2py:entity:xml_set_attrs
xml_set_attrs(doc, attrs_val, ns)