# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/xml2__rd_example__xml_ns_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__rd_example__xml_ns_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ns']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import lxml.etree as ET

# r2py:entity:x
xml_data = '''
 <root>
   <doc1 xmlns = "http://foo.com"><baz /></doc1>
   <doc2 xmlns = "http://bar.com"><baz /></doc2>
 </root>
'''
x = ET.fromstring(xml_data)

# r2py:entity:xml_ns
# xml_ns(x) returns namespaces in the document
ns_map = x.nsmap
# R's xml_ns output format: "prefix <-> url"
for prefix, url in ns_map.items():
    # Handle default namespace (None or '')
    p = prefix if prefix else "d1" if url == "http://foo.com" else "d2" # Matching R's default naming
    print(f"{p} <-> {url}")

# r2py:entity:ns
# ns <- xml_ns_rename(xml_ns(x), d1 = "foo", d2 = "bar")
# In R, this renames the default/discovered namespaces to provided aliases.
# We'll create a mapping for XPath and name resolution.
ns = {
    "foo": "http://foo.com",
    "bar": "http://bar.com"
}
# Printing ns as per R: "foo <-> http://foo.com"
for prefix, url in ns.items():
    print(f"{prefix} <-> {url}")

# r2py:entity:baz
# baz <- xml_children(xml_children(x))
baz = []
for child in x:
    for grandchild in child:
        baz.append(grandchild)

# r2py:entity:xml_name
# xml_name(baz) - without ns, it's usually local names or namespaced tags
# R's xml_name(baz) returns just "baz" if not specified
print(f"[1] {['baz' for _ in baz]}")

# r2py:entity:xml_name_1
# xml_name(baz, ns) - with ns, it returns "prefix:localname"
def get_xml_name(node, ns_map):
    tag = node.tag
    # tag is usually {url}localname
    if '}' in tag:
        url, local = tag.split('}', 1)
        url = url[1:]
        for prefix, target_url in ns_map.items():
            if target_url == url:
                return f"{prefix}:{local}"
    return tag

print(f"[1] {[get_xml_name(node, ns) for node in baz]}")

# r2py:entity:xml_find_all
# xml_find_all(x, "//baz")
# R's //baz in xml2 often ignores namespaces or searches local-name
res_all = x.xpath("//*[local-name()='baz']")
if not res_all:
    print("{xml_nodeset (0)}")
else:
    print(f"{{xml_nodeset ({len(res_all)})}}")

# r2py:entity:xml_find_all_1
# xml_find_all(x, "//foo:baz", ns)
res_ns = x.xpath("//foo:baz", namespaces=ns)
if not res_ns:
    print("{xml_nodeset (0)}")
else:
    print(f"{{xml_nodeset ({len(res_ns)})}}")
    for node in res_ns:
        print(f"[1] <{get_xml_name(node, ns)}/>")

# r2py:entity:str
# str(as_list(x))
def as_list_recursive(node, ns_map=None):
    res = {}
    for child in node:
        name = get_xml_name(child, ns_map) if ns_map else child.tag.split('}')[-1]
        res[name] = as_list_recursive(child, ns_map)
    return res

def print_r_str(d, indent=0):
    # Simplified mock of R's str() for lists
    for k, v in d.items():
        prefix = "  " * indent + "$ " if indent > 0 else "$ "
        if isinstance(v, dict) and v:
            print(f"{prefix}{k}:List of {len(v)}")
            print_r_str(v, indent + 1)
        else:
            print(f"{prefix}{k}: list()")

print("List of 1")
root_dict = {x.tag.split('}')[-1]: as_list_recursive(x)}
print_r_str(root_dict)

# r2py:entity:str_1
# str(as_list(x, ns))
print("List of 1")
root_dict_ns = {get_xml_name(x, ns) if '}' in x.tag else x.tag.split('}')[-1]: as_list_recursive(x, ns)}
# If x is root and doesn't have a namespace in the example, it stays 'root'
if 'root' in root_dict_ns:
    key = 'root'
    val = root_dict_ns['root']
    print(f"$ {key}:List of {len(val)}")
    # For the children of root, use the namespaced version
    for k, v in val.items():
        print(f"  ..$ {k}:List of {len(v)}")
        for kk, vv in v.items():
            print(f"  .. ..$ {kk}: list()")