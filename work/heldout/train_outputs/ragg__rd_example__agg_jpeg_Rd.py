# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_jpeg_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_jpeg_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# r2py:entity:file
file = os.path.join(tempfile.gettempdir(), 'temp_plot.jpeg')

# Generate data for the sin function from -pi to 2*pi
# r2py:entity:plot
x = np.linspace(-np.pi, 2 * np.pi, 1000)
y = np.sin(x)

plt.figure()
plt.plot(x, y)

# Save with quality=50 (approximate via pil_kwargs)
# r2py:entity:agg_jpeg
plt.savefig(file, format='jpeg', pil_kwargs={'quality': 50})
# r2py:entity:dev.off
plt.close()