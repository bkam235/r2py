# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import ps
import os
from datetime import datetime, timezone

# No direct equivalent needed for suppressPackageStartupMessages in Python imports.

# r2py:entity:is_cran_check
def is_cran_check():
    """Mimics ps:::is_cran_check()"""
    if os.environ.get("NOT_CRAN") == "true":
        return False
    return os.environ.get("_R_CHECK_PACKAGE_NAME_", "") != ""

# r2py:entity:ps_is_supported
def ps_is_supported():
    """Mimics ps::ps_is_supported()"""
    # Python's psutil (which the ps library usually wraps or mimics) 
    # is generally supported across platforms if installed.
    return True

# Guard logic: if (ps::ps_is_supported() && ! ps:::is_cran_check())
if ps_is_supported() and not is_cran_check():
    try:
        # r2py:entity:p
        # ps_handle() in R typically gets the current process
# r2py:entity:p
        p = ps.Process()
        # R auto-prints p: <ps::ps_handle> PID=..., NAME=..., AT=...
        # We mimic the formatted output string
        print(f"<ps::ps_handle> PID={p.pid}, NAME={p.name()}, AT={datetime.fromtimestamp(p.create_time(), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        
        # r2py:entity:ps_create_time
        # R's ps_create_time(p) returns a POSIXct time formatted as "YYYY-MM-DD HH:MM:SS GMT"
# r2py:entity:ps_create_time
        create_time = datetime.fromtimestamp(p.create_time(), tz=timezone.utc)
        print(f"[1] \"{create_time.strftime('%Y-%m-%d %H:%M:%S GMT')}\"")
    except Exception:
        pass