# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import pandas as pd
import numpy as np
from datetime import date, datetime

# r2py:entity:con
def simulate_dbi():
    """Simulates the R simulate_dbi() function."""
    return {}

# r2py:entity:sql_escape_logical
def sql_escape_logical(con, values):
    res = [str(val).upper() if pd.notna(val) else "NULL" for val in values]
    return res

# r2py:entity:sql_escape_date
def sql_escape_date(con, val):
    if pd.isna(val):
        return "NULL"
    # R's sql_escape_date wraps the date in single quotes
    return f"'{val}'"

# r2py:entity:sql_escape_raw
def sql_escape_raw(con, val):
    # R's charToRaw("hi") is 68 69 in hex
    if isinstance(val, str):
        hex_val = val.encode('utf-8').hex().upper()
    else:
        hex_val = val.hex().upper()
    return f"X'{hex_val}'"

def r_print_vector(vec):
    """Helper to mimic R's printing of character vectors."""
    if not isinstance(vec, list):
        vec = [vec]
    formatted = '  '.join([f'"{v}"' for v in vec])
    print(f"[1] {formatted}")

# Simulation of the R script
# r2py:entity:con
con = simulate_dbi()

# r2py:entity:sql_escape_logical
logical_vals = [True, False, np.nan]
res_logical = sql_escape_logical(con, logical_vals)
r_print_vector(res_logical)

# r2py:entity:sql_escape_date
res_date = sql_escape_date(con, date.today())
r_print_vector(res_date)

# r2py:entity:sql_escape_date_1
# Using a fixed timestamp or datetime.now() to match R's Sys.time()
res_time = sql_escape_date(con, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
r_print_vector(res_time)

# r2py:entity:sql_escape_raw
res_raw = sql_escape_raw(con, "hi")
r_print_vector(res_raw)