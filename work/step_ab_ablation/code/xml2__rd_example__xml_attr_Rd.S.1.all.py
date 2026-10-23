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
    
    # Handle namespaced attributes if a mapping is provided
    if isinstance(ns, dict) and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            if val is not None:
                return val
    
    # Fallback to direct match
    return x.get(attr)

def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = x.attrib
    if isinstance(ns, dict):
        # R's xml_attrs(doc, ns) converts {url}local back to prefix:local
        inv_ns = {v: k for k, v in ns.items()}
        res = {}
        for k, v in attrs.items():
            if '}' in k:
                url, local = k.split('}', 1)
                url = url[1:]
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
xml_attr_res1 = xml_attr(x, "id")
xml_attr_res2 = xml_attr(x, "apple")
xml_attrs_res1 = xml_attrs(x)

kids = xml_children(x)
xml_attr_kids = xml_attr(kids, "id")
xml_has_attr_kids = xml_has_attr(kids, "id")
xml_attrs_kids = xml_attrs(kids)

# Missing attributes
xml_attr_missing = xml_attr(xml_children(x), "d")
xml_has_attr_missing = xml_has_attr(xml_children(x), "d")

# Namespace example
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
doc = xml_children(x)[0]

# In R, xml_ns returns a named character vector. 
# For Python logic, we use a dictionary.
ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
ns = ns_map # Using dict as ns to mimic named vector behavior in helpers

xml_attrs_doc1 = xml_attrs(doc)
xml_attrs_doc2 = xml_attrs(doc, ns)

# Attribute access
xml_attr_doc_id = xml_attr(doc, "id")
xml_attr_doc_bid = xml_attr(doc, "b:id", ns)
xml_attr_doc_id_ns = xml_attr(doc, "id", ns)

# Set attributes
# R: xml_attr(doc, "id") <- "one"
xml_set_attr(doc, "id", "one")
xml_set_attr(doc, "id", "two")

# Set multiple attributes
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
# R: xml_attrs(doc) <- c(...)
xml_set_attrs(doc, attrs_val, ns)
# R: xml_set_attrs(doc, c(...))
xml_set_attrs(doc, attrs_val, ns)