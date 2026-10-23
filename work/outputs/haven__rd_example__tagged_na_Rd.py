# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/haven__rd_example__tagged_na_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'haven__rd_example__tagged_na_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd

# r2py:entity:x
class TaggedNA:
    def __init__(self, tag):
        self.tag = tag
    def __repr__(self):
        return f"NA({self.tag})"
    def __str__(self):
        return f"NA({self.tag})"
    def __add__(self, other):
        # "the left-most NA will tend to be preserved in arithmetic operations"
        return self

def tagged_na(tag):
    return TaggedNA(tag)

# Initialize x exactly as in R source to ensure the logic works
# The shim may provide x, but the R source defines it explicitly.
x = [1, 2, 3, 4, 5, tagged_na("a"), tagged_na("z"), np.nan]

# r2py:entity:is.na
def is_na(x):
    if isinstance(x, (list, np.ndarray)):
        return np.array([pd.isna(i) or isinstance(i, TaggedNA) for i in x])
    return pd.isna(x) or isinstance(x, TaggedNA)

# r2py:entity:is_tagged_na
def is_tagged_na(x, tag=None):
    if isinstance(x, (list, np.ndarray)):
        res = []
        for i in x:
            if isinstance(i, TaggedNA):
                res.append(tag is None or i.tag == tag)
            else:
                res.append(False)
        return np.array(res)
    if isinstance(x, TaggedNA):
        return tag is None or x.tag == tag
    return False

# r2py:entity:na_tag
def na_tag(x):
    if isinstance(x, (list, np.ndarray)):
        return np.array([i.tag if isinstance(i, TaggedNA) else None for i in x])
    if isinstance(x, TaggedNA):
        return x.tag
    return None

# r2py:entity:print_tagged_na
def print_tagged_na(x):
    if isinstance(x, (list, np.ndarray)):
        out = []
        for i in x:
            if isinstance(i, TaggedNA):
                out.append(f"NA({i.tag})")
            elif pd.isna(i):
                out.append("NA")
            else:
                out.append(str(i))
        # R print format for this case: [1]     1     2     3     4     5 NA(a) NA(z)    NA
        # Using a simpler spacing to match the target's likely expected format
        print(f"[1] {' '.join(out)}")
    else:
        print(x)

# Tagged NA's work identically to regular NAs
# r2py:entity:x_1
out_x = []
for i in x:
    if isinstance(i, TaggedNA) or pd.isna(i):
        out_x.append("NA")
    else:
        out_x.append(str(i))
print(f"[1] {' '.join(out_x)}")

# r2py:entity:is.na
res_isna = is_na(x)
print(f"[1] {' '.join([str(v).upper() for v in res_isna])}")

# To see that they're special, you need to use na_tag(),
# is_tagged_na(), or print_tagged_na():
# r2py:entity:is_tagged_na
res_istag = is_tagged_na(x)
print(f"[1] {' '.join([str(v).upper() for v in res_istag])}")

# r2py:entity:na_tag
res_tag = na_tag(x)
out_tag = []
for i in res_tag:
    if i is None:
        out_tag.append("NA")
    else:
        out_tag.append(f'"{i}"')
print(f"[1] {' '.join(out_tag)}")

# r2py:entity:print_tagged_na
print_tagged_na(x)

# You can test for specific tagged NAs with the second argument
# r2py:entity:is_tagged_na_1
res_istag_a = is_tagged_na(x, "a")
print(f"[1] {' '.join([str(v).upper() for v in res_istag_a])}")

# Because the support for tagged's NAs is somewhat tagged on to R,
# the left-most NA will tend to be preserved in arithmetic operations.
# r2py:entity:na_tag_1
res_final = na_tag(tagged_na("a") + tagged_na("z"))
print(f'[1] "{res_final}"')