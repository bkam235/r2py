# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/htmltools__rd_example__capturePlot_Rd.py'
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
import tempfile

# Mocking the 'cars' and 'pressure' datasets common in R

# Part 1: Capture plot of cars
# r2py:entity:res
res = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
p1 = ggplot(cars, aes('speed', 'dist')) + geom_point()
save_plot(res, p1)
# r2py:entity:browseURL
webbrowser.open(res)
# r2py:entity:unlink
os.unlink(res)

# Part 2: Capture plot of pressure with specific dimensions
# r2py:entity:pngpath
pngpath = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes('temp', 'pressure')) + geom_point()
save_plot(pngpath, p2, width=8, height=3.75, dpi=100) # 800/100 = 8 inches
# r2py:entity:browseURL_1
webbrowser.open(pngpath)
# r2py:entity:unlink_1
os.unlink(pngpath)

# Part 3: SVG capture (capabilities("cairo") equivalent via plotnine/matplotlib)
# r2py:entity:capabilities
try:
# r2py:entity:svgpath
    svgpath = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
    p3 = ggplot(pressure, aes('temp', 'pressure')) + geom_point()
    save_plot(svgpath, p3, width=8, height=3.75)
# r2py:entity:browseURL_2
    webbrowser.open(svgpath)
# r2py:entity:unlink_2
    os.unlink(svgpath)
except Exception:
    pass