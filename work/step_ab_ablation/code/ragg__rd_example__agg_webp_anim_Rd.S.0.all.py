# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_webp_anim_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_webp_anim_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import imageio
import tempfile
import os

# r2py:entity:suppressPackageStartupMessages
# Equivalent to library(ragg)
# r2py:entity:import_ragg

# r2py:entity:file
file = tempfile.mktemp(suffix='.webp')

# r2py:entity:agg_webp_anim
# This opens a webp animation device. In Python, we accumulate frames.
delay = 100
loop = 0
frames = []

for i in range(1, 11):
    # r2py:entity:plot
    plt.figure(figsize=(5, 4))
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    # Capture the frame
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    frames.append(image)
    plt.close(fig)

# r2py:entity:dev.off
# Closing the device is equivalent to saving the final animated file.
# imageio duration is in seconds. R delay 100 is 100ms.
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)

# Ensure i remains as the final loop value for verification
i = 10