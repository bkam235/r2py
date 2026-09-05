# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/DBI__rd_example__dbSendQueryArrow_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'DBI__rd_example__dbSendQueryArrow_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:requireNamespace_1
import sqlite3
import pandas as pd
import pyarrow as pa

# Create an in-memory SQLite connection
# r2py:entity:con
con = sqlite3.connect(":memory:")

# Load mtcars dataset (using pandas since it's commonly used for this dataset)
# Assuming mtcars is available via a CSV or common source, but for simulation:

# Write table to SQL
# r2py:entity:dbWriteTable
mtcars.to_sql("mtcars", con, index=False)

# Execute query and fetch as a PyArrow Table
# SQLite doesn't have a direct 'dbSendQueryArrow' equivalent, 
# so we fetch via pandas and convert to arrow
# r2py:entity:rs
df = pd.read_sql_query("SELECT * FROM mtcars WHERE cyl = 4", con)
table = pa.Table.from_pandas(df)

# r2py:entity:dbClearResult
print(table)

# Close connection
# r2py:entity:dbDisconnect
con.close()