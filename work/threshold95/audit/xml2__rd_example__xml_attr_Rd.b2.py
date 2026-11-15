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

import re
import lxml.etree as ET


# ---------------------------------------------------------------------------
# R-like console printing helpers
# ---------------------------------------------------------------------------
def _r_val(v):
    if v is None:
        return 'NA'
    if isinstance(v, bool):
        return 'TRUE' if v else 'FALSE'
    if isinstance(v, (int, float)):
        return repr(v)
    return '"%s"' % v


def _r_vec_line(vals):
    strs = [_r_val(v) for v in vals]
    w = max(len(s) for s in strs)
    is_text = all(v is None or isinstance(v, str) for v in vals)
    if is_text:
        return '[1] ' + ' '.join(s.ljust(w) for s in strs)
    return '[1] ' + ' '.join(s.rjust(w) for s in strs)


def _r_named_print(d):
    pairs = getattr(d, 'pairs', None)
    if pairs is None:
        pairs = list(d.items())
    names = [p[0] for p in pairs]
    vals = [_r_val(p[1]) for p in pairs]
    w = max([len(n) for n in names] + [len(s) for s in vals])
    print(' '.join(n.rjust(w) for n in names) + ' ')
    print(' '.join(s.rjust(w) for s in vals) + ' ')


def xml_text_of(el):
    s = ET.tostring(el, encoding='unicode', with_tail=False)
    s = re.sub(r'\s+xmlns(:\w+)?="[^"]*"', '', s)
    return s.strip()


def _node_fp(el):
    return {'__r2py_fp__': True, 'class': ['xml_node'], 'text': xml_text_of(el)}


def r_print(v):
    if isinstance(v, ET._Element):
        print('{xml_node}')
        print(xml_text_of(v))
    elif isinstance(v, list) and len(v) > 0 and all(isinstance(e, ET._Element) for e in v):
        print('{xml_nodeset (%d)}' % len(v))
        for i, e in enumerate(v, 1):
            print('[%d] %s' % (i, xml_text_of(e)))
    elif isinstance(v, dict):
        _r_named_print(v)
    elif isinstance(v, list) and len(v) > 0 and all(isinstance(e, dict) for e in v):
        n = len(v)
        for i, d in enumerate(v, 1):
            print('[[%d]]' % i)
            _r_named_print(d)
            if i < n:
                print()
    elif isinstance(v, list):
        print(_r_vec_line(v))
    else:
        print(_r_vec_line([v]))


# ---------------------------------------------------------------------------
# xml2 equivalents built on lxml
# ---------------------------------------------------------------------------
class RAttrs(dict):
    """dict-like named character vector that remembers duplicates/order."""

    def __init__(self, pairs):
        super().__init__()
        self.pairs = list(pairs)
        for k, v in self.pairs:
            if k not in self:
                self[k] = v


def _ns_prefixes(el):
    m = {}
    for k, v in el.nsmap.items():
        if k is not None:
            m[v] = k
    return m


def _local_name(key):
    if key.startswith('{'):
        return key[1:].split('}', 1)[1]
    return key


# r2py:entity:xml_attr
def xml_attr(x, attr, ns=None, default=None):
    if isinstance(x, list):
        return [xml_attr(node, attr, ns, default) for node in x]

    has_ns = isinstance(ns, dict) and len(ns) > 0

    if has_ns:
        if ':' in attr:
            prefix, local = attr.split(':', 1)
            if prefix in ns:
                val = x.get('{%s}%s' % (ns[prefix], local))
                if val is not None:
                    return val
            return default
        val = x.get(attr)
        return val if val is not None else default

    # No ns supplied: match on the local attribute name, first match in order
    for key, v in x.attrib.items():
        if _local_name(key) == attr:
            return v
    return default


# r2py:entity:xml_attrs
def xml_attrs(x, ns=None):
    if isinstance(x, list):
        return [xml_attrs(node, ns) for node in x]
    has_ns = isinstance(ns, dict) and len(ns) > 0
    if not has_ns:
        # Without a namespace spec xml2 resolves names by local name, and
        # unqualified attributes fall back to the first namespaced match.
        first_by_local = {}
        for k, v in x.attrib.items():
            if k.startswith('{'):
                loc = _local_name(k)
                if loc not in first_by_local:
                    first_by_local[loc] = v
        pairs = []
        for k, v in x.attrib.items():
            loc = _local_name(k)
            if not k.startswith('{') and loc in first_by_local:
                pairs.append((loc, first_by_local[loc]))
            else:
                pairs.append((loc, v))
        return RAttrs(pairs)
    prefixes = _ns_prefixes(x)
    pairs = []
    for k, v in x.attrib.items():
        if k.startswith('{'):
            url, local = k[1:].split('}', 1)
            prefix = prefixes.get(url)
            name = '%s:%s' % (prefix, local) if prefix else local
        else:
            name = k
        pairs.append((name, v))
    return RAttrs(pairs)


# r2py:entity:xml_children
def xml_children(x):
    if isinstance(x, list):
        out = []
        for node in x:
            out.extend(list(node))
        return out
    return list(x)


# r2py:entity:xml_has_attr
def xml_has_attr(x, attr, ns=None):
    if isinstance(x, list):
        return [xml_has_attr(node, attr, ns) for node in x]
    return xml_attr(x, attr, ns) is not None


# r2py:entity:xml_set_attr
def xml_set_attr(x, attr, value, ns=None):
    if isinstance(x, list):
        for node in x:
            xml_set_attr(node, attr, value, ns)
        return
    target = attr
    if isinstance(ns, dict) and len(ns) > 0 and ':' in attr:
        prefix, local = attr.split(':', 1)
        if prefix in ns:
            target = '{%s}%s' % (ns[prefix], local)
    x.set(target, value)


# r2py:entity:xml_set_attrs
def xml_set_attrs(x, value, ns=None):
    if isinstance(x, list):
        for node in x:
            xml_set_attrs(node, value, ns)
        return
    for attr, val in value.items():
        xml_set_attr(x, attr, val, ns)


# ---------------------------------------------------------------------------
# Main script
# ---------------------------------------------------------------------------
# r2py:entity:x
x = ET.fromstring("<root id='1'><child id ='a' /><child id='b' d='b'/></root>")

# r2py:entity:xml_attr
xml_attr_res1 = xml_attr(x, "id"); r_print(xml_attr_res1)
# r2py:entity:xml_attr_1
xml_attr_res2 = xml_attr(x, "apple"); r_print(xml_attr_res2)
# r2py:entity:xml_attrs
xml_attrs_res1 = xml_attrs(x); r_print(xml_attrs_res1)

# r2py:entity:kids
_kids_els = xml_children(x)
kids = [_node_fp(e) for e in _kids_els]
# r2py:entity:kids_1
kids_1 = kids
r_print(_kids_els)
# r2py:entity:xml_attr_2
xml_attr_kids = xml_attr(_kids_els, "id"); r_print(xml_attr_kids)
# r2py:entity:xml_has_attr
xml_has_attr_kids = xml_has_attr(_kids_els, "id"); r_print(xml_has_attr_kids)
# r2py:entity:xml_attrs_1
xml_attrs_kids = xml_attrs(_kids_els); r_print(xml_attrs_kids)

# Missing attributes
# r2py:entity:xml_attr_3
xml_attr_missing = xml_attr(_kids_els, "d"); r_print(xml_attr_missing)
# r2py:entity:xml_has_attr_1
xml_has_attr_missing = xml_has_attr(_kids_els, "d"); r_print(xml_has_attr_missing)

# Namespace example
# r2py:entity:x_1
x = ET.fromstring('''
 <root xmlns:b="http://bar.com" xmlns:f="http://foo.com">
   <doc b:id="b" f:id="f" id="" />
 </root>
''')
# r2py:entity:doc
_doc_el = xml_children(x)[0]
_doc_el.tail = None
doc = _node_fp(_doc_el)

# r2py:entity:ns
ns_map = x.nsmap.copy()
if None in ns_map:
    del ns_map[None]
ns = list(ns_map.values())

# r2py:entity:xml_attrs_2
xml_attrs_doc1 = xml_attrs(_doc_el); r_print(xml_attrs_doc1)
# r2py:entity:xml_attrs_3
xml_attrs_doc2 = xml_attrs(_doc_el, ns_map); r_print(xml_attrs_doc2)

# Attribute access
# r2py:entity:xml_attr_4
xml_attr_doc_id = xml_attr(_doc_el, "id"); r_print(xml_attr_doc_id)
# r2py:entity:xml_attr_5
xml_attr_doc_bid = xml_attr(_doc_el, "b:id", ns_map); r_print(xml_attr_doc_bid)
# r2py:entity:xml_attr_6
xml_attr_doc_id_ns = xml_attr(_doc_el, "id", ns_map); r_print(xml_attr_doc_id_ns)

# Set attributes
# r2py:entity:xml_attr(doc, "id")
# r2py:entity:xml_set_attr
xml_set_attr(_doc_el, "id", "one") # xml_attr(doc, "id") <- "one"
xml_set_attr(_doc_el, "id", "two")

# Set multiple attributes
# r2py:entity:xml_attrs(doc)
attrs_val = {"b:id": "one", "f:id": "two", "id": "three"}
# r2py:entity:xml_set_attrs
xml_set_attrs(_doc_el, attrs_val, ns_map)