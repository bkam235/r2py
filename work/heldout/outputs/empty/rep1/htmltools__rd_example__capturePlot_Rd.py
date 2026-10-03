# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/htmltools__rd_example__capturePlot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__capturePlot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars', 'pressure']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import os
import webbrowser
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, save_plot

# Mocking 'cars' and 'pressure' datasets since they are built-in to R
# cars: speed vs dist
# pressure: temperature vs pressure

# Note: capturePlot is a helper function in R; in Python we use plotnine.save_plot
# res <- capturePlot(plot(cars))
# r2py:entity:res
res = "cars_plot.png"
p1 = ggplot(cars, aes('speed', 'dist')) + geom_point()
save_plot(p1, res)

# r2py:entity:browseURL
webbrowser.open(res)
# r2py:entity:unlink
os.remove(res)

# pngpath <- tempfile(fileext = ".png")
# r2py:entity:pngpath
pngpath = "temp_pressure.png"
# capturePlot(plot(pressure), pngpath, width = 800, height = 375)
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes('temperature', 'pressure')) + geom_point()
save_plot(p2, pngpath, width=800/96, height=375/96) # Convert px to inches
# r2py:entity:browseURL_1
webbrowser.open(pngpath)
# r2py:entity:unlink_1
os.remove(pngpath)

# Check for SVG capabilities (Cairo is standard in plotnine/matplotlib)
# if (capabilities("cairo")) { ... }
# r2py:entity:capabilities
try:
    # svgpath <- capturePlot(...)
# r2py:entity:svgpath
    svgpath = "temp_pressure.svg"
    # plotnine uses the file extension to determine format
    save_plot(p2, svgpath, width=8, height=3.75)
# r2py:entity:browseURL_2
    webbrowser.open(svgpath)
# r2py:entity:unlink_2
    os.remove(svgpath)
except Exception:
    pass