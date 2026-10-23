# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/testthat__vignette__test-fixtures_s6.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'testthat__vignette__test-fixtures_s6.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import plotnine as pnp
from shiny import App, ui, render

# r2py:entity:sloppy
def sloppy(x, sig_digits):
    # Python's equivalent to options(digits = sig_digits) for printing
    # is using formatted strings or numpy's printoptions
    print(f"{x:.{sig_digits}g}")

# pi (In Python, np.pi is the equivalent)
# r2py:entity:pi
print(np.pi)

# sloppy(pi, 2)
# r2py:entity:sloppy_1
sloppy(np.pi, 2)

# pi
# r2py:entity:pi_1
print(np.pi)