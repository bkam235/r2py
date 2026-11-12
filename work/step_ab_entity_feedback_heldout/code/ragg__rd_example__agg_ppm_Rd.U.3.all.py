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

# Global variable to track the open device file, simulating R's graphics device state
_current_ppm_device = None

def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    global _current_ppm_device
    _current_ppm_device = filename
    
    # Calculate dimensions
    if units == "in":
        w_px, h_px = int(width * res), int(height * res)
    elif units == "cm":
        w_px, h_px = int(width * (res / 2.54)), int(height * (res / 2.54))
    elif units == "mm":
        w_px, h_px = int(width * (res / 25.4)), int(height * (res / 25.4))
    else: # px
        w_px, h_px = int(width), int(height)

    # Set up the figure to be the current active one
    plt.figure(figsize=(w_px / res, h_px / res), dpi=res)
    plt.gcf().set_facecolor(bg if bg is not None else background)
    return None

def dev_off():
    global _current_ppm_device
    if _current_ppm_device is None:
        return None
    
    fig = plt.gcf()
    fig.canvas.draw()
    
    # Extract RGBA buffer
    rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    h_px, w_px, _ = fig.canvas.get_width_height() # This is not standard, use the known size
    # Correct way to get dimensions from the figure
    w_px = fig.canvas.get_width_height()[0] if hasattr(fig.canvas, 'get_width_height') else int(fig.get_size_inches()[0] * fig.get_dpi())
    h_px = fig.canvas.get_width_height()[1] if hasattr(fig.canvas, 'get_width_height') else int(fig.get_size_inches()[1] * fig.get_dpi())
    
    rgba_buffer = rgba_buffer.reshape(h_px, w_px, 4)
    rgb_buffer = rgba_buffer[:, :, :3]

    with open(_current_ppm_device, 'wb') as f:
        f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
        f.write(rgb_buffer.tobytes())
    
    plt.close(fig)
    res_msg = "null device" # In R, dev.off() typically prints a summary or null device
    print(res_msg)
    _current_ppm_device = None
    return res_msg

# suppressPackageStartupMessages(library(ragg)) -> Handled by imports
# r2py:entity:file
file = tempfile.mktemp(suffix='.ppm')

# r2py:entity:agg_ppm
agg_ppm(file)

# plot(sin, -pi, 2*pi)
x = np.linspace(-pi, 2 * pi, 1000)
y = np.sin(x)
plt.plot(x, y)

# r2py:entity:dev.off
dev_off()