# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import numpy as np
import matplotlib.pyplot as plt
import imageio
import tempfile
import os

# Force non-interactive backend for consistent buffer access
plt.switch_backend('Agg')

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_webp_anim_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_webp_anim_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:file
temp_file_obj = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
file = temp_file_obj.name
temp_file_obj.close()

# r2py:entity:agg_webp_anim
frames = []
delay = 100
loop = 0

# R loop: for(i in 1:10)
for i in range(1, 11):
    # r2py:entity:plot
    fig = plt.figure()
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    fig.canvas.draw()
    # Use buffer_rgba and convert to RGB
    rgba_buffer = fig.canvas.buffer_rgba()
    image = np.asarray(rgba_buffer)[:, :, :3]
    frames.append(image)
    plt.close(fig)

# r2py:entity:dev.off
# duration is in seconds, R delay 100 is 100ms = 0.1s
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)