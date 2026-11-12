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

# r2py:entity:agg_ppm
def agg_ppm(filename, width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    """
    Equivalent to ragg::agg_ppm.
    In R, this opens a graphics device. In Python, we configure the current figure.
    """
    # Set figure size and DPI based on the parameters
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
    
    # We store the filename on the figure object so dev.off can find it
    plt.gcf()._r2py_ppm_file = filename
    return None

# suppressPackageStartupMessages(library(ragg)) -> handled by imports
# r2py:entity:file
file = tempfile.mktemp(suffix='.ppm')

# r2py:entity:agg_ppm
agg_ppm(file)

# r2py:entity:plot
x = np.linspace(-pi, 2 * pi, 1000)
y = np.sin(x)
plt.plot(x, y)

# r2py:entity:dev.off
def dev_off():
    fig = plt.gcf()
    # Render the figure to a buffer
    fig.canvas.draw()
    
    # Extract the RGB buffer
    # agg_ppm in R writes the file when dev.off() is called
    if hasattr(fig, '_r2py_ppm_file'):
        filename = fig._r2py_ppm_file
        rgba_buffer = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        h_px, w_px, _ = rgba_buffer.reshape(fig.canvas.get_width_height()[1], fig.canvas.get_width_height()[0], 4).shape
        rgb_buffer = rgba_buffer.reshape(h_px, w_px, 4)[:, :, :3]

        with open(filename, 'wb') as f:
            f.write(f"P6\n{w_px} {h_px}\n255\n".encode('ascii'))
            f.write(rgb_buffer.tobytes())
            
    plt.close(fig)
    # R's dev.off() typically prints null or a summary of the device closed
    print("null")

dev_off()