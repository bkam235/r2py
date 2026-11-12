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
# In R, tempfile(fileext='.tiff') creates a path to a file that doesn't exist yet
file = tempfile.mktemp(suffix='.tiff')

# r2py:entity:agg_tiff
# agg_tiff opens the device. In matplotlib, we initialize the figure.
# The compression 'lzw+p' is handled during save.
plt.figure()

# r2py:entity:plot
x = np.linspace(-pi, 2 * pi, 1000)
y = np.sin(x)
plt.plot(x, y)

# Save the plot to the file specified by agg_tiff before closing
plt.savefig(file, format='tiff', pil_kwargs={"compression": "tiff_lzw"})

# r2py:entity:dev.off
plt.close()
print(f"null device") # R's dev.off() often prints the device being closed or "null device"