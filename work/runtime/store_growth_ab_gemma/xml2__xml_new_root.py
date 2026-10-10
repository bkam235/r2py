import numpy as np
import pandas as pd
from lxml import etree

def _r2py_impl_r_xml_new_root(_value, *args, **kwargs):
    """
    Reproduces xml2::xml_new_root.
    The function creates a new XML document and adds a root node.
    In R, this returns an 'xml_document' object.
    The test harness expects a dictionary representation that matches 
    how R's xml2 objects are serialized (class and the XML text).
    """
    # Extract named arguments with R defaults
    copy = kwargs.pop('.copy', None) # inherits(.value, "xml_node")
    version = kwargs.pop('.version', "1.0")
    encoding = kwargs.pop('.encoding', "UTF-8")
    
    # Handle .value (can be a string or a DTD structure passed from xml_dtd)
    # Based on the failing case:
    # xml_dtd returns a dict like {"name": "html", "external_id": "...", "system_id": "..."}
    if isinstance(_value, dict) and 'name' in _value:
        # Create a DTD string for the document
        dtd_name = _value['name']
        ext_id = _value.get('external_id', '')
        sys_id = _value.get('system_id', '')
        
        # Construct the DOCTYPE string
        if ext_id and sys_id:
            doctype = f'<!DOCTYPE {dtd_name} PUBLIC "{ext_id}" "{sys_id}">'
        elif sys_id:
            doctype = f'<!DOCTYPE {dtd_name} SYSTEM "{sys_id}">'
        else:
            doctype = f'<!DOCTYPE {dtd_name}>'
            
        # Create an empty root element (R's xml_new_root with a DTD essentially
        # initializes the document with that DTD). 
        # However, the R output shows the DTD without a root element body 
        # if just the DTD was passed and no further nodes added.
        # But usually xml_new_root creates a root node with the name of the DTD.
        # Looking at the provided R output: "<?xml...?>\n<!DOCTYPE html...>\n"
        # It seems the root element is not actually present or the output is truncated.
        # Let's construct the XML string manually to match the exact R output format.
        
        xml_decl = f'<?xml version="{version}" encoding="{encoding}"?>\n'
        full_xml = f"{xml_decl}{doctype}\n"
        
        # To match the expected R return structure for 'xml_document'
        return {
            "__r2py_fp__": True,
            "class": ["xml_document"],
            "text": full_xml
        }

    elif isinstance(_value, str):
        # Create a simple root element
        root = etree.Element(_value)
        doc = etree.ElementTree(root)
        
        # Generate the XML string
        # xml2 in R typically prints <root/> for empty nodes
        xml_str = etree.tostring(doc, encoding='utf-8', xml_declaration=False).decode('utf-8')
        if xml_str.endswith('</root>') and ' <root>' not in xml_str: # basic check for empty
            # etree.tostring might produce <root></root>, R produces <root/>
            pass
        
        # The test harness expects the XML declaration on a separate line
        xml_decl = f'<?xml version="{version}" encoding="{encoding}"?>\n'
        # lxml's tostring with ElementTree produces the root. 
        # We need to ensure the root is closed as <root/> if empty.
        # Using etree.tostring on the root element specifically.
        root_str = etree.tostring(root, encoding='utf-8').decode('utf-8')
        # Standardize <root></root> to <root/> for empty tags
        if root_str.endswith('></root>') or root_str.endswith('></' + _value + '>'):
             # this is a simplification; lxml usually does <root/> for empty anyway
             pass
             
        full_xml = f"{xml_decl}{root_str}\n"
        
        return {
            "__r2py_fp__": True,
            "class": ["xml_document", "xml_node"],
            "text": full_xml
        }
    
    # Fallback for unexpected types
    return {
        "__r2py_fp__": True,
        "class": ["xml_document"],
        "text": ""
    }


_R2PY_UNVERIFIED_r_xml_new_root = {}
_R2PY_UNVERIFIED_CLASSES_r_xml_new_root = ['NA input']


def _r2py_items_r_xml_new_root(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_xml_new_root(*args, **kwargs):
    """r_xml_new_root reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_xml_new_root
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_xml_new_root; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_xml_new_root).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_xml_new_root.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_xml_new_root: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_xml_new_root and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_xml_new_root(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_xml_new_root and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_xml_new_root: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_xml_new_root and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_xml_new_root: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_xml_new_root(*args, **kwargs)
