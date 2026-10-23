# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/DBI__rd_example__dbExecute_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'DBI__rd_example__dbExecute_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:requireNamespace
import sqlite3
import pandas as pd
import numpy as np

# Establish connection to an in-memory SQLite database
# r2py:entity:con
con = sqlite3.connect(":memory:")

# Setup initial data (mimicking head(cars, 3))
# r2py:entity:dbWriteTable
cars_initial = pd.DataFrame({
    'speed': [4, 4, 7],
    'dist': [2, 0, 4]
})

# dbWriteTable
cars_initial.to_sql("cars", con, index=False)

# dbReadTable
# r2py:entity:dbReadTable
print(pd.read_sql("SELECT * FROM cars", con)) # there are 3 rows

# dbExecute (Simple Insert)
# r2py:entity:dbExecute
con.execute(
    "INSERT INTO cars (speed, dist) VALUES (1, 1), (2, 2), (3, 3)"
)
con.commit()
# r2py:entity:dbReadTable_1
print(pd.read_sql("SELECT * FROM cars", con)) # there are now 6 rows

# dbExecute (Parameterized Insert)
# params = list(4:7, 5:8)
# r2py:entity:dbExecute_1
params = [(i, i+1) for i in range(4, 8)]
con.executemany(
    "INSERT INTO cars (speed, dist) VALUES (?, ?)",
    params
)
con.commit()
# r2py:entity:dbReadTable_2
print(pd.read_sql("SELECT * FROM cars", con)) # there are now 10 rows

# r2py:entity:dbDisconnect
con.close()