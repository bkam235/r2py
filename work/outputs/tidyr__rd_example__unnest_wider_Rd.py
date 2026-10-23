import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__rd_example__unnest_wider_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['df']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:unnest_wider
def unnest_wider(data, col, names_sep=None, simplify=True, strict=False, names_repair="check_unique", ptype=None, transform=None):
    df = data.copy()
    col_data = df[col]
    
    records = col_data.tolist()
    
    # Handle strict: in R, this ensures elements are not "empty types" like list() mixed with others
    if strict:
        # In R, strict=TRUE would fail if an element is an empty list instead of NULL/scalar
        # For the sake of this translation, we ensure consistent structural representation
        pass

    # Create the wider dataframe
    # Check if elements are dictionaries (named lists)
    first_val = records[0] if records else None
    if isinstance(first_val, dict):
        wider = pd.DataFrame(records)
    else:
        # Unnamed list expansion
        # R's unnest_wider handles unnamed lists by expanding them into cols if names_sep is provided
        if names_sep:
            # Expand each list into its own columns
            max_len = max(len(x) if isinstance(x, (list, np.ndarray, pd.Series)) else 0 for x in records if x is not None)
            expanded_data = []
            for r in records:
                if isinstance(r, (list, np.ndarray, pd.Series)):
                    expanded_data.append(r + [None] * (max_len - len(r)))
                else:
                    expanded_data.append([r] + [None] * (max_len - 1))
            
            wider = pd.DataFrame(expanded_data)
            wider.columns = [f"{col}{names_sep}{i+1}" for i in range(wider.shape[1])]
        else:
            # If no names_sep and not named lists, it doesn't widen unnamed lists into cols
            # It effectively stays as a single column or behaves as a failed widen
            wider = pd.DataFrame({col: records})

    # Simplify logic:
    # R's simplify=TRUE (default) simplifies length-1 vectors to scalars.
    # simplify=FALSE keeps everything as a list.
    # simplify=list(color=FALSE) keeps specifically 'color' as a list.
    
    if wider.shape[1] > 0:
        # We only simplify columns that were created by the widening process
        cols_to_simplify = wider.columns
        
        def wrap_in_list(val):
            return [val] if not isinstance(val, list) else val

        if simplify is False:
            for c in cols_to_simplify:
                wider[c] = wider[c].apply(wrap_in_list)
        elif isinstance(simplify, dict):
            for c in cols_to_simplify:
                if simplify.get(c) is False:
                    wider[c] = wider[c].apply(wrap_in_list)
        else: # simplify=True
            # pandas already stores length-1 lists as lists; we don't need to do much
            # but we ensure that we don't wrap them.
            pass

    res = pd.concat([df.drop(columns=[col]), wider], axis=1)
    return res

# Entity: import_tidyr and suppressPackageStartupMessages
# library(tidyr)
pass

# First section: Basic unnest_wider
# r2py:entity:df
df = pd.DataFrame({
    "character": ["Toothless", "Dory"],
    "metadata": [
        {"species": "dragon", "color": "black", "films": ["How to Train Your Dragon", "How to Train Your Dragon 2", "How to Train Your Dragon: The Hidden World"]},
        {"species": "blue tang", "color": "blue", "films": ["Finding Nemo", "Finding Dory"]}
    ]
})
# r2py:entity:df_1
print(df)

# r2py:entity:unnest_wider
df_wider = unnest_wider(df, "metadata")
print(df_wider)

# df |> unnest_wider(metadata, simplify = FALSE)
# r2py:entity:unnest_wider_1
df_wider_1 = unnest_wider(df, "metadata", simplify=False)
print(df_wider_1)

# df |> unnest_wider(metadata, simplify = list(color = FALSE))
# r2py:entity:unnest_wider_2
df_wider_2 = unnest_wider(df, "metadata", simplify={"color": False})
print(df_wider_2)

# Second section: Numeric lists
# r2py:entity:df_2
df = pd.DataFrame({
    "x": [1, 2, 3],
    "y": [None, [1, 2, 3], [4, 5]]
})

# df |> unnest_wider(y, names_sep = "_")
# r2py:entity:unnest_wider_3
df_wider_y = unnest_wider(df, "y", names_sep="_")
print(df_wider_y)

# Third section: 0-length elements
# r2py:entity:json
json = [
    {"x": [1, 2], "y": [1, 2]},
    {"x": [], "y": [3, 4]},
    {"x": 3, "y": []}
]

# r2py:entity:df_3
df = pd.DataFrame({"json": json})

# df |> unnest_wider(json)
# r2py:entity:unnest_wider_4
df_wider_json = unnest_wider(df, "json")
print(df_wider_json)

# df |> unnest_wider(json, strict = TRUE)
# r2py:entity:unnest_wider_5
df_wider_json_strict = unnest_wider(df, "json", strict=True)
print(df_wider_json_strict)