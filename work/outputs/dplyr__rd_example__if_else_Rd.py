# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__if_else_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__if_else_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import random

# r2py:entity:if_else
def if_else(condition, true_val, false_val, missing=None):
    """
    Equivalent to dplyr::if_else.
    Strictly typed and handles NA values in condition.
    """
    cond = pd.Series(condition)
    
    # Convert values to Series for element-wise operation
    t_val = pd.Series(true_val) if isinstance(true_val, (list, np.ndarray, pd.Series)) else pd.Series([true_val] * len(cond))
    f_val = pd.Series(false_val) if isinstance(false_val, (list, np.ndarray, pd.Series)) else pd.Series([false_val] * len(cond))
    
    # R's if_else logic:
    # Result is true_val where condition is TRUE
    # Result is false_val where condition is FALSE
    # Result is 'missing' where condition is NA
    
    # We create a result series. We use object type to avoid casting issues with strings and NAs
    result = pd.Series(index=cond.index, dtype=object)
    
    # TRUE
    mask_true = cond == True
    result[mask_true] = t_val[mask_true]
    
    # FALSE
    mask_false = cond == False
    result[mask_false] = f_val[mask_false]
    
    # NA
    mask_na = cond.isna()
    if missing is not None:
        result[mask_na] = missing
    else:
        result[mask_na] = np.nan
            
    return result

# r2py:entity:ifelse
def ifelse(test, yes, no):
    """
    Equivalent to base::ifelse.
    Less strict about types than if_else.
    """
    test_ser = pd.Series(test)
    
    # R's ifelse logic:
    # result[test == TRUE] = yes
    # result[test == FALSE] = no
    # result[test == NA] = NA
    
    res = pd.Series(index=test_ser.index, dtype=object)
    
    mask_true = test_ser == True
    # Handle broadcasting for 'yes' and 'no'
    y_val = pd.Series(yes) if isinstance(yes, (list, np.ndarray, pd.Series)) else pd.Series([yes] * len(test_ser))
    n_val = pd.Series(no) if isinstance(no, (list, np.ndarray, pd.Series)) else pd.Series([no] * len(test_ser))
    
    res[mask_true] = y_val[mask_true]
    
    mask_false = test_ser == False
    res[mask_false] = n_val[mask_false]
    
    res[test_ser.isna()] = np.nan
    return res

# x <- c(-5:5, NA)
# r2py:entity:x
x = pd.Series(list(range(-5, 6)) + [np.nan])

# if_else(x < 0, NA, x)
# r2py:entity:if_else
res1 = if_else(x < 0, np.nan, x)
print(res1.values)

# if_else(x < 0, "negative", "positive", missing = "missing")
# r2py:entity:if_else_1
res2 = if_else(x < 0, "negative", "positive", missing="missing")
print(res2.values)

# x <- factor(sample(letters[1:5], 10, replace = TRUE))
# r2py:entity:x_1
sample_letters = letters[0:5] 
# To ensure reproducibility or match R's behavior, but here we use random.choice
x_sampled = [random.choice(sample_letters) for _ in range(10)]
x_factor = pd.Series(x_sampled).astype('category')

# ifelse(x %in% c("a", "b", "c"), x, NA)
# r2py:entity:ifelse
res3 = ifelse(x_factor.isin(["a", "b", "c"]), x_factor, np.nan)
print(res3.values)

# if_else(x %in% c("a", "b", "c"), x, NA)
# r2py:entity:if_else_2
res4 = if_else(x_factor.isin(["a", "b", "c"]), x_factor, np.nan)
print(res4.values)

# starwars |> mutate(category = if_else(height < 100, "short", "tall"), .keep = "used")
# r2py:entity:mutate
df_starwars = pd.DataFrame(starwars)
# .keep = "used" in R's mutate means keep only the columns used in the operation
# The operation uses 'height'
heights = df_starwars['height']
categories = if_else(heights < 100, "short", "tall")

# Result should contain 'height' and 'category'
res_mutate = pd.DataFrame({
    'height': heights,
    'category': categories
})
print(res_mutate.head(10))