import pandas as pd
import numpy as np
import re

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'data.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:melt
def patterns(*args, cols=None, ignore_case=False, perl=False, fixed=False, useBytes=False):
    if cols is None:
        # This is handled by the call site in the R script logic
        raise ValueError("cols must be a character vector of column names")
    
    patterns_list = []
    for arg in args:
        if isinstance(arg, list):
            patterns_list.extend(arg)
        else:
            patterns_list.append(arg)
            
    if not all(isinstance(p, str) for p in patterns_list):
        raise TypeError("Input patterns must be of type character.")
    
    matched_results = []
    for p in patterns_list:
        regex = re.compile(p, re.IGNORECASE if ignore_case else 0)
        found = [col for col in cols if regex.search(col)]
        if not found:
            raise ValueError(f"Pattern not found: [{p}]")
        matched_results.append(found)
    
    # R's patterns() returns a vector if length 1, otherwise a list
    if len(matched_results) == 1:
        return matched_results[0]
    return matched_results

# r2py:entity:melt
def melt(data, measure_vars=None, id_vars=None, variable_name="variable", value_name="value", na_rm=False):
    all_cols = data.columns.tolist()
    
    # If measure_vars is a list of lists (returned by patterns() for >1 pattern)
    if isinstance(measure_vars, list) and len(measure_vars) > 0 and isinstance(measure_vars[0], list):
        # R data.table::melt behavior for list-based measure.vars:
        # It creates one 'value' column per pattern group.
        # The 'variable' column becomes the index of the pattern.
        
        # Determine id_vars: columns not in any of the measure_vars groups
        flattened_measure = [item for sublist in measure_vars for item in sublist]
        if id_vars is None:
            id_vars = [col for col in all_cols if col not in flattened_measure]
        
        # We need to pivot each group separately and join them, or construct the result
        # R's output for this specific case is: variable | value1 | value2 ...
        # where 'variable' is the row index (1, 2, 3, 4, 5)
        
        # Calculate the number of rows (based on the original data)
        num_rows = len(data)
        res_df = pd.DataFrame({'variable': range(1, num_rows + 1)})
        
        # For each pattern group, find the columns and create valueN
        for i, group in enumerate(measure_vars, 1):
            # The R output for this specific case seems to concatenate the values of 
            # all columns in a group for each row. 
            # However, based on the R output provided: 
            # value1 is 1,2,3,4,5... (from x1, x2) -> Wait, x1 is 1:5, x2 is 6:10.
            # The R output shows value1: 1, 2, 3, 4, 5 and value2: a, b, c, d, e.
            # This means for each row, it takes the first column of each group? 
            # No, looking at R output:
            # row 1: var=1, val1=1, val2=a
            # row 6: var=2, val1=6, val2=f
            # This means it melts each group into a single column by effectively 
            # treating the group as a single entity or taking the first matched col?
            # Actually, if the group contains multiple cols, data.table's melt 
            # usually handles it differently, but here x1, x2 match ^x and y1, y2 match ^y.
            # If measure.vars is a list, it's a "wide" melt.
            # Let's implement the specific logic seen in the R output:
            # value1 = data[group1].sum(axis=1) or similar? 
            # No, the values 1, 2, 3, 4, 5 in value1 match x1. 
            # 6, 7, 8, 9, 10 match x2.
            # Wait: 
            # R Output:
            # 1: 1 1 a  (var=1, val1=1, val2=a)
            # 2: 1 2 b  (var=1, val1=2, val2=b)
            # 3: 1 3 c  (var=1, val1=3, val2=c)
            # 4: 1 4 d  (var=1, val1=4, val2=d)
            # 5: 1 5 e  (var=1, val1=5, val2=e)
            # 6: 2 6 f  (var=2, val1=6, val2=f)
            # ...
            # This is actually a "long" melt where the group of patterns is the 
            # outer level of 'variable', and the columns within the group are 
            # treated as a sequence.
            # Variable 1 (x group): x1(1..5), x2(6..10)
            # Variable 2 (y group): y1(a..e), y2(f..j)
            
            # CORRECT LOGIC:
            # If measure_vars is a list of groups:
            # For each group in measure_vars:
            #   For each col in that group:
            #     Append rows to result: variable = group_index, value = col_values
            pass
        
        # Re-implementing based on the actual R output pattern:
        final_rows = []
        for g_idx, group in enumerate(measure_vars, 1):
            for col in group:
                for r_idx in range(num_rows):
                    final_rows.append({
                        'variable': g_idx,
                        'value': data[col].iloc[r_idx]
                    })
        
        # But R output shows value1, value2... ? No, it shows:
        # "variable value1 value2"
        # Wait, I misread the R output. 
        # R produced:
        #       variable value1 value2
        #       <fctr>  <int> <char>
        #  1:        1      1      a
        #  2:        1      2      b
        #  ...
        #  6:        2      6      f
        # This means it's a wide melt of the GROUPS.
        # For each row in the original data:
        #   For each column in group 1: 
        #     create a row with variable=1, value1=col1_val, value2=col2_val...
        # No, the R output is 10 rows. Original data has 5 rows.
        # Original: 5 rows, 4 cols (x1, x2, y1, y2).
        # Result: 10 rows.
        # Variable 1: rows 1-5. Value 1: x1. Value 2: y1.
        # Variable 2: rows 6-10. Value 1: x2. Value 2: y2.
        # So it's melting across the PATTERNS first, then across the COLUMNS within patterns.
        
        # Let's re-examine:
        # Row 1: var=1, val1=1, val2=a (x1[0], y1[0])
        # Row 2: var=1, val1=2, val2=b (x1[1], y1[1])
        # Row 6: var=2, val1=6, val2=f (x2[0], y2[0])
        # Yes: it's melting the columns grouped by patterns.
        # Group 1: [x1, x2], Group 2: [y1, y2] -> This is not it.
        # Group 1: ^x, Group 2: ^y.
        # Pattern 1 matched [x1, x2], Pattern 2 matched [y1, y2].
        # The result has variable 1 for x1 and y1, then variable 2 for x2 and y2.
        
        # Correct logic for this specific R data.table output:
        # 1. Find cols matching pattern 1, pattern 2...
        # 2. Transpose the match results. 
        #    Instead of (Pat1: [x1, x2], Pat2: [y1, y2]),
        #    we look at (ColIdx1: [x1, y1], ColIdx2: [x2, y2])
        # 3. For each ColIdx (1 to max_cols_in_group):
        #    Create rows for all original data indices.
        
        max_cols = max(len(g) for g in measure_vars)
        final_data = []
        for c_idx in range(max_cols):
            for r_idx in range(len(data)):
                row = {'variable': c_idx + 1}
                for g_idx, group in enumerate(measure_vars, 1):
                    if c_idx < len(group):
                        col_name = group[c_idx]
                        row[f'value{g_idx}'] = data[col_name].iloc[r_idx]
                final_data.append(row)
        
        return pd.DataFrame(final_data)

    # Standard long melt
    if id_vars is None:
        id_vars = [col for col in all_cols if col not in measure_vars]
        
    return pd.melt(data, id_vars=id_vars, value_vars=measure_vars, var_name=variable_name, value_name=value_name)

# suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(None)

# DT = data.table(x1 = 1:5, x2 = 6:10, y1 = letters[1:5], y2 = letters[6:10])
# r2py:entity:DT
DT = pd.DataFrame({
    'x1': list(range(1, 6)),
    'x2': list(range(6, 11)),
    'y1': letters[0:5],
    'y2': letters[5:10]
})

# melt(DT, measure.vars = patterns("^x", "^y", cols=names(DT)))
# r2py:entity:melt
mv1 = patterns("^x", "^y", cols=DT.columns.tolist())
melt_res1 = melt(DT, measure_vars=mv1)
print(melt_res1)

# melt(DT, measure.vars = patterns("^x", "^y"))
# r2py:entity:melt_1
mv2 = patterns("^x", "^y", cols=DT.columns.tolist())
melt_res2 = melt(DT, measure_vars=mv2)
print(melt_res2)