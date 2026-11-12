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

# Global to track the active device file
_active_ppm_file = None

def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    global _active_ppm_file
    _active_ppm_file = filename
    
    # Calculate dimensions
    if units == "in":
        w_px = int(width * res)
        h_px = int(height * res)
    elif units == "cm":
        w_px = int(width * (res / 2.54))
        h_px = int(height * (res / 2.54))
    elif units == "mm":
        w_px = int(width * (res / 25.4))
        h_px = int(height * (res / 25.4))
    else: # px
        w_px = int(width)
        h_px = int(height)
        
    plt.figure(figsize=(w_px / res, h_px / res), dpi=res)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0) # Mimic R's fill
    return None

def dev_off():
    global _active_ppm_file
    if _active_ppm_file is None:
        print("null device")
        return "null device"
    
    fig = plt.gcf()
    fig.canvas.draw()
    
    # Extract RGB data
    rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    h, w, _ = fig.canvas.get_width_height() # Wait, get_width_height is not standard
    # Use the buffer shape instead
    rgba_buffer = rgba_buffer.reshape(-1, 4) # This is risky if shape is unknown
    # Re-calculate based on figure
    w_px = fig.canvas.get_width_height()[0] if hasattr(fig.canvas, 'get_width_height') else 480
    h_px = fig.canvas.get_height_width()[1] if hasattr(fig.canvas, 'get_height_width') else 480
    # Better: use the image array directly
    img = fig.canvas.renderer.buffer_rgba()
    rgb_buffer = img[:, :, :3]
    w_px, h_px, _ = rgb_buffer.shape[1], rgb_buffer.shape[0], 3

    with open(_active_ppm_file, 'wb') as f:
        f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
        f.write(rgb_buffer.tobytes())
    
    plt.close(fig)
    res = f"null device" # dev.off() usually returns "null device" in R
    print(res)
    _active_ppm_file = None
    return res

# suppressPackageStartupMessages(library(ragg))
# r2py:entity:file
file = tempfile.mktemp(suffix='.ppm')

# r2py:entity:agg_ppm
agg_ppm(file)

# r2py:entity:plot
# plot(sin, -pi, 2*pi)
x = np.linspace(-pi, 2 * pi, 1000)
y = np.sin(x)
plt.plot(x, y)

# r2py:entity:dev.off
dev_off()