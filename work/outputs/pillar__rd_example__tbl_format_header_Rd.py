# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/pillar__rd_example__tbl_format_header_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pillar__rd_example__tbl_format_header_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['penguins']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd

# Load the data into a DataFrame
df_penguins = pd.DataFrame(penguins)

# r2py:entity:setup
def tbl_format_setup(df):
    """
    Mimics pillar::tbl_format_setup by calculating basic metadata 
    about the dataframe for formatting.
    """
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'df': df
    }

# r2py:entity:tbl_format_header
def tbl_format_header(x, setup=None):
    """
    Mimics pillar::tbl_format_header by printing the tibble-style 
    header summary: '# A tibble: rows × cols'
    """
    if setup is None:
        # If only setup is passed (as in the second R call), 
        # we extract the info from the setup object.
        if isinstance(x, dict) and 'shape' in x:
            setup = x
        else:
            # Handle cases where the first arg is meant to be the setup
            setup = x
    else:
        # If both df and setup are passed, use the setup
        pass
        
    # Ensure we have the shape from the setup object
    if isinstance(setup, dict) and 'shape' in setup:
        rows, cols = setup['shape']
        header = f"# A tibble: {rows} × {cols}"
        return header
    return ""

# suppressPackageStartupMessages(library(pillar)) - No-op in Python

# setup <- tbl_format_setup(palmerpenguins::penguins)
# r2py:entity:setup
setup = tbl_format_setup(df_penguins)

# tbl_format_header(palmerpenguins::penguins, setup)
# r2py:entity:tbl_format_header
res1 = tbl_format_header(df_penguins, setup)
print(f"[1] \"{res1}\"")

# Shortcut for debugging: tbl_format_header(setup)
# The R output shows the call and then the result
print("<tbl_format_header(setup)>")
# r2py:entity:tbl_format_header_1
res2 = tbl_format_header(setup)
print(res2)