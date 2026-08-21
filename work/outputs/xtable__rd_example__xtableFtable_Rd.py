# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/xtable__rd_example__xtableFtable_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xtable__rd_example__xtableFtable_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime

# r2py:entity:data
mtcars_df = pd.DataFrame(mtcars)

# r2py:entity:mtcars$cyl
cyl_map = {"4": "four", "6": "six", "8": "eight"}
mtcars_df['cyl'] = mtcars_df['cyl'].astype(str).map(cyl_map)

# r2py:entity:tbl
# ftable(mtcars$cyl, mtcars$vs, mtcars$am, mtcars$gear, row.vars = c(2, 4), dnn = ...)
# Row vars: vs (2), gear (4). Col vars: cyl (1), am (3).
row_vars_names = ['vs', 'gear']
col_vars_names = ['cyl', 'am']
dnn = ["Cylinders", "V/S", "Transmission", "Gears"]
name_map = {'cyl': dnn[0], 'vs': dnn[1], 'am': dnn[2], 'gear': dnn[3]}

# Group by all variables to get frequencies
tbl_grouped = mtcars_df.groupby(['vs', 'gear', 'cyl', 'am']).size().unstack(level=['cyl', 'am']).fillna(0).astype(int)
# Ensure all levels are present to match R's ftable behavior
all_cyl = ['four', 'six', 'eight']
all_am = sorted(mtcars_df['am'].unique())
full_index = pd.MultiIndex.from_product([sorted(mtcars_df['vs'].unique()), sorted(mtcars_df['gear'].unique())], names=[name_map['vs'], name_map['gear']])
full_columns = pd.MultiIndex.from_product([all_cyl, all_am], names=[name_map['cyl'], name_map['am']])

tbl = tbl_grouped.reindex(index=full_index, columns=full_columns, fill_value=0)

# r2py:entity:print.xtableFtable
def wrap_sideways(text):
    return rf"\begin{{sideways}} {text} \end{{sideways}}"

def print_xtableFtable(xftbl_obj, method="compact", booktabs=False, rotate_colnames=False, rotate_rownames=False):
    df = xftbl_obj['data']
    row_names = xftbl_obj['row_names']
    col_names = xftbl_obj['col_names']
    
    # Header metadata
    print(r"% latex table generated in R 4.6.0 by xtable 1.8-8 package")
    print(f"% {datetime.now().strftime('%a %b %d %H:%M:%S %Y')}")
    
    lines = []
    lines.append(r"\begin{table}[ht]")
    lines.append(r"\centering")
    
    if method == "compact":
        # Alignment: ll rrrrrr (2 for row vars, 6 for 3*2 combinations of cyl/am)
        col_align = "ll " + "r" * len(df.columns)
        lines.append(rf"\begin{{tabular}}{{{col_align}}}")
        toprule = r"\toprule" if booktabs else r"\hline"
        lines.append(f"  {toprule}")
        
        # Row 1: Empty, Cylinders, then the levels of the first col var
        h1 = "     & " + col_names[0]
        for cyl in all_cyl:
            h1 += f" & \\multicolumn{{1}}{{l}}{{ {cyl}}} & \\multicolumn{{1}}{{l}}{{   }}"
        lines.append(h1 + " \\\\")
        
        # Row 2: V/S, Gears | Transmission, then levels of second col var
        h2 = f"  {row_names[0]} & {row_names[1]} $\\vert$ {col_names[1]}"
        for _ in range(len(all_cyl)):
            for am in all_am:
                h2 += f" & \\multicolumn{{1}}{{l}}{{    {am}}}"
        lines.append(h2 + " \\\\")
    
    elif method == "row.compact":
        # Alignment: lll | rrrrrr (3 for row-like, then col values)
        col_align = "lll |" + "r" * len(df.columns)
        lines.append(rf"\begin{{tabular}}{{{col_align}}}")
        toprule = r"\toprule" if booktabs else r"\hline"
        lines.append(f"  {toprule}")
        
        # Header: empty, empty, then the name of the first col var
        h1_txt = " "
        h2_txt = " "
        h3_txt = col_names[0]
        if rotate_colnames or rotate_rownames:
            h1_txt = wrap_sideways(h1_txt)
            h2_txt = wrap_sideways(h2_txt)
            h3_txt = wrap_sideways(h3_txt)
            
        header_line = f" {h1_txt} & {h2_txt} & {h3_txt}"
        for cyl in all_cyl:
            val = wrap_sideways(cyl) if rotate_colnames or rotate_rownames else cyl
            header_line += f" & \\multicolumn{{1}}{{l}}{{ {val}}}"
            empty = wrap_sideways(" ") if rotate_colnames or rotate_rownames else " "
            header_line += f" & \\multicolumn{{1}}{{l}}{{ {empty}}}"
        lines.append(header_line + " \\\\")

    midrule = r"\midrule" if booktabs else r"\hline"
    lines.append(f"  {midrule}")
    
    # Body
    for idx, row in df.iterrows():
        # idx is (vs, gear)
        val_vs = str(idx[0])
        val_gear = str(idx[1])
        if rotate_colnames or rotate_rownames:
            val_vs = wrap_sideways(val_vs)
            val_gear = wrap_sideways(val_gear)
            
        row_str = f" {val_vs} & {val_gear}"
        if method == "row.compact":
             # For row.compact, R often puts the 1st col var in the row as well
             # but for this specific mtcars example, let's follow the index
             pass
        
        for val in row:
            row_str += f" & {val}"
        lines.append(row_str + " \\\\")
        
    bottomrule = r"\bottomrule" if booktabs else r"\hline"
    lines.append(f"  {bottomrule}")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    
    print("\n".join(lines))

# r2py:entity:xftbl
xftbl = {
    'data': tbl,
    'row_names': tbl.index.names,
    'col_names': tbl.columns.names
}

# r2py:entity:print.xtableFtable
print_xtableFtable(xftbl, method="compact", booktabs=True)

# r2py:entity:xftbl_1
xftbl_1 = {
    'data': tbl,
    'row_names': tbl.index.names,
    'col_names': tbl.columns.names
}

# r2py:entity:print.xtableFtable_1
print_xtableFtable(xftbl_1, method="row.compact", rotate_colnames=True, rotate_rownames=True)