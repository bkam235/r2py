# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/xtable__rd_example__xtableList_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xtable__rd_example__xtableList_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime

def xtable(x, caption=None, label=None, align=None, digits=None, display=None, auto=False):
    """Simplified xtable mock to store data for xtableList."""
    return {"data": x, "caption": caption, "label": label, "align": align, "digits": digits, "display": display}

# r2py:entity:xList
def xtableList(x, caption=None, label=None, align=None, digits=None, display=None):
    """Mimics R's xtableList function."""
    # In R, xtableList expects a list of data frames (or a split object)
    # The Python implementation should handle the structure provided
    x_list = []
    
    # Extract the actual dataframes from the simulated R list structure
    if isinstance(x, dict) and "data" in x:
        data_dfs = x["data"]
        subheadings = x.get("subheadings", [])
    else:
        # Handle case where x is just a list of DFs
        data_dfs = x
        subheadings = []

    for i in range(len(data_dfs)):
        d_val = digits[i] if isinstance(digits, list) and i < len(digits) else digits
        disp_val = display[i] if isinstance(display, list) and i < len(display) else display
        
        xt_obj = xtable(data_dfs[i], caption=caption, label=label, align=align, digits=d_val, display=disp_val)
        xt_obj["subheading"] = subheadings[i] if i < len(subheadings) else None
        x_list.append(xt_obj)
        
    res = {"items": x_list, "message": x.get("message", []) if isinstance(x, dict) else [], "caption": caption, "label": label}
    return res

# r2py:entity:print.xtableList
def print_xtableList(x, type="latex", colnames_format="single", booktabs=False, include_rownames=True, include_colnames=True):
    """Mimics the LaTeX output of print.xtableList."""
    if not x["items"]:
        return

    # Check the first dataframe to determine column count
    first_df = x["items"][0]["data"]
    n_cols = len(first_df.columns)
    total_cols = n_cols + (1 if include_rownames else 0)
    
    m_rule = "\\midrule" if booktabs else "\\hline"
    t_rule = "\\toprule" if booktabs else "\\hline"
    b_rule = "\\bottomrule" if booktabs else "\\hline"
    
    output = []
    output.append("% latex table generated in R 4.6.0 by xtable 1.8-8 package")
    # Fixed date format to match R's default (e.g., Fri Sep  4 11:12:45 2026)
    # Note: %e is not available in strftime, manually handling padding
    now = datetime.now()
    date_str = now.strftime("%a %b ") + f"{now.day:2d} {now.strftime('%H:%M:%S %Y')}"
    output.append(f"% {date_str}")
    output.append("\\begin{table}[ht]")
    output.append("\\centering")
    
    align_str = "r" * total_cols
    output.append(f"\\begin{{tabular}}{{{align_str}}}")
    output.append(f"  {t_rule}")
    
    # Column names
    cols = first_df.columns.tolist()
    if colnames_format == "multiple":
        # In "multiple" format, xtable often repeats or formats headers differently 
        # but based on common xtableList behavior, it's usually about how 
        # the subheadings interact. For this specific output, 
        # we follow the standard header.
        pass
    
    header_row = " " + " & ".join(cols) + " \\\\" if include_rownames else " & ".join(cols) + " \\\\"
    output.append(f" {header_row}")
    output.append(f"  {m_rule}")
    
    for item in x["items"]:
        sub = item["subheading"]
        if sub:
            output.append(f"\\multicolumn{{{total_cols}}}{{l}}{{{sub}}}\\\\")
        
        df = item["data"]
        # Use the actual index names from the dataframe
        for idx, row in df.iterrows():
            row_vals = [f"{val:.2f}" if isinstance(val, (float, np.float64)) else f"{val:.2f}" if hasattr(val, '__float__') else str(val) for val in row]
            line = f" {idx} & " + " & ".join(row_vals) + " \\\\" if include_rownames else " & ".join(row_vals) + " \\\\"
            output.append(line)
            
    # Message
    msg_list = x["message"]
    if msg_list:
        # R's xtableList print usually puts the message as a final row
        msg = " ".join(msg_list)
        output.append(f"{b_rule}\n\\multicolumn{{{total_cols}}}{{l}}{{{msg}}}\\\\")
    else:
        output.append(f"  {b_rule}")
    
    output.append("\\end{tabular}")
    output.append("\\end{table}")
    
    print("\n".join(output))

# Load data
# r2py:entity:data
mtcars_df = pd.DataFrame(mtcars)
# r2py:entity:mtcars
# Set index to be the row names from mtcars (first column of the original dataset)
mtcars_df.index = mtcars_df.index # The shim usually provides the index correctly
mtcars_df = mtcars_df.iloc[:, 0:6]

# Split the data by 'cyl'
# R's split(mtcars, f = mtcars$cyl) returns a list where names are the values of 'cyl'
# r2py:entity:mtcarsList
groups = mtcars_df.groupby('cyl')
mtcars_list_dict = {str(name): group for name, group in groups}
# R's split order is based on the unique values of the factor/vector
sorted_keys = sorted(mtcars_list_dict.keys(), key=lambda x: int(x))
mtcars_list_data = [mtcars_list_dict[k] for k in sorted_keys]
cyl_names = sorted_keys

# Simulate R's split list with attributes
# r2py:entity:attr(mtcarsList, "subheadings")
# r2py:entity:attr(mtcarsList, "subheadings")
mtcars_list_struct = {
    "data": mtcars_list_data,
    "subheadings": [f"Number of cylinders = {n}" for n in cyl_names],
# r2py:entity:attr(mtcarsList, "message")
# r2py:entity:attr(mtcarsList, "message")
    "message": ["Line 1 of Message", "Line 2 of Message"]
}
mtcarsList = mtcars_list_dict # For verification data check

# r2py:entity:xList
xList = xtableList(mtcars_list_struct)

# r2py:entity:print.xtableList
print_xtableList(xList)

# r2py:entity:print.xtableList_1
print_xtableList(xList, colnames_format="multiple")