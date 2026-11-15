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
import xml.etree.ElementTree as ET2


# ---- R-like printing helpers -------------------------------------------------
def _fmt_scalar(v):
    return "NA" if v is None else '"%s"' % v


def print_vec(v):
    if isinstance(v, list):
        print("[1] " + " ".join(_fmt_scalar(x) for x in v))
    else:
        print("[1] " + _fmt_scalar(v))


def print_bool(v):
    if isinstance(v, list):
        print("[1] " + " ".join("TRUE" if b else "FALSE" for b in v))
    else:
        print("[1] " + ("TRUE" if v else "FALSE"))


def _named_vector_lines(items):
    if isinstance(items, dict):
        pairs = list(items.items())
    else:
        pairs = [(k, v) for k, v in items]
    if not pairs:
        return "", ""
    fields = [(str(k), _fmt_scalar(v)) for k, v in pairs]
    width = max(max(len(a), len(b)) for a, b in fields)
    names = " ".join(a.rjust(width) for a, b in fields) + " "
    vals = " ".join(b.rjust(width) for a, b in fields) + " "
    return names, vals


def print_attrs(v):
    is_multi = isinstance(v, list) and len(v) > 0 and isinstance(v[0], list)
    if is_multi:
        for i, item in enumerate(v, 1):
            print("[[%d]]" % i)
            names, vals = _named_vector_lines(item)
            print(names)
            print(vals)
            print()
    else:
        names, vals = _named_vector_lines(v)
        print(names)
        print(vals)


def print_nodeset(nodes):
    print("{xml_nodeset (%d)}" % len(nodes))
    for i, n in enumerate(nodes, 1):
        print("[%d] %s" % (i, ET.tostring(n, encoding="unicode")))


# ---- xml2-like helpers -------------------------------------------------------
def _local_of(name):
    if name.startswith("{"):
        return name.split("}", 1)[1]
    if ":" in name:
        return name.split(":", 1)[1]
    return name


# r2py:entity:xml_attr
def xml_attr(x, attr, ns=None, default=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns, default) for node in x]

    # A supplied ns specification means fully-qualified lookup first
    if isinstance(ns, dict) and len(ns) > 0:
        if ":" in attr:
            prefix, local = attr.split(":", 1)
            if prefix in ns:
                got = x.get("{%s}%s" % (ns[prefix], local), None)
                if got is not None:
                    return got
            return x.get(attr, default)
        return x.get(attr, default)

    # No ns spec: first attribute whose local name matches
    local = _local_of(attr)
    for k, v in x.attrib.items():
        if _local_of(k) == local:
            return v
    return default


# r2py:entity:xml_attrs
def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]

    out = []
    if isinstance(ns, dict) and len(ns) > 0:
        inv = {v: k for k, v in ns.items() if k}
        for k, v in x.attrib.items():
            if k.startswith("{"):
                url, local = k[1:].split("}", 1)
                prefix = inv.get(url)
                if prefix:
                    out.append(("%s:%s" % (prefix, local), v))
                else:
                    out.append((k, v))
            else:
                out.append((k, v))
        return out

    # No ns spec: bare local names; xml2 resolves the value by local name
    # (so an empty attribute falls back to the first attribute with that name)
    for k, v in x.attrib.items():
        local = _local_of(k)
        value = v
        if value == "":
            first = None
            for k2, v2 in x.attrib.items():
                if _local_of(k2) == local:
                    first = v2
                    break
            if first is not None:
                value = first
        out.append((local, value))
    return out


# r2py:entity:xml_children
def xml_children(x):
    return list(x)


def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None


def xml_set_attr(x, attr, value, ns=None):
    if isinstance(x, list):
        for node in x:
            xml_set_attr(node, attr, value, ns)
        return
    target = attr
    if isinstance(ns, dict) and len(ns) > 0 and ":" in attr:
        prefix, local = attr.split(":", 1)
        if prefix in ns and attr not in x.attrib:
            target = "{%s}%s" % (ns[prefix], local)
    x.set(target, value)


def xml_set_attrs(x, value, ns=None):
    if isinstance(x, list):
        for node in x:
            xml_set_attrs(node, value, ns)
        return
    items = value.items() if isinstance(value, dict) else value
    for attr, val in items:
        xml_set_attr(x, attr, val, ns)


# ---- Main script -------------------------------------------------------------
# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

# r2py:entity:xml_attr
print_vec(xml_attr(x, "id"))
# r2py:entity:xml_attr_1
print_vec(xml_attr(x, "apple"))
# r2py:entity:xml_attrs
print_attrs(xml_attrs(x))

# r2py:entity:kids
kids = xml_children(x)
# r2py:entity:kids_1
print_nodeset(kids)

# r2py:entity:xml_attr_2
print_vec(xml_attr(kids, "id"))
# r2py:entity:xml_has_attr
print_bool(xml_has_attr(kids, "id"))
# r2py:entity:xml_attrs_1
print_attrs(xml_attrs(kids))

# Missing attributes
# r2py:entity:xml_attr_3
print_vec(xml_attr(xml_children(x), "d"))
# r2py:entity:xml_has_attr_1
print_bool(xml_has_attr(xml_children(x), "d"))

# Namespace example
# r2py:entity:x_1
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')

# r2py:entity:ns
ns_map = {k: v for k, v in x.nsmap.items() if k}
ns = list(ns_map.values())

# r2py:entity:doc
# Rebuild the child node with literal (non-expanded) attribute names so that
# printing it matches xml2, which does not re-declare the root namespaces.
_inv = {v: k for k, v in ns_map.items()}
doc = ET2.Element(x[0].tag)
for _k, _v in x[0].attrib.items():
    if _k.startswith("{"):
        _url, _local = _k[1:].split("}", 1)
        _pref = _inv.get(_url)
        _name = "%s:%s" % (_pref, _local) if _pref else _local
    else:
        _name = _k
    doc.set(_name, _v)
del _inv, _k, _v

# r2py:entity:xml_attrs_2
print_attrs(xml_attrs(doc))
# r2py:entity:xml_attrs_3
print_attrs(xml_attrs(doc, ns_map))

# Attribute access
# r2py:entity:xml_attr_4
print_vec(xml_attr(doc, "id"))
# r2py:entity:xml_attr_5
print_vec(xml_attr(doc, "b:id", ns_map))
# r2py:entity:xml_attr_6
print_vec(xml_attr(doc, "id", ns_map))

# Set a single attribute with xml_attr() <- or xml_set_attr()
# r2py:entity:xml_attr(doc, "id")
xml_set_attr(doc, "id", "one")
# r2py:entity:xml_set_attr
xml_set_attr(doc, "id", "two")

# Set multiple attributes with xml_attrs() <- or xml_set_attrs()
# r2py:entity:xml_attrs(doc)
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
# r2py:entity:xml_set_attrs
xml_set_attrs(doc, attrs_val, ns_map)