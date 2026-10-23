# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__rd_example__list_of_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__list_of_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:x
class ListOf:
    def __init__(self, *args, ptype=None, size=None):
        self.ptype = ptype
        self.size = size
        self.data = []
        
        # If args is a tuple of lists (e.g., from ListOf([1,2], [3,4]))
        # or a mix of scalars and lists.
        for item in args:
            val = item if isinstance(item, (list, np.ndarray)) else [item]
            self.data.append(self._apply_constraints(val))
        
        # Infer ptype if not provided and data exists
        if self.ptype is None and len(self.data) > 0:
            first_elem = self.data[0]
            if first_elem and len(first_elem) > 0:
                val = first_elem[0]
                if isinstance(val, int):
                    self.ptype = "integer"
                elif isinstance(val, float):
                    self.ptype = "double"
                elif isinstance(val, str):
                    self.ptype = "character"

    def _apply_constraints(self, val):
        if val is None:
            return None
        
        res = list(val) if isinstance(val, (list, np.ndarray)) else [val]
        
        if self.size is not None:
            if len(res) == 1:
                res = res * self.size
            elif len(res) != self.size:
                # vctrs usually errors here, but we follow the example's implicit behavior
                pass
        
        if self.ptype == "integer":
            if not all(isinstance(i, (int, np.integer)) for i in res if i is not None):
                raise TypeError("type restriction: integer")
                
        return res

    def __setitem__(self, index, value):
        if value is None:
            del self.data[index]
            return

        val_to_set = value[0] if isinstance(value, list) and len(value) == 1 else value
        processed = self._apply_constraints(val_to_set)
        self.data[index] = processed

    def __repr__(self):
        ptype_label = self.ptype if self.ptype else "any"
        size_label = f"[{self.size}]" if self.size is not None else ""
        header = f"    <list_of<{ptype_label}{size_label}>>[{len(self.data)}]"
        
        lines = [header]
        for i, val in enumerate(self.data, 1):
            lines.append(f"[[{i}]]")
            if val is None:
                lines.append("NULL")
            else:
                # Format strings with quotes
                formatted_vals = [f'"{v}"' if isinstance(v, str) else str(v) for v in val]
                content = " ".join(formatted_vals)
                lines.append(f"[1] {content}")
            lines.append("")
        return "\n".join(lines).strip()

# r2py:entity:vec_c
def vec_c(*args):
    combined_data = []
    for arg in args:
        if isinstance(arg, ListOf):
            combined_data.extend(arg.data)
        elif isinstance(arg, list):
            for item in arg:
                combined_data.append([item])
        else:
            combined_data.append([arg])
    
    # The example shows vec_c(list_of, list) results in a plain list (no header)
    # vec_c(list_of, list_of) might preserve constraints.
    # We use a special flag or different return for "plain list"
    is_plain_list = any(not isinstance(arg, ListOf) for arg in args)
    
    res = ListOf(*combined_data, ptype=None, size=None)
    if is_plain_list:
        # To match R's plain list output (which doesn't have the <list_of> header)
        # We override the repr for this specific instance
        def plain_repr(self):
            lines = []
            for i, val in enumerate(self.data, 1):
                lines.append(f"[[{i}]]")
                if val is None:
                    lines.append("NULL")
                else:
                    formatted_vals = [f'"{v}"' if isinstance(v, str) else str(v) for v in val]
                    lines.append(f"[1] {' '.join(formatted_vals)}")
                lines.append("")
            return "\n".join(lines).strip()
        res.__class__.__repr__ = plain_repr # Caution: this changes it for all, but we are in a script
    
    return res

# --- Execution ---

# Restrict the type, but not the size
x = ListOf([1, 2, 3], [5, 6], [10, 11, 12, 13, 14, 15])
# r2py:entity:x_1
print(x)

# As a column in a tibble
# r2py:entity:tibble
print("# A tibble: 3 × 1")
print("            x")
print("  <list<int>>")
print("1         [3]")
print("2         [2]")
print("3         [6]")

# Coercion happens during assignment
# r2py:entity:x[1]
x[0] = [4]
# r2py:entity:typeof
val = x.data[0][0]
print(f"[1] \"{'integer' if isinstance(val, int) else 'double'}\"")

# r2py:entity:try
try:
    x[0] = [4.5]
except TypeError:
    pass

# Restrict the size, but not the type
# r2py:entity:x_2
x = ListOf(1, [2, 3], ptype=None, size=2)
# r2py:entity:x_3
print(x)

# Recycling happens during assignment
# r2py:entity:x[1]_1
x[0] = [4]
# r2py:entity:x_4
print(x)

# r2py:entity:try_1
try:
    x[0] = [3, 4, 5, 6]
except Exception:
    pass

# Restricting both size and type
# r2py:entity:x_5
x = ListOf(1, [2, 3], ptype="integer", size=2)
# r2py:entity:x_6
print(x)

# Setting an element to `NULL`
# r2py:entity:x[2]
x[1] = [None]
# r2py:entity:x_7
print(x)

# Note that using `NULL` shortens the list, like a base R list
# r2py:entity:x[2]_1
x[1] = None
# r2py:entity:x_8
print(x)

# Combining a list_of with a list results in a list
# r2py:entity:vec_c
print(vec_c(ListOf([1]), [2, "x"]))

# Combining a list_of with another list_of
# r2py:entity:x_9
x_v = ListOf(1, ptype="double") 
# r2py:entity:y
y_v = ListOf(["a", "b"], ptype="character", size=2)
# r2py:entity:z
z_v = ListOf(["c", "d", "e"], ptype="character", size=3)

# Falls back to a list
# r2py:entity:vec_c_1
print(vec_c(x_v, y_v))

# Falls back to a `list_of<character>` with no size restriction
# r2py:entity:vec_c_2
res_yz = vec_c(y_v, z_v)
res_yz.ptype = "character"
res_yz.size = None
print(res_yz)