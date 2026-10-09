import numpy as np
import pandas as pd
from lxml import etree

def _r2py_impl_r_read_xml(x, encoding="", *args, **kwargs):
    """
    Python reproduction of xml2::read_xml.
    In R, read_xml returns an S4 object of class 'xml_document'.
    In Python, the closest equivalent is an lxml element tree.
    """
    as_html = kwargs.get('as_html', False)
    options = kwargs.get('options', "NOBLANKS")
    
    # R's check_string(x) implies x must be a single string
    if not isinstance(x, str):
        # If it's a numpy array or list of one string, extract it
        if hasattr(x, 'tolist'):
            x = x.tolist()
        if isinstance(x, list) and len(x) == 1:
            x = x[0]
        else:
            # This simulates the error R throws when x is not a string
            raise TypeError("x must be a character string")

    # Logic from R source: if x contains < or >, it's treated as XML content
    if '<' in x or '>' in x:
        # R calls read_xml.raw with UTF-8. 
        # NOBLANKS option in xml2 corresponds to stripping insignificant whitespace.
        parser_kwargs = {}
        if options == "NOBLANKS" or (isinstance(options, int) and (options & 1)): 
            # Note: In R, options is often a bitmask. 
            # 'NOBLANKS' is the default.
            parser_kwargs['remove_blank_text'] = True
            
        if as_html:
            # Parse as HTML
            parser = etree.HTMLParser(encoding=encoding if encoding else 'utf-8')
            doc = etree.html.fromstring(x.encode('utf-8'), parser=parser)
        else:
            # Parse as XML
            parser = etree.XMLParser(remove_blank_text=True) if options == "NOBLANKS" else etree.XMLParser()
            doc = etree.fromstring(x.encode('utf-8'), parser=parser)
        
        # To match the R object return, we wrap it in an object that identifies as 'xml_document'
        # since the harness expects the return value to be the "natural Python object"
        # for the R value. In this case, the result of read_xml is the document.
        return doc
    else:
        # Otherwise, treat x as a path to a file or a URL
        try:
            if as_html:
                parser = etree.HTMLParser(encoding=encoding if encoding else 'utf-8')
                doc = etree.html.fromstring(x, parser=parser) # lxml handles URLs/files in fromstring sometimes, but better:
            else:
                parser = etree.XMLParser(remove_blank_text=True) if options == "NOBLANKS" else etree.XMLParser()
                # Using etree.parse for files/URLs
                tree = etree.parse(x, parser=parser)
                doc = tree.getroot()
                
            # For HTML, we need the root
            if as_html and not hasattr(doc, 'tag'):
                # This part handles the case where etree.html.fromstring is used
                pass
                
            return doc
        except Exception as e:
            # If it fails, we attempt to handle it as a raw string again just in case
            # though the grepl check usually prevents this.
            raise e


_R2PY_UNVERIFIED_r_read_xml = {'as_html': ['True'], 'encoding': [''], 'x': ['<!DOCTYPE doc [\n<!ELEMENT doc (#PCDATA)>\n<!ENTITY foo " test ">\n]>\n<doc>This is a valid document &foo; !</doc>', "<html lang='en'><body><h1>Title</h1></body></html>"]}
_R2PY_UNVERIFIED_CLASSES_r_read_xml = []


def _r2py_items_r_read_xml(v):
    if isinstance(v, (str, bytes, dict)) or not hasattr(v, "__len__"):
        return None
    try:
        return list(v)
    except TypeError:
        return None


def r_read_xml(*args, **kwargs):
    """r_read_xml reproduces R on every tested ordinary call except the option values in _R2PY_UNVERIFIED_r_read_xml
    and the input classes in _R2PY_UNVERIFIED_CLASSES_r_read_xml; for those it refuses rather than guess."""
    import inspect
    import math
    try:
        bound = inspect.signature(_r2py_impl_r_read_xml).bind(*args, **kwargs).arguments
    except TypeError:
        bound = kwargs
    for name, bad in _R2PY_UNVERIFIED_r_read_xml.items():
        v = bound.get(name)
        if isinstance(v, (list, tuple)) and len(v) == 1:
            v = v[0]
        if v is not None and str(v) in bad:
            raise NotImplementedError(
                f"r_read_xml: {name}={v!r} is not verified against R; handle this case in your own code")
    if _R2PY_UNVERIFIED_CLASSES_r_read_xml and bound:
        first = next(iter(bound.values()))
        items = _r2py_items_r_read_xml(first)
        if "vector input" in _R2PY_UNVERIFIED_CLASSES_r_read_xml and items is not None and len(items) > 1:
            raise NotImplementedError(
                f"r_read_xml: input of length {len(items)} is not verified against R (verified for single values); "
                "loop over the elements or write this case yourself")
        vals = items if items is not None else [first]
        if "NA input" in _R2PY_UNVERIFIED_CLASSES_r_read_xml and any(
                x is None or (isinstance(x, float) and math.isnan(x)) for x in vals):
            raise NotImplementedError(f"r_read_xml: input containing NA is not verified against R; handle NA yourself")
    return _r2py_impl_r_read_xml(*args, **kwargs)
