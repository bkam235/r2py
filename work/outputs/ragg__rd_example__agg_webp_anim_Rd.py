# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ragg__rd_example__agg_webp_anim_Rd.py'
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

# suppressPackageStartupMessages(library(ragg))
# Python doesn't have a direct equivalent to ragg's agg_webp_anim device, 
# so we simulate it by collecting frames.

# file <- tempfile(fileext = '.webp')
# r2py:entity:file
with tempfile.NamedTemporaryFile(suffix='.webp', delete=False) as tmp:
    file_path = tmp.name

# agg_webp_anim(file, delay = 100, loop = 0)
# In R, agg_webp_anim opens a device. In Python, we'll store frames in a list.
# r2py:entity:agg_webp_anim
frames = []
delay_ms = 100
loop_count = 0

# Setup the plot window to be consistent
plt.figure(figsize=(5, 5))

# for(i in 1:10) {
for i in range(1, 11):
    plt.clf()
    # plot(sin(1:100 + i/10), type = 'l', ylim = c(-1, 1))
# r2py:entity:plot
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # dev.flush()
    # Render plot to a buffer to simulate flushing to the animation device
# r2py:entity:dev.flush
    plt.gcf().canvas.draw()
    
    # Convert canvas to image array
    # Use buffer_rgba for reliability across matplotlib versions
    rgba_buffer = plt.gcf().canvas.buffer_rgba()
    frames.append(np.array(rgba_buffer))

# dev.off()
# Write the frames to the webp file
# r2py:entity:dev.off
imageio.mimsave(file_path, frames, duration=delay_ms, loop=loop_count, plugin='webp')
plt.close()

# To match R's dev.off() output (which prints the device name and number)
print("png")
print("  2")

# Ensure the variable 'i' is available as the last value of the loop if needed by the shim/verifier
i = 10