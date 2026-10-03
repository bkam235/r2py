# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/htmltools__rd_example__capturePlot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__capturePlot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars', 'pressure']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, save_plot
import webbrowser
import os
import tempfile

# Setup dummy data to match R's cars and pressure datasets
# cars: speed, dist

# pressure: temperature, pressure

# First block: capturePlot(plot(cars))
# In R, capturePlot usually returns a temp file path of the plot
# r2py:entity:res
res = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
p1 = ggplot(cars, aes(x='speed', y='dist')) + geom_point()
save_plot(res, p1)

# r2py:entity:browseURL
webbrowser.open(f"file://{os.path.abspath(res)}")
# r2py:entity:unlink
os.unlink(res)

# Second block: capturePlot(plot(pressure), pngpath, ...)
# r2py:entity:pngpath
pngpath = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
# plotnine handles dimensions via figure size in inches (800px/72dpi approx 11.1, 375px/72dpi approx 5.2)
save_plot(pngpath, p2, width=800/72, height=375/72)
# r2py:entity:browseURL_1
webbrowser.open(f"file://{os.path.abspath(pngpath)}")
# r2py:entity:unlink_1
os.unlink(pngpath)

# Third block: SVG export (if capabilities("cairo") equivalent)
# Python's plotnine/matplotlib uses cairo if installed, otherwise standard svg
# r2py:entity:capabilities
try:
# r2py:entity:svgpath
    svgpath = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
    save_plot(svgpath, p2, width=8, height=3.75)
# r2py:entity:browseURL_2
    webbrowser.open(f"file://{os.path.abspath(svgpath)}")
# r2py:entity:unlink_2
    os.unlink(svgpath)
except Exception:
    pass