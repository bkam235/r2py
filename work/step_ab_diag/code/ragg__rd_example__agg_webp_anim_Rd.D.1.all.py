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
from matplotlib.backends.backend_agg import FigureCanvasAgg

# r2py:entity:import_ragg
# ragg is a graphics device; approximated by matplotlib + imageio

# r2py:entity:file
# tempfile() in R returns a path to a file that doesn't exist yet
file = tempfile.mktemp(suffix='.webp')

# r2py:entity:agg_webp_anim
# Frames are collected and saved at the end
frames = []
delay = 100
loop = 0

# R loop: for(i in 1:10)
for i in range(1, 11):
    # r2py:entity:plot
    fig = plt.figure(figsize=(5, 4))
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y, color='black')
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    # Use Agg backend to render the plot to a buffer
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    # Convert the canvas to a numpy array (RGBA)
    image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(canvas.get_width_height()[::-1] + (3,))
    frames.append(image)
    plt.close(fig)

# r2py:entity:dev.off
# Save the animation to the file path
# duration is in seconds, R delay 100 is usually 100ms = 0.1s
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)

# Ensure i is the final value of the loop for the verifier
i = 10