# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/DBI__rd_example__dbListObjects_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'DBI__rd_example__dbListObjects_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:requireNamespace
import sqlite3
import pandas as pd
from plotnine import *

# Setup connection to in-memory SQLite database
# r2py:entity:con
con = sqlite3.connect(":memory:")

# List objects (tables) in the database
# r2py:entity:dbListObjects
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
print(tables)

# Load mtcars dataset (using plotnine's built-in dataset)

# Write table to database
# r2py:entity:dbWriteTable
mtcars.to_sql("mtcars", con, index=False)

# List objects (tables) in the database again
# r2py:entity:dbListObjects_1
tables_updated = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", con)
print(tables_updated)

# Disconnect
# r2py:entity:dbDisconnect
con.close()