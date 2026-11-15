# Translated from <R script> by r2py v0.3.0
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/xml2__rd_example__xml_attr_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__rd_example__xml_attr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['kids']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:suppressPackageStartupMessages
import lxml.etree as ET


def _r_repr_na(v):
    return "NA" if v is None else str(v)


def print_vec(v):
    if v is None:
        print("[1] NA")
        return
    if isinstance(v, bool):
        print("[1] " + ("TRUE" if v else "FALSE"))
        return
    if isinstance(v, str):
        print('[1] "' + v + '"')
        return
    items = list(v)
    toks = []
    for i in items:
        if i is None:
            toks.append(("NA", False))
        elif isinstance(i, bool):
            toks.append(("TRUE" if i else "FALSE", True))
        else:
            toks.append(('"' + str(i) + '"', False))
    if not toks:
        print("character(0)")
        return
    width = max(len(s) for s, _ in toks)
    out = []
    for s, isbool in toks:
        out.append(s.rjust(width) if isbool else s.ljust(width))
    print("[1] " + " ".join(out))


def _print_named(pl):
    if not pl:
        print("named list()")
        return
    names = [str(k) for k, v in pl]
    vals = ['"' + v + '"' for k, v in pl]
    w = max(max(len(n) for n in names), max(len(v) for v in vals))
    print(" ".join(n.rjust(w) for n in names) + " ")
    print(" ".join(v.rjust(w) for v in vals) + " ")


def print_attrs(a):
    if a and isinstance(a[0], list):
        for i, pl in enumerate(a, start=1):
            print("[[%d]]" % i)
            _print_named(pl)
            print()
        return
    _print_named(a)


# r2py:entity:xml_children
def xml_children(x):
    return list(x)


def _local_name(k):
    if k.startswith('{'):
        return k.split('}', 1)[1]
    if ':' in k:
        return k.split(':', 1)[1]
    return k


def _qname(attr, ns):
    if isinstance(ns, dict) and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            return "{%s}%s" % (ns[prefix], local)
    return None


def xml_attr(x, attr, ns=None, default=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns, default) for node in x]
    has_ns = bool(ns)
    if ':' in attr and has_ns:
        q = _qname(attr, ns)
        if q is not None:
            val = x.get(q)
            if val is not None:
                return val
        val = x.get(attr)
        if val is not None:
            return val
        return default
    if has_ns:
        return x.get(attr, default)
    for k, v in x.attrib.items():
        if _local_name(k) == attr:
            return v
    return default


def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    out = []
    if ns:
        inv = {v: k for k, v in ns.items()}
        for k, v in x.attrib.items():
            if k.startswith('{'):
                url, local = k[1:].split('}', 1)
                pre = inv.get(url)
                out.append((("%s:%s" % (pre, local)) if pre else local, v))
            else:
                out.append((k, v))
    else:
        for k, v in x.attrib.items():
            out.append((_local_name(k), v))
    return out


def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None


def xml_set_attr(x, attr, value, ns=None):
    target_attr = attr
    q = _qname(attr, ns)
    if q is not None:
        target_attr = q
    x.set(target_attr, value)


def xml_set_attrs(x, value, ns=None):
    for attr, val in value.items():
        xml_set_attr(x, attr, val, ns)


# r2py:entity:import_xml2
# xml2 functionality provided above via lxml.etree

# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

# r2py:entity:xml_attr
print_vec(xml_attr(x, "id"))

# r2py:entity:xml_attr_1
print_vec(xml_attr(x, "apple"))

# r2py:entity:xml_attrs
print_attrs(xml_attrs(x))

# r2py:entity:kids
_kids_elems = xml_children(x)
kids = [{'__r2py_fp__': True,
         'class': ['xml_node'],
         'text': ET.tostring(e, encoding='unicode').strip()} for e in _kids_elems]

# r2py:entity:kids_1
print("{xml_nodeset (%d)}" % len(_kids_elems))
for _i, _k in enumerate(_kids_elems, start=1):
    print("[%d] %s" % (_i, ET.tostring(_k, encoding='unicode').strip()))

# r2py:entity:xml_attr_2
print_vec(xml_attr(_kids_elems, "id"))

# r2py:entity:xml_has_attr
print_vec(xml_has_attr(_kids_elems, "id"))

# r2py:entity:xml_attrs_1
print_attrs(xml_attrs(_kids_elems))

# r2py:entity:xml_attr_3
print_vec(xml_attr(xml_children(x), "d"))

# r2py:entity:xml_has_attr_1
print_vec(xml_has_attr(xml_children(x), "d"))

# r2py:entity:x_1
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')

# r2py:entity:doc
doc = xml_children(x)[0]

# r2py:entity:ns
ns_map = {k: v for k, v in x.nsmap.items() if k is not None}
ns = [v for k, v in x.nsmap.items() if k is not None]

# r2py:entity:xml_attrs_2
print_attrs(xml_attrs(doc))

# r2py:entity:xml_attrs_3
print_attrs(xml_attrs(doc, ns_map))

# r2py:entity:xml_attr_4
print_vec(xml_attr(doc, "id"))

# r2py:entity:xml_attr_5
print_vec(xml_attr(doc, "b:id", ns_map))

# r2py:entity:xml_attr_6
print_vec(xml_attr(doc, "id", ns_map))

# r2py:entity:xml_attr(doc, "id")
xml_set_attr(doc, "id", "one")

# r2py:entity:xml_set_attr
xml_set_attr(doc, "id", "two")

# r2py:entity:xml_attrs(doc)
xml_set_attrs(doc, {"b:id": "one", "f:id": "two", "id": "three"}, ns_map)

# r2py:entity:xml_set_attrs
xml_set_attrs(doc, {"b:id": "one", "f:id": "two", "id": "three"}, ns_map)