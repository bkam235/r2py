# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import pandas as pd
import numpy as np
import sqlite3

# Python does not have a direct 1:1 equivalent to dbplyr's build_sql 
# as it's designed for translating R expressions to SQL. 
# The closest equivalent for simulating SQL behavior is using sqlite3.

# Simulate a database connection
# r2py:entity:con
con = sqlite3.connect(':memory:')

# r2py:entity:build_sql
def build_sql(*args):
    # Simplified substitute for build_sql: joins arguments into a string
    # In real scenarios, one would use parameterized queries to prevent injection
    return "".join(str(arg) for arg in args)

# Example 1
# r2py:entity:build_sql
print(build_sql("SELECT * FROM TABLE"))

# Example 2
# r2py:entity:x
x = "TABLE"
# r2py:entity:build_sql_1
print(build_sql("SELECT * FROM ", x))

# ident() and sql() are internal dbplyr helpers for quoting identifiers.
# In Python, we can use a simple helper to simulate identifier quoting.
# r2py:entity:build_sql_2
def ident(val):
    return f'"{val}"'

# r2py:entity:build_sql_3
def sql(val):
    return val

# Example 3
# r2py:entity:build_sql_2
print(build_sql("SELECT * FROM ", ident(x)))

# Example 4
# r2py:entity:build_sql_3
print(build_sql("SELECT * FROM ", sql(x)))

# Example 5: SQL Injection demonstration
# r2py:entity:name
name = "Robert'); DROP TABLE Students;--"
# r2py:entity:build_sql_4
print(build_sql("INSERT INTO Students (Name) VALUES ('", name, "')"))