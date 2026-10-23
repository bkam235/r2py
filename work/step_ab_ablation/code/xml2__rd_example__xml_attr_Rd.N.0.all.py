import lxml.etree as ET
import pandas as pd
import numpy as np
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/xml2__rd_example__xml_attr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__rd_example__xml_attr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['kids']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Helper functions to mimic xml2 behavior
def xml_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns) for node in x]
    
    # Handle namespaced attributes if a mapping is provided and prefix is present
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        # ns in R's xml2 is a named character vector
        # In Python, we treat it as a dict for lookup
        if isinstance(ns, dict) and prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            return val if val is not None else None
    
    # Standard attribute lookup
    return x.get(attr)

def xml_attrs(x, ns=None):
    if isinstance(x, list):
        # In R, xml_attrs on a node set usually throws an error or handles differently,
        # but for the sake of this translation, we follow the mapping.
        return [xml_attrs(node, ns) for node in x]
    
    attrs = x.attrib
    if ns is not None and isinstance(ns, dict):
        # Map {url}local -> prefix:local using the ns map
        inv_ns = {v: k for k, v in ns.items()}
        result = {}
        for k, v in attrs.items():
            if '}' in k:
                url, local = k.split('}', 1)
                url = url[1:]
                prefix = inv_ns.get(url, 'unknown')
                result[f"{prefix}:{local}"] = v
            else:
                result[k] = v
        return result
    return dict(attrs)

def xml_children(x):
    return list(x)

def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    # In R, xml_has_attr returns TRUE/FALSE. 
    # If the attribute exists (even if empty string), it is TRUE.
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if isinstance(ns, dict) and prefix in ns:
            return x.get(f"{{{ns[prefix]}}}{local}") is not None
    return attr in x.attrib

def xml_set_attr(x, attr, value, ns=None):
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if isinstance(ns, dict) and prefix in ns:
            attr = f"{{{ns[prefix]}}}{local}"
    x.set(attr, value)

def xml_set_attrs(x, value_dict, ns=None):
    for attr, val in value_dict.items():
        xml_set_attr(x, attr, val, ns)

def xml_ns(x):
    # R's xml_ns returns a named character vector of namespaces
    # Python's nsmap is {prefix: url}. We'll use this dict.
    return {k: v for k, v in x.nsmap.items() if k is not None}

# Main execution
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")
xml_attr_1 = xml_attr(x, "id")
xml_attr_2 = xml_attr(x, "apple")
xml_attrs_1 = xml_attrs(x)

kids = xml_children(x)
# kids is just the list of elements
xml_attr_3 = xml_attr(kids, "id")
xml_has_attr_1 = xml_has_attr(kids, "id")
xml_attrs_2 = xml_attrs(kids)

# Missing attributes
xml_attr_4 = xml_attr(xml_children(x), "d")
xml_has_attr_2 = xml_has_attr(xml_children(x), "d")

# Namespace example
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
doc = xml_children(x)[0]
ns = xml_ns(x)

xml_attrs_3 = xml_attrs(doc)
xml_attrs_4 = xml_attrs(doc, ns)

# If you don't supply a ns spec, you get the first matching attribute
xml_attr_5 = xml_attr(doc, "id")
xml_attr_6 = xml_attr(doc, "b:id", ns)
xml_attr_7 = xml_attr(doc, "id", ns)

# Can set a single attribute
# xml_attr(doc, "id") <- "one"
xml_set_attr(doc, "id", "one")
xml_set_attr(doc, "id", "two")

# Set multiple attributes
attrs_update = {"b:id": "one", "f:id": "two", "id": "three"}
# xml_attrs(doc) <- attrs_update
xml_set_attrs(doc, attrs_update, ns)
xml_set_attrs(doc, attrs_update, ns)