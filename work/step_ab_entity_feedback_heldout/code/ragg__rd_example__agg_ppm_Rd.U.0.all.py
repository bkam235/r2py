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

# Global variable to track the active R-like device
_active_device = {"file": None, "fig": None}

def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    """
    Equivalent to ragg::agg_ppm. 
    In R, this opens a device. We create a matplotlib figure and store it globally.
    """
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

    # Create a figure that simulates the R device
    fig = plt.figure(figsize=(w_px / res, h_px / res), dpi=res)
    fig.set_facecolor(bg if bg is not None else background)
    
    _active_device["file"] = filename
    _active_device["fig"] = fig
    return None

def dev_off():
    """
    Closes the current device and writes the output file.
    """
    global _active_device
    if _active_device["fig"] is not None:
        fig = _active_device["fig"]
        filename = _active_device["file"]
        
        # Render the figure
        fig.canvas.draw()
        
        # Use the Agg backend to get the RGB buffer
        rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        h, w, _ = fig.canvas.get_width_height() # This is slightly wrong in some versions, manually use calculated w_px, h_px
        # Since we know the dimensions from the figure setup:
        w_px = fig.get_size_inches()[0] * fig.get_dpi()
        h_px = fig.get_size_inches()[1] * fig.get_dpi()
        w_px, h_px = int(w_px), int(h_px)
        
        rgba_buffer = rgba_buffer.reshape(h_px, w_px, 4)
        rgb_buffer = rgba_buffer[:, :, :3]

        # Write PPM P6 format
        with open(filename, 'wb') as f:
            f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
            f.write(rgb_buffer.tobytes())
        
        plt.close(fig)
        _active_device["fig"] = None
        _active_device["file"] = None
        
        # R's dev.off() prints the null device or the device that was closed
        print("null device")

# suppressPackageStartupMessages(library(ragg)) -> Handled by imports
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