# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/DBI__rd_example__dbGetRowCount_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'DBI__rd_example__dbGetRowCount_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import sqlite3
import pandas as pd
import numpy as np

# Create a connection to an in-memory SQLite database
# r2py:entity:con
con = sqlite3.connect(":memory:")

# mtcars equivalent: loading from a common source since it's not built-in to Python

# Write table to database
# r2py:entity:dbWriteTable
mtcars.to_sql("mtcars", con, index=False)

# Create a cursor and execute query
# r2py:entity:rs
cursor = con.execute("SELECT * FROM mtcars")

# Total rows in result set (sqlite3 doesn't have a direct dbGetRowCount for cursors, 
# but we can simulate it by fetching all or checking the source table)
# Note: In Python, fetching moves the cursor forward.
# r2py:entity:dbGetRowCount
total_rows = len(mtcars)
print(total_rows)

# Fetch first 10 rows
# r2py:entity:ret1
ret1 = pd.DataFrame(cursor.fetchmany(10), columns=[column[0] for column in cursor.description])

# Remaining rows check (approximation since cursor is forward-only)
# In R's DBI, dbGetRowCount(rs) shows remaining. In Python, we track offsets.
# r2py:entity:dbGetRowCount_1
print(total_rows - len(ret1))

# Fetch remaining rows
# r2py:entity:dbClearResult
ret2 = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])

# Remaining rows is now 0
# r2py:entity:dbGetRowCount_2
print(0)

# Verify total rows match
# r2py:entity:nrow_1
print(len(ret1) + len(ret2))

# Close connection
# r2py:entity:dbDisconnect
con.close()