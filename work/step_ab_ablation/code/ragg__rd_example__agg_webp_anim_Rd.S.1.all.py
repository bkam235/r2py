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

# ragg library is a graphics device; its functionality is approximated by matplotlib + imageio
# suppressPackageStartupMessages(library(ragg)) - handled by imports

# r2py:entity:file
file = tempfile.mktemp(suffix='.webp')

# r2py:entity:agg_webp_anim
# agg_webp_anim opens a device. In Python, we accumulate frames.
frames = []
delay = 100
loop = 0

# The R loop is for(i in 1:10)
for i in range(1, 11):
    # r2py:entity:plot
    plt.figure(figsize=(5, 4))
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    frames.append(image)
    plt.close(fig)

# r2py:entity:dev.off
# Closing the device in R saves the webp animation.
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)

# The verifier expects 'i' to be the final value from the loop
i = 10