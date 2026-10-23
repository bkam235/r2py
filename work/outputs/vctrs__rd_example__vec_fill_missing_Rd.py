# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/vctrs__rd_example__vec_fill_missing_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'vctrs__rd_example__vec_fill_missing_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['df']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:vec_fill_missing
def vec_fill_missing(x, direction="down", max_fill=None):
    if isinstance(x, pd.DataFrame):
        # Data frames are filled rowwise. Rows are only considered missing
        # if all elements of that row are missing.
        mask = x.isna().all(axis=1)
        if not mask.any():
            return x
        
        # Create a helper series to track the "row-missing" status
        # We effectively treat the row as a single unit.
        # To implement this in pandas, we can find non-missing rows
        # and use them to fill the missing ones.
        
        # We can use a temporary column or index-based approach
        # but the simplest is to identify indices of non-all-NA rows.
        filled_df = x.copy()
        
        if direction == "down" or direction == "downup":
            # Forward fill rows where all are NA
            # pandas ffill works column-wise, so we use a trick:
            # Use a mask to only fill where the whole row is NA.
            # We can use a dummy series of indices to ffill the row data.
            indices = pd.Series(np.arange(len(x)))
            indices[~mask] = indices[~mask]
            indices[mask] = np.nan
            
            # This is complex in pandas. Simpler: loop or use a mask.
            # Let's use a loop for exact R behavior on rows.
            last_valid_row = None
            for i in range(len(filled_df)):
                if not mask.iloc[i]:
                    last_valid_row = filled_df.iloc[i]
                elif last_valid_row is not None:
                    if max_fill is None:
                        filled_df.iloc[i] = last_valid_row
                    else:
                        # Count sequential NAs
                        count = 0
                        for j in range(i - 1, -1, -1):
                            if mask.iloc[j]: count += 1
                            else: break
                        if count < max_fill:
                            filled_df.iloc[i] = last_valid_row
            
            if direction == "downup":
                # Backward fill remaining all-NA rows
                next_valid_row = None
                for i in range(len(filled_df) - 1, -1, -1):
                    if not mask.iloc[i] or not filled_df.iloc[i].isna().all():
                        next_valid_row = filled_df.iloc[i]
                    elif next_valid_row is not None:
                        filled_df.iloc[i] = next_valid_row
        
        return filled_df

    else:
        # Handle vector/series
        s = pd.Series(x)
        if direction == "down":
            res = s.ffill(limit=max_fill)
        elif direction == "up":
            res = s.bfill(limit=max_fill)
        elif direction == "downup":
            res = s.ffill(limit=max_fill).bfill(limit=max_fill)
        elif direction == "updown":
            res = s.bfill(limit=max_fill).ffill(limit=max_fill)
        else:
            res = s
        return res.values

# r2py:entity:x
x = np.array([np.nan, np.nan, 1, np.nan, np.nan, np.nan, 3, np.nan, np.nan])

# vec_fill_missing(x, direction = "down")
# r2py:entity:vec_fill_missing
print(vec_fill_missing(x, direction="down"))

# vec_fill_missing(x, direction = "downup")
# r2py:entity:vec_fill_missing_1
print(vec_fill_missing(x, direction="downup"))

# vec_fill_missing(x, max_fill = 1)
# r2py:entity:vec_fill_missing_2
print(vec_fill_missing(x, max_fill=1))

# r2py:entity:y
y = np.array([1, np.nan, 2, np.nan, np.nan, 3, 4, np.nan, 5])

# df <- data_frame(x = x, y = y)
# r2py:entity:df
df = pd.DataFrame({'x': x, 'y': y})
# r2py:entity:df_1
print(df)

# vec_fill_missing(df)
# r2py:entity:vec_fill_missing_3
print(vec_fill_missing(df))