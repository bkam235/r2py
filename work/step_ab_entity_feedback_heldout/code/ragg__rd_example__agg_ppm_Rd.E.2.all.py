# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_ppm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_ppm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# State to track the active graphics device
_active_device_file = None

def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    global _active_device_file
    _active_device_file = filename
    
    # Set up the figure according to R's agg_ppm defaults
    # In R, agg_ppm opens the device; here we prepare the plt state
    plt.figure(figsize=(width/res, height/res), dpi=res)
    plt.rcParams['figure.facecolor'] = background if bg is None else bg
    return None

def plot_sin(func, start, end):
    # Mocking plot(sin, -pi, 2*pi)
    x = np.linspace(start, end, 1000)
    y = func(x)
    plt.plot(x, y)

def dev_off():
    global _active_device_file
    if _active_device_file is None:
        return "null device"
    
    # Render the current figure to the file
    fig = plt.gcf()
    fig.canvas.draw()
    
    # Get RGB buffer
    rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    h, w, _ = fig.canvas.get_width_height() # Simplified size retrieval
    # Re-calculate based on actual figure size
    h_px = fig.canvas.get_height_in_pixels()
    w_px = fig.canvas.get_width_in_pixels()
    
    rgba_buffer = rgba_buffer.reshape(h_px, w_px, 4)
    rgb_buffer = rgba_buffer[:, :, :3]

    with open(_active_device_file, 'wb') as f:
        f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
        f.write(rgb_buffer.tobytes())
    
    plt.close(fig)
    device_name = _active_device_file
    _active_device_file = None
    print(device_name)
    return device_name

# suppressPackageStartupMessages(library(ragg)) -> handled by imports
# r2py:entity:file
file = tempfile.mktemp(suffix='.ppm')

# r2py:entity:agg_ppm
agg_ppm(file)

# r2py:entity:plot
# R: plot(sin, -pi, 2*pi)
plot_sin(np.sin, -pi, 2*pi)

# r2py:entity:dev.off
dev_off()