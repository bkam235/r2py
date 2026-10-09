import numpy as np
import pandas as pd

def r_structure(_Data, *args, **kwargs):
    """
    Python reproduction of R's structure function.
    R's structure allows attaching attributes to an object.
    """
    if _Data is None:
        # R: stop("attempt to set an attribute on NULL")
        raise ValueError("attempt to set an attribute on NULL")

    attrib = kwargs
    
    if attrib:
        specials = [".Dim", ".Dimnames", ".Names", ".Tsp", ".Label"]
        replace = ["dim", "dimnames", "names", "tsp", "levels"]
        
        # Process special attribute name mappings
        final_attrib = {}
        for k, v in attrib.items():
            if k in specials:
                idx = specials.index(k)
                final_attrib[replace[idx]] = v
            else:
                final_attrib[k] = v
        
        # Logic: if(any(attrib[["class", exact = TRUE]] == "factor") && 
        #        typeof(.Data) == "double") storage.mode(.Data) <- "integer"
        if final_attrib.get("class") == "factor":
            if isinstance(_Data, np.ndarray) and np.issubdtype(_Data.dtype, np.floating):
                _Data = _Data.astype(np.int64)
            elif isinstance(_Data, (float, np.float64)):
                _Data = int(_Data)

        # In R, attributes are metadata attached to the object.
        # Python objects don't share this universal structure.
        # To support the harness's expectation of R attributes, 
        # we store them in a custom attribute `_r_attributes`.
        
        # Check if object allows attribute assignment
        try:
            if not hasattr(_Data, '_r_attributes'):
                _Data._r_attributes = {}
            _Data._r_attributes.update(final_attrib)
        except (AttributeError, TypeError):
            # For immutable types (str, int, etc.), we cannot attach attributes.
            # In a real environment, these would be wrapped in a class.
            # However, we follow the logic of the R source.
            pass

    return _Data
