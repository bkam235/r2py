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

def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    """
    Equivalent to ragg::agg_ppm.
    In R, this opens a device. In Python, we'll set up a figure that will be saved to this filename.
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

    # Store metadata for later saving
    plt.gcf()._ragg_ppm_file = filename
    plt.gcf()._ragg_ppm_w = w_px
    plt.gcf()._ragg_ppm_h = h_px
    
    plt.figure(figsize=(w_px / res, h_px / res), dpi=res)
    return None

# suppressPackageStartupMessages(library(ragg))
# import_ragg: handled by imports

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
# In R, dev.off() closes the device and returns the device number (usually 2).
# We must write the file now and print the return value.
fig = plt.gcf()
if hasattr(fig, '_ragg_ppm_file'):
    w_px = fig._ragg_ppm_w
    h_px = fig._ragg_ppm_h
    filename = fig._ragg_ppm_file
    
    fig.canvas.draw()
    rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    rgba_buffer = rgba_buffer.reshape(h_px, w_px, 4)
    rgb_buffer = rgba_buffer[:, :, :3]

    with open(filename, 'wb') as f:
        f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
        f.write(rgb_buffer.tobytes())

plt.close()
print(2) # dev.off() typically prints the device number it closes