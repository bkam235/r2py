# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/htmltools__rd_example__capturePlot_Rd.py'
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

# Mocking the 'cars' and 'pressure' datasets common in R


# Section 1: Plot cars and browse
# r2py:entity:res
res = "cars_plot.png"
p1 = ggplot(cars, aes(x='speed', y='dist')) + geom_point()
save_plot(res, p1)
# r2py:entity:browseURL
webbrowser.open(res)
# r2py:entity:unlink
os.remove(res)

# Section 2: Plot pressure to tempfile PNG
# r2py:entity:pngpath
pngpath = "temp_pressure.png"
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
save_plot(pngpath, p2, width=8, height=3.75, dpi=100) # Approximate 800x375
# r2py:entity:browseURL_1
webbrowser.open(pngpath)
# r2py:entity:unlink_1
os.remove(pngpath)

# Section 3: Plot pressure to SVG
# Checking for cairo/svg capabilities via existence of svgwrite/plotnine svg support
# r2py:entity:capabilities
try:
# r2py:entity:svgpath
    svgpath = "temp_pressure.svg"
    save_plot(svgpath, p2, width=8, height=3.75)
# r2py:entity:browseURL_2
    webbrowser.open(svgpath)
# r2py:entity:unlink_2
    os.remove(svgpath)
except Exception:
    pass