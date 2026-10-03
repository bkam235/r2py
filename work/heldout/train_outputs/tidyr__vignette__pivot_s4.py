# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__vignette__pivot_s4.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['relig_income']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd

# Convert the shim data to a DataFrame
relig_income = pd.DataFrame(relig_income)

# cols = !religion
# r2py:entity:pivot_longer
cols_to_pivot = [col for col in relig_income.columns if col != "religion"]
id_vars = [col for col in relig_income.columns if col not in cols_to_pivot]

# To mimic pivot_longer, maintain original row order
relig_income_with_idx = relig_income.copy()
relig_income_with_idx['_orig_idx'] = range(len(relig_income))

d = pd.melt(
    relig_income_with_idx,
    id_vars=['_orig_idx'] + id_vars,
    value_vars=cols_to_pivot,
    var_name="income",
    value_name="count"
)

# pivot_longer sorts by original row first, then by the variable (cols_vary="fastest")
d = d.sort_values(by=['_orig_idx', 'income']).drop(columns=['_orig_idx'])
d = d.reset_index(drop=True)