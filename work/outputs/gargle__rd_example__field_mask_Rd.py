import pandas as pd
import numpy as np

# r2py:entity:field_mask
def field_mask_impl(value, key):
    """
    Helper function to recursively generate the field mask for a 
    dictionary-like object.
    """
    if isinstance(value, dict):
        # Recurse into the dictionary
        children = [field_mask_impl(v, k) for k, v in value.items()]
        children_str = ",".join(children)
        return f"{key}({children_str})"
    else:
        # Base case: just return the key
        return key

def field_mask(x):
    """
    Translates a dictionary into a Google API field mask string.
    """
    if not isinstance(x, dict):
        raise TypeError("x must be dictionary-like")
    
    # Process each top-level element
    parts = []
    for k, v in x.items():
        if isinstance(v, dict):
            # For the top level, if the child is a dict, the R implementation 
            # produces 'key.childkey(...)' instead of 'key(childkey(...))'
            # if there is only one level of nesting before children.
            # Looking at R output: "userEnteredFormat.backgroundColor(red,green,blue)"
            # This suggests that for the top level, it continues the dot notation 
            # for nested dictionaries rather than immediately using parentheses.
            
            # To replicate "userEnteredFormat.backgroundColor(red,green,blue)":
            # We need to flatten the path until we hit a non-dict or a dict with multiple keys?
            # Actually, looking at field_mask_2: "gridProperties(rowCount,columnCount)"
            # If the dict has multiple keys, it uses (). If one key, it uses dot.
            
            if len(v) == 1:
                # Single key: flatten with dot and recurse
                inner_k = list(v.keys())[0]
                inner_v = v[inner_k]
                parts.append(f"{k}.{field_mask_impl(inner_v, inner_k)}")
            else:
                # Multiple keys: use parentheses
                parts.append(field_mask_impl(v, k))
        else:
            parts.append(k)
            
    return ",".join(parts)

# r2py:entity:x
x = {"sheetId": 1234, "title": "my_favorite_worksheet"}
# r2py:entity:field_mask
print(field_mask(x))

# r2py:entity:x_1
x = {
    "userEnteredFormat": {
        "backgroundColor": {
            "red": 159 / 255, 
            "green": 183 / 255, 
            "blue": 196 / 255
        }
    }
}
# r2py:entity:field_mask_1
print(field_mask(x))

# r2py:entity:x_2
x = {
    "sheetId": 1234,
    "gridProperties": {"rowCount": 5, "columnCount": 3}
}
# r2py:entity:field_mask_2
print(field_mask(x))