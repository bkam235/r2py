# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import psutil
import os

# R: suppressPackageStartupMessages(library(ps))
# Python equivalent is importing psutil.

# R: .r2py_cp("ps_is_supported")
# R: .r2py_cp("is_cran_check")
# These are markers for the translation tool; no operational Python code needed.

# p <- ps_handle()
# r2py:entity:p
p = psutil.Process(os.getpid())

# R: p
# Based on verification, evaluating p in this context produces no stdout.

# ps_username(p)
# R output shows the handle representation followed by the username.
# The handle representation in R for ps_handle is <ps::ps_handle> PID=..., NAME=..., AT=...
# r2py:entity:ps_username
create_time = p.create_time()
import datetime
dt = datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S.%f')
handle_str = f"<ps::ps_handle> PID={p.pid}, NAME={p.name()}, AT={dt}"

username_val = p.username()
print(handle_str)
print(f'[1] "{username_val}"')