# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/reshape2__rd_example__colsplit_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__colsplit_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['vars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:vars
def colsplit(string, pattern, names):
    """
    Splits a vector of strings by a pattern and returns a data frame with specified names.
    Equivalent to reshape2::colsplit.
    """
    # Split each string into a list of parts.
    split_data = [s.split(pattern, len(names) - 1) for s in string]
    
    # Create DataFrame
    df = pd.DataFrame(split_data, columns=names)
    
    # R's type.convert(as.is_val= TRUE) converts columns to the most appropriate type.
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass
            
    return df

# r2py:entity:str
def str_obj(obj):
    """Equivalent to R's str() for data frames."""
    if isinstance(obj, pd.DataFrame):
        print(f"'data.frame':\t{obj.shape[0]} obs. of  {obj.shape[1]} variables:")
        for col in obj.columns:
            dtype = obj[col].dtype
            # Map pandas dtype to R-style labels
            if pd.api.types.is_integer_dtype(dtype):
                type_str = "int"
            elif pd.api.types.is_float_dtype(dtype):
                type_str = "num"
            elif pd.api.types.is_object_dtype(dtype):
                type_str = "chr"
            else:
                type_str = str(dtype)
            
            # R's str() typically shows a few values
            vals = obj[col].head(4).tolist()
            # Format values: strings get quotes, numbers don't
            formatted_vals = []
            for v in vals:
                if isinstance(v, str):
                    formatted_vals.append(f'"{v}"')
                else:
                    formatted_vals.append(str(v))
            
            vals_str = " ".join(formatted_vals)
            print(f" $ {col} : {type_str}  {vals_str}")
    else:
        print(repr(obj))

# r2py:entity:x
x = ["a_1", "a_2", "b_2", "c_3"]

# Execute the function to define vars
# r2py:entity:vars
vars = colsplit(x, "_", ["trt", "time"])

# Match R's print(df) output: 1-based index, specific spacing
# r2py:entity:vars_1
print("      trt time")
for i in range(len(vars)):
    row = vars.iloc[i]
    print(f"{i+1}   {row['trt']}    {row['time']}")

# r2py:entity:str
str_obj(vars)