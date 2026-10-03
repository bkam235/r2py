# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/htmltools__rd_example__capturePlot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__capturePlot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['cars', 'pressure']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
import webbrowser
import os
import tempfile

# Data for cars and pressure equivalents

# res <- capturePlot(plot(cars))
# browseURL(res)
# unlink(res)
# r2py:entity:res
res = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
p1 = ggplot(cars, aes(x='speed', y='dist')) + geom_point()
p1.save(res)
# r2py:entity:browseURL
webbrowser.open(f"file://{os.path.abspath(res)}")
# r2py:entity:unlink
os.remove(res)

# pngpath <- tempfile(fileext = ".png")
# capturePlot(plot(pressure), pngpath, width = 800, height = 375)
# browseURL(pngpath)
# unlink(pngpath)
# r2py:entity:pngpath
pngpath = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
# r2py:entity:capturePlot
p2 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
p2.save(pngpath, width=800/96, height=375/96, dpi=96) # plotnine uses inches
# r2py:entity:browseURL_1
webbrowser.open(f"file://{os.path.abspath(pngpath)}")
# r2py:entity:unlink_1
os.remove(pngpath)

# if (capabilities("cairo")) { ... }
# svgpath <- capturePlot(plot(pressure), tempfile(fileext = ".svg"), grDevices::svg, width = 8, height = 3.75)
# browseURL(svgpath)
# unlink(svgpath)
# r2py:entity:svgpath
svgpath = tempfile.NamedTemporaryFile(suffix=".svg", delete=False).name
p3 = ggplot(pressure, aes(x='temperature', y='pressure')) + geom_point()
p3.save(svgpath, width=8, height=3.75)
# r2py:entity:browseURL_2
webbrowser.open(f"file://{os.path.abspath(svgpath)}")
# r2py:entity:unlink_2
os.remove(svgpath)