# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/data.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'data.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['DT']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import string
import sys

# Entity: suppressPackageStartupMessages / import_data.table
# library(data.table) is handled by the pandas import.

# Entity: DT
# DT = data.table(A=1:10, B=letters[1:10])
# r2py:entity:DT
letters_list = list(string.ascii_lowercase)
DT = pd.DataFrame({'A': list(range(1, 11)), 'B': letters_list[0:10]})

# Entity: DT2
# DT2 = data.table(A=1:10000, ColB=10000:1)
# r2py:entity:DT2
DT2 = pd.DataFrame({'A': list(range(1, 10001)), 'ColB': list(range(10000, 0, -1))})

# Entity: setkey
# setkey(DT, B)
# In data.table, setkey sorts the table and sets the key.
# r2py:entity:setkey
DT = DT.sort_values('B').reset_index(drop=True)
DT.attrs['key'] = ['B']

# Entity: tables
# r2py:entity:tables
def tables():
    """
    Mimics the data.table::tables() function.
    Iterates through global variables to find data-table-like objects.
    """
    # Get all globals that are pandas DataFrames (mimicking is.data.table)
    found_tables = []
    for name, obj in globals().items():
        if isinstance(obj, pd.DataFrame):
            # Calculate memory usage in MB
            mb = obj.memory_usage(deep=True).sum() / (1024 * 1024)
            # Get columns
            cols = ",".join(obj.columns.tolist())
            # Get key from attributes (set by our setkey equivalent)
            key = obj.attrs.get('key', '[NULL]')
            if isinstance(key, list):
                key = ",".join(key)
            
            found_tables.append({
                'NAME': name,
                'NROW': len(obj),
                'NCOL': len(obj.columns),
                'MB': int(mb),
                'COLS': cols,
                'KEY': key
            })
    
    if not found_tables:
        print("No objects of class data.table exist in .GlobalEnv")
        return
    
    # Convert to DataFrame for printing to match R output
    info = pd.DataFrame(found_tables)
    # R output: NAME NROW NCOL MB COLS KEY
    # Print formatted as data.table
    # Note: R's tables() output is essentially a data.table print
    
    # Formatting to match the specific R output provided in verification
    #      NAME  NROW NCOL MB   COLS    KEY
    # 1:   DT    10    2  0    A,B      B
    # 2:  DT2 10000    2  0 A,ColB [NULL]
    
    # We manually format to match the exact structure
    print(f"{'NAME':<6} {'NROW':<6} {'NCOL':<6} {'MB':<6} {'COLS':<10} {'KEY':<10}")
    for i, row in info.iterrows():
        print(f"{i+1}: {row['NAME']:<6} {row['NROW']:<6} {row['NCOL']:<6} {row['MB']:<6} {row['COLS']:<10} {row['KEY']:<10}")
    
    total_mb = sum(info['MB'])
    print(f"Total: {total_mb}MB using type_size")

# Execute tables()
# r2py:entity:tables
tables()