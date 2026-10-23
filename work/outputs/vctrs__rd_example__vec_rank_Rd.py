import pandas as pd
import numpy as np
from scipy import stats

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__vec_rank_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['df']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:vec_rank
def vec_rank(x, ties="min", incomplete="rank", direction="asc", na_value="largest", nan_distinct=False):
    if isinstance(x, pd.DataFrame):
        # Lexicographical rank for data frames
        # R's vec_rank(df) ranks rows based on columns in order
        # We use pandas' rank with a trick: sort by all columns, then rank the resulting sequence
        sorted_df = x.sort_values(by=x.columns.tolist())
        
        # To implement 'min' rank on lexicographical order:
        # We identify groups of identical rows
        # In this specific case, the R example uses default ties="min"
        # For a DataFrame, we can use a temporary column for the order
        # Since we need to return the ranks in the original order:
        
        # 1. Sort and track original index
        orig_idx = x.index
        sorted_x = x.sort_values(by=x.columns.tolist())
        
        # 2. Create a rank for the sorted rows
        # We can use a helper to treat the row as a single entity
        # For ties="min", we identify duplicate rows
        # We'll use a temporary series that identifies unique rows
        unique_rows = sorted_x.duplicated(keep='first')
        
        # The rank of the first instance of a unique row is its position
        # but we need to handle the 'min' logic.
        # Let's use a more robust way: create a string representation or tuple
        row_tuples = [tuple(row) for row in sorted_x.values]
        
        # Now rank the tuples
        ranks = []
        current_rank = 1
        for i in range(len(row_tuples)):
            if i > 0 and row_tuples[i] == row_tuples[i-1]:
                ranks.append(current_rank)
            else:
                # The rank is the index of the first occurrence + 1
                # But since it's sorted, it's just i + 1
                current_rank = i + 1
                ranks.append(current_rank)
        
        # Now map these ranks back to original indices
        result_series = pd.Series(ranks, index=sorted_x.index)
        return result_series.reindex(orig_idx).values

    # Handle vector-like inputs
    arr = np.asanyarray(x, dtype=float)
    
    # Direction handling
    if direction == "desc":
        # To rank descending, we flip the values
        # but we must handle NaNs carefully
        # R's vec_rank(direction="desc") effectively treats values as -x
        work_arr = -arr
    else:
        work_arr = arr.copy()

    # NA value handling
    # R's "largest" means NA is treated as +inf, "smallest" as -inf
    if na_value == "largest":
        work_arr = np.where(np.isnan(work_arr), np.inf, work_arr)
    elif na_value == "smallest":
        work_arr = np.where(np.isnan(work_arr), -np.inf, work_arr)

    # nan_distinct handling
    # If nan_distinct=True, each NaN gets its own unique rank
    if nan_distinct:
        nan_mask = np.isnan(arr)
        # We need to ensure NaNs are ranked separately.
        # We replace NaNs with values slightly larger than the max
        # to preserve the 'largest' logic while making them unique.
        nan_indices = np.where(nan_mask)[0]
        if len(nan_indices) > 0:
            fill_start = np.nanmax(work_arr) + 1 if not np.all(np.isnan(work_arr)) else 0
            # Add small increments to make them distinct
            for idx, nan_idx in enumerate(nan_indices):
                work_arr[nan_idx] = fill_start + idx

    # Ties handling
    if ties == "min":
        method = "min"
    elif ties == "max":
        method = "max"
    elif ties == "sequential":
        method = "ordinal"
    elif ties == "dense":
        method = "dense"
    else:
        method = "min"

    ranks = stats.rankdata(work_arr, method=method)
    
    # Incomplete handling
    if incomplete == "na":
        # Return NaN for any original NaN input
        return np.where(np.isnan(arr), np.nan, ranks)
    
    return ranks

# x <- c(5L, 6L, 3L, 3L, 5L, 3L)
# r2py:entity:x
x = np.array([5, 6, 3, 3, 5, 3])

# vec_rank(x, ties = "min")
# r2py:entity:vec_rank
print(vec_rank(x, ties="min"))

# vec_rank(x, ties = "max")
# r2py:entity:vec_rank_1
print(vec_rank(x, ties="max"))

# vec_rank(x, ties = "sequential")
# r2py:entity:vec_rank_2
print(vec_rank(x, ties="sequential"))

# vec_rank(x, ties = "dense")
# r2py:entity:vec_rank_3
print(vec_rank(x, ties="dense"))

# y <- c(NA, x, NA, NaN)
# R's c(NA, x, NA, NaN) result: [NA, 5, 6, 3, 3, 5, 3, NA, NaN]
# r2py:entity:y
y = np.array([np.nan, 5, 6, 3, 3, 5, 3, np.nan, np.nan])

# vec_rank(y, na_value = "largest")
# r2py:entity:vec_rank_4
print(vec_rank(y, na_value="largest"))

# vec_rank(y, na_value = "smallest")
# r2py:entity:vec_rank_5
print(vec_rank(y, na_value="smallest"))

# vec_rank(y, nan_distinct = TRUE)
# r2py:entity:vec_rank_6
print(vec_rank(y, nan_distinct=True))

# vec_rank(y, direction = "desc", na_value = "largest")
# r2py:entity:vec_rank_7
print(vec_rank(y, direction="desc", na_value="largest"))

# vec_rank(y, incomplete = "na")
# r2py:entity:vec_rank_8
print(vec_rank(y, incomplete="na"))

# z <- c(2L, 3L, 4L, 4L, 5L, 2L)
# r2py:entity:z
z = np.array([2, 3, 4, 4, 5, 2])

# df <- data_frame(x = x, z = z)
# r2py:entity:df_1
df = pd.DataFrame({'x': x, 'z': z})
print(df)

# vec_rank(df)
# r2py:entity:vec_rank_9
print(vec_rank(df))