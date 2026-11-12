# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_tiff_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_tiff_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# r2py:entity:file
# Use tempfile.mktemp to get a filename without creating the file, mimicking R's tempfile()
file = tempfile.mktemp(suffix='.tiff')

# r2py:entity:agg_tiff
# In R, agg_tiff opens the device. In Matplotlib, we specify the file at save time.
# We store the target file for use later.
target_file = file

# r2py:entity:plot
x = np.linspace(-pi, 2 * pi, 1000)
y = np.sin(x)

plt.figure()
plt.plot(x, y)

# Save to the file specified in agg_tiff
plt.savefig(target_file, format='tiff', pil_kwargs={"compression": "lzw"})

# r2py:entity:dev.off
plt.close()
print("null device 1")