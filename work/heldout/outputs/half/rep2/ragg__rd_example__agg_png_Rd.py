# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/ragg__rd_example__agg_png_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_png_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import tempfile
import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:file
file = tempfile.mktemp(suffix='.png')

# r2py:entity:agg_png
# In Python, matplotlib handles the device management. 
# The agg_png functionality is equivalent to creating a figure and saving it.
plt.figure(figsize=(480/72, 480/72), dpi=72)
# r2py:entity:plot
x = np.linspace(-np.pi, 2 * np.pi, 100)
plt.plot(x, np.sin(x))

# r2py:entity:dev.off
plt.savefig(file)
plt.close()