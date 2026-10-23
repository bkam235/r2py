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
    
    # Handle namespaced attribute lookup
    if ns is not None and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            val = x.get(f"{{{ns[prefix]}}}{local}")
            if val is not None:
                return val
    
    # Try direct match
    return x.get(attr)

def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    
    attrs = dict(x.attrib)
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
    return attrs

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

def xml_set_attrs(x, value, ns=None):
    for attr, val in value.items():
        xml_set_attr(x, attr, val, ns)

# Main script
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

print(xml_attr(x, "id"))
print(xml_attr(x, "apple"))
print(xml_attrs(x))

kids = xml_children(x)
print(kids)
print(xml_attr(kids, "id"))
print(xml_has_attr(kids, "id"))
print(xml_attrs(kids))

# Missing attributes give missing values
print(xml_attr(xml_children(x), "d"))
print(xml_has_attr(xml_children(x), "d"))

# If the document has a namespace, use the ns argument and
# qualified attribute names
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
doc = xml_children(x)[0]
ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
ns = ns_map # Store as dict for easy lookup

print(xml_attrs(doc))
print(xml_attrs(doc, ns))

# If you don't supply a ns spec, you get the first matching attribute
print(xml_attr(doc, "id"))
print(xml_attr(doc, "b:id", ns))
print(xml_attr(doc, "id", ns))

# Can set a single attribute with `xml_attr() <-` or `xml_set_attr()`
xml_set_attr(doc, "id", "one")
xml_set_attr(doc, "id", "two")

# Or set multiple attributes with `xml_attrs()` or `xml_set_attrs()`
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
xml_set_attrs(doc, attrs_val, ns)