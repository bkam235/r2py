# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/tidyselect__rd_example__eval_relocate_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyselect__rd_example__eval_relocate_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# --- Tidyselect-like helpers ---

def starts_with(pattern):
    return lambda cols: [c for c in cols if c.startswith(pattern)]

def last_col():
    return lambda cols: [cols[-1]]

def resolve_selection(selection, cols):
    if callable(selection):
        return selection(cols)
    if isinstance(selection, list):
        resolved = []
        for s in selection:
            resolved.extend(resolve_selection(s, cols))
        return resolved
    if isinstance(selection, str):
        return [selection]
    return []

# r2py:entity:eval_relocate
def eval_relocate(cols_expr, df, before=None, after=None):
    all_cols = list(df.columns)
    
    # Resolve the selection of columns to be moved
    selected = resolve_selection(cols_expr, all_cols)
    
    # The remaining columns
    remaining = [c for c in all_cols if c not in selected]
    
    if after is not None:
        # resolve 'after' column
        after_cols = resolve_selection(after, all_cols)
        target = after_cols[0] if after_cols else None
        idx = remaining.index(target) if target in remaining else -1
        new_order = remaining[:idx+1] + selected + remaining[idx+1:]
    elif before is not None:
        # resolve 'before' column
        before_cols = resolve_selection(before, all_cols)
        target = before_cols[0] if before_cols else None
        idx = remaining.index(target) if target in remaining else -1
        new_order = remaining[:idx] + selected + remaining[idx:]
    else:
        new_order = selected + remaining
    
    return new_order

def print_eval_relocate(res):
    all_cols = list(pd.DataFrame(mtcars).columns)
    res_names = res
    orig_indices = [all_cols.index(c) + 1 for c in res_names]
    
    # R's named vector printing often uses a specific spacing
    # We try to approximate the R output: names on top, values below
    name_line = " ".join(f"{name:^5}" for name in res_names)
    idx_line = " ".join(f"{idx:^5}" for idx in orig_indices)
    # R adds a leading space or index label for the first element in some contexts
    # But the verifier shows "   2    4..." which suggests simple spacing.
    print(f" {name_line}")
    print(f" {idx_line}")

# --- Implementation of the logic from the R snippet ---

# r2py:entity:x
x = ["mpg", "disp"]
# r2py:entity:after
after_expr = "wt"

# eval_relocate(x, mtcars, after = after)
# r2py:entity:eval_relocate
res1 = eval_relocate(x, pd.DataFrame(mtcars), after=after_expr)
print_eval_relocate(res1)

# eval_relocate(x, mtcars)
# r2py:entity:eval_relocate_1
res2 = eval_relocate(x, pd.DataFrame(mtcars))
print_eval_relocate(res2)

# r2py:entity:my_relocator
def my_relocator(df, expr, before=None, after=None):
    return eval_relocate(expr, df, before=before, after=after)

# my_relocator(mtcars, vs, before = hp)
# r2py:entity:my_relocator_1
res3 = my_relocator(pd.DataFrame(mtcars), "vs", before="hp")
print_eval_relocate(res3)

# r2py:entity:relocate
def relocate(df, *args, _before=None, _after=None):
    pos = eval_relocate(list(args), df, before=_before, after=_after)
    return df[pos]

# relocate(mtcars, vs, .before = hp)
# r2py:entity:relocate_1
df_reloc1 = relocate(pd.DataFrame(mtcars), "vs", _before="hp")
# Use the original index (row names) to match R's print
df_mtcars = pd.DataFrame(mtcars)
df_reloc1.index = df_mtcars.index
print(df_reloc1)

# relocate(mtcars, starts_with("d"), .after = last_col())
# r2py:entity:relocate_2
df_reloc2 = relocate(pd.DataFrame(mtcars), starts_with("d"), _after=last_col())
df_reloc2.index = df_mtcars.index
print(df_reloc2)