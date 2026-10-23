# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/hardhat__rd_example__model_matrix_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hardhat__rd_example__model_matrix_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from typing import Any, Dict, Tuple, Optional, List

# r2py:entity:framed
def model_frame(formula: str, data: pd.DataFrame) -> Dict[str, Any]:
    """
    Simulates hardhat::model_frame.
    Returns a dict with 'data' (the frame) and 'terms'.
    Only keeps columns present in the RHS of the formula.
    """
    # Extract variables from the formula
    if '~' in formula:
        rhs = formula.split('~')[1].strip()
    else:
        rhs = formula.strip()
    
    # Simple extraction of column names (split by + or *)
    import re
    vars_found = re.findall(r'[a-zA-Z_][a-zA-Z0-9_.]*', rhs)
    
    df_frame = data[vars_found].copy() if vars_found else data.copy()
    return {'data': df_frame, 'terms': formula}

# r2py:entity:model_matrix
def model_matrix(terms: str, data: pd.DataFrame, contrasts_override: Optional[Any] = None) -> pd.DataFrame:
    """
    Simulates hardhat::model_matrix.
    Missing values never result in dropped rows.
    """
    # Simple formula parser for these examples
    if '~' not in terms:
        rhs = terms
    else:
        rhs = terms.split('~')[1].strip()
    
    # Determine contrast type
    contrast_type = 'treatment'
    if isinstance(contrasts_override, dict) and 'unordered' in contrasts_override:
        if contrasts_override['unordered'] == 'contr.sum':
            contrast_type = 'sum'
    elif isinstance(contrasts_override, list) and len(contrasts_override) > 0:
        if 'contr.sum' in contrasts_override:
            contrast_type = 'sum'

    # Variable extraction
    col_name = rhs
    if col_name not in data.columns:
        # Try to find the first valid column name if rhs is complex
        import re
        vars_found = re.findall(r'[a-zA-Z_][a-zA-Z0-9_.]*', rhs)
        if vars_found and vars_found[0] in data.columns:
            col_name = vars_found[0]
        else:
            # Fallback for empty/intercept-only formulas
            return pd.DataFrame({'(Intercept)': np.ones(len(data))})
    
    series = data[col_name]
    # Get unique values excluding NA for contrast levels
    all_levels = pd.Series(series).dropna().unique()
    # R's factor levels are typically sorted alphabetically if not specified
    all_levels = np.sort(all_levels)
    
    # Intercept
    res_cols = {'(Intercept)': np.ones(len(data))}
    
    if contrast_type == 'treatment':
        # Treatment: 1st level is baseline. Others get 1/0.
        for level in all_levels[1:]:
            col_name_final = f"{col_name}{level}"
            col = np.where(series == level, 1.0, 0.0)
            col[pd.isna(series)] = np.nan
            res_cols[col_name_final] = col
    elif contrast_type == 'sum':
        # Contr.sum for 2 levels is [1, -1]^T
        if len(all_levels) == 2:
            col_name_final = f"{col_name}1"
            col = np.where(series == all_levels[0], 1.0, 0.0)
            col = np.where(series == all_levels[1], -1.0, col)
            col[pd.isna(series)] = np.nan
            res_cols[col_name_final] = col
        else:
            # Simplified generic sum contrast
            for i in range(1, len(all_levels)):
                col_name_final = f"{col_name}{i}"
                col = np.zeros(len(data))
                for j, level in enumerate(all_levels):
                    val = 1.0 if j == i-1 else (-1.0 / (len(all_levels)-1) if j == len(all_levels)-1 else 0.0)
                    col[series == level] = val
                col[pd.isna(series)] = np.nan
                res_cols[col_name_final] = col

    return pd.DataFrame(res_cols)

# --- Main Execution ---

# 1. Basic usage
df_iris = pd.DataFrame(iris)
# r2py:entity:framed
framed = model_frame('Sepal.Width ~ Species', df_iris)
# r2py:entity:model_matrix
print(model_matrix(framed['terms'], framed['data']))

# 2. Missing values
# r2py:entity:iris2
iris2 = df_iris.copy()
# r2py:entity:iris2$Species[1]
iris2.loc[0, 'Species'] = np.nan
# r2py:entity:framed2
framed2 = model_frame('Sepal.Width ~ Species', iris2)
# r2py:entity:model_matrix_1
print(model_matrix(framed2['terms'], framed2['data']))

# 3. Contrasts
# r2py:entity:y
y = pd.Series(['a', 'b'])
# r2py:entity:x
x = pd.DataFrame({'y': y})
# r2py:entity:framed_1
framed_c = model_frame('~ y', x)
# r2py:entity:model_matrix_2
print(model_matrix(framed_c['terms'], framed_c['data']))

# Setting contrasts directly
# r2py:entity:y_with_contrast
y_with_contrast = y.copy()
# Simulated by passing the override to model_matrix
# r2py:entity:x2
x2 = pd.DataFrame({'y': y_with_contrast})
# r2py:entity:framed2_1
framed2_c = model_frame('~ y', x2)
# r2py:entity:model_matrix_3
print(model_matrix(framed2_c['terms'], framed2_c['data'], contrasts_override={'unordered': 'contr.sum'}))

# Global override
# r2py:entity:global_override
global_override = ['contr.sum', 'contr.poly'] 
# rlang::with_options simulation
# r2py:entity:model_matrix_4
_ = model_matrix(framed_c['terms'], framed_c['data'], contrasts_override=global_override)