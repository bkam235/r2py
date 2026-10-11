import numpy as np
import pandas as pd
from lxml import etree

def r_xml_new_root(_value, *args, **kwargs):
    """
    Python reproduction of xml2::xml_new_root.
    
    Returns an object that matches the serialization expected by the harness
    for an 'xml_document' (a dict with 'class' and 'text').
    """
    version = kwargs.get('.version', '1.0')
    encoding = kwargs.get('.encoding', 'UTF-8')
    
    # Handle NA values (converted to <NA/> in R's xml2)
    if _value is None or (isinstance(_value, float) and np.isnan(_value)):
        root_name = "NA"
    elif isinstance(_value, dict):
        # Handle the xml_dtd case: {"name": "...", "external_id": "...", "system_id": "..."}
        name = _value.get('name')
        ext_id = _value.get('external_id')
        sys_id = _value.get('system_id')
        
        # Construct the XML declaration and DOCTYPE string manually to match R's output
        # R's xml2 prints DOCTYPE as: <!DOCTYPE name PUBLIC "ext" "sys">
        xml_dec = f'<?xml version="{version}" encoding="{encoding}"?>\n'
        doctype = f'<!DOCTYPE {name} PUBLIC "{ext_id}" "{sys_id}">\n'
        text = xml_dec + doctype
        
        return {
            "__r2py_fp__": True,
            "class": ["xml_document"],
            "text": text
        }
    else:
        # Standard case: root is a character string
        root_name = str(_value)
        
    # Create an XML document with a root node
    root = etree.Element(root_name)
    # We use etree.tostring to get the XML content, then prepend the declaration
    # R's xml_new_root produces a document that, when serialized, includes the 
    # declaration and the root element.
    content = etree.tostring(root, encoding='utf-8').decode('utf-8')
    
    # R's serialization for xml_document includes a newline after the declaration 
    # and a newline after the root element.
    xml_dec = f'<?xml version="{version}" encoding="{encoding}"?>\n'
    # Since tostring of a single element doesn't add a trailing newline in some versions,
    # we ensure it matches R's pattern: <root/>\n
    if not content.endswith('\n'):
        content += '\n'
        
    text = xml_dec + content
    
    # Map the R class hierarchy: xml_document inherits from xml_node
    return {
        "__r2py_fp__": True,
        "class": ["xml_document", "xml_node"],
        "text": text
    }
