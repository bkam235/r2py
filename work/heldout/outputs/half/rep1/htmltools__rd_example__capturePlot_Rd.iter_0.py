# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/htmltools__rd_example__capturePlot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__capturePlot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars', 'pressure']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import os
import webbrowser
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, theme_minimal
from plotnine.plotting import render_plot

# Mocking the 'cars' and 'pressure' datasets usually found in R


# res <- capturePlot(plot(cars))
# Plotnine doesn't have a direct "capturePlot" helper, we render to a file
# r2py:entity:res
res = "temp_cars_plot.png"
p1 = ggplot(cars, aes(x='speed', y='dist')) + geom_point()
p1.save(res, width=5, height=5, dpi=100)

# browseURL(res)
# r2py:entity:browseURL
webbrowser.open(os.path.abspath(res))

# unlink(res)
# r2py:entity:unlink
os.remove(res)

# pngpath <- tempfile(fileext = ".png")
# r2py:entity:pngpath
pngpath = "temp_pressure_plot.png"
# capturePlot(plot(pressure), pngpath, width = 800, height = 375)
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
p2.save(pngpath, width=8, height=3.75, dpi=100) # plotnine uses inches

# browseURL(pngpath)
# r2py:entity:browseURL_1
webbrowser.open(os.path.abspath(pngpath))

# unlink(pngpath)
# r2py:entity:unlink_1
os.remove(pngpath)

# if (capabilities("cairo")) { ... }
# Python's plotnine/matplotlib supports SVG by default if the backend is available
# r2py:entity:capabilities
try:
    # svgpath <- capturePlot(plot(pressure), tempfile(fileext = ".svg"), ...)
# r2py:entity:svgpath
    svgpath = "temp_pressure_plot.svg"
    p3 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
    p3.save(svgpath, width=8, height=3.75)
    
    # browseURL(svgpath)
# r2py:entity:browseURL_2
    webbrowser.open(os.path.abspath(svgpath))
    
    # unlink(svgpath)
# r2py:entity:unlink_2
    os.remove(svgpath)
except Exception:
    pass