import pandas as pd
import numpy as np

# r2py:entity:chop
def chop(data, cols):
    if isinstance(cols, str):
        cols = [cols]
    
    all_cols = data.columns.tolist()
    group_cols = [c for c in all_cols if c not in cols]
    
    # R's chop: one row per unique combination of non-chopped variables.
    # The chopped columns become lists.
    res = data.groupby(group_cols, sort=False).agg({c: list for c in cols}).reset_index()
    return res

# r2py:entity:nest
def nest(data, data_cols, key='data'):
    if isinstance(data_cols, str):
        data_cols = [data_cols]
    
    all_cols = data.columns.tolist()
    group_cols = [c for c in all_cols if c not in data_cols]
    
    # R's nest: stores the subset of the dataframe for each group in a list-column
    def nest_group(group):
        return pd.Series({key: group[data_cols]})
    
    res = data.groupby(group_cols, sort=False).apply(nest_group, include_groups=False).reset_index()
    return res

# r2py:entity:unchop
def unchop(data, cols, keep_empty=False):
    if isinstance(cols, str):
        cols = [cols]
    
    df = data.copy()
    for col in cols:
        # Check for mixed types to emulate R's type compatibility check
        # We check if elements are consistently lists/arrays or not
        if len(df) > 0:
            first_val = df[col].iloc[0]
            is_list_like = isinstance(first_val, (list, np.ndarray, pd.DataFrame))
            for val in df[col]:
                if isinstance(val, (list, np.ndarray, pd.DataFrame)) != is_list_like:
                    raise TypeError("Incompatible types in list-column")

        # Handle list-columns of DataFrames
        sample = None
        for item in df[col]:
            if item is not None and not (isinstance(item, (list, np.ndarray)) and len(item) == 0):
                sample = item
                break
        
        if isinstance(sample, pd.DataFrame):
            # Gather all possible columns across all nested DFs
            all_nested_cols = []
            for item in df[col]:
                if isinstance(item, pd.DataFrame):
                    for c in item.columns:
                        if c not in all_nested_cols:
                            all_nested_cols.append(c)
            
            rows = []
            for idx, row in df.iterrows():
                val = row[col]
                base_data = row.drop(col)
                
                if isinstance(val, pd.DataFrame) and not val.empty:
                    for _, nested_row in val.iterrows():
                        new_row = base_data.copy()
                        for c_name, c_val in nested_row.items():
                            # R naming: col$name if name != col, else $name
                            final_name = f"{col}${c_name}" if c_name != col else f"${c_name}"
                            new_row[final_name] = c_val
                        rows.append(new_row)
                elif keep_empty:
                    new_row = base_data.copy()
                    for c_name in all_nested_cols:
                        final_name = f"{col}${c_name}" if c_name != col else f"${c_name}"
                        new_row[final_name] = np.nan
                    rows.append(new_row)
            
            if not rows:
                df = pd.DataFrame(columns=df.columns)
            else:
                df = pd.DataFrame(rows).reset_index(drop=True)
        else:
            # Vector unchop (lists/arrays)
            df = df.explode(col)
            if not keep_empty:
                df = df.dropna(subset=[col])
            df = df.reset_index(drop=True)
                
    return df

# Chop ----------------------------------------------------------------------
# r2py:entity:df
df = pd.DataFrame({'x': [1, 1, 1, 2, 2, 3], 'y': range(1, 7), 'z': range(6, 0, -1)})
# r2py:entity:chop
chop_res = chop(df, ['y', 'z'])
print(chop_res)

# r2py:entity:nest
nest_res = nest(df, ['y', 'z'])
print(nest_res)

# Unchop --------------------------------------------------------------------
# r2py:entity:df_1
df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [[], [1], [1, 2], [1, 2, 3]]})
# r2py:entity:unchop
unchop_res = unchop(df, 'y', keep_empty=False)
print(unchop_res)

# r2py:entity:unchop_1
unchop_empty_res = unchop(df, 'y', keep_empty=True)
print(unchop_empty_res)

# unchop will error if the types are not compatible:
# r2py:entity:df_2
df = pd.DataFrame({'x': [1, 2], 'y': ["1", [1, 2, 3]]})
# r2py:entity:try
try:
    unchop_mixed = unchop(df, 'y')
except Exception:
    pass

# Unchopping a list-col of data frames
# r2py:entity:df_3
df = pd.DataFrame({'x': [1, 2, 3], 'y': [pd.DataFrame(), pd.DataFrame({'x': [1]}), pd.DataFrame({'y': [1, 2]})]})
# r2py:entity:unchop_2
unchop_df_res = unchop(df, 'y', keep_empty=False)
print(unchop_df_res)

# r2py:entity:unchop_3
unchop_df_keep_res = unchop(df, 'y', keep_empty=True)
print(unchop_df_keep_res)