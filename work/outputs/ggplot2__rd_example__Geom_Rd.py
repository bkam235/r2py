# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__Geom_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__Geom_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.geom.geom import Geom
from plotnine.drawing import Drawing
from plotnine.rendering import render_geom

# Since plotnine's internal Geom classes are complex to extend via a simple wrapper 
# compared to ggproto, we define the logic of GeomSimplePoint.
# Note: In Python/plotnine, custom geoms usually inherit from Geom and implement draw_panel.

# r2py:entity:GeomSimplePoint
class GeomSimplePoint(Geom):
    required_aes = ["x", "y"]
    
    def draw_panel(self, data, panel_params, coord):
        # Transform data based on coordinates
        data = coord.transform(data, panel_params)
        
        # plotnine renders to a Drawing object; we use the point drawing logic
        # In a real implementation, this would call a low-level graphics primitive.
        # For this translation, we mimic the point drawing behavior.
        return Drawing().add_points(data['x'], data['y'])

# r2py:entity:geom_simple_point
def geom_simple_point(**kwargs, mapping=None, data=None, stat="identity", position="identity", na_rm=False, show_legend=None, inherit_aes=True):
    # In plotnine, custom layers are typically created by passing the Geom class to a layer function
    return layer(
        mapping=mapping, 
        data=data,
        geom=GeomSimplePoint, 
        stat=stat, 
        position=position,
        show_legend=show_legend, 
        inherit_aes=inherit_aes,
        params={"na_rm": na_rm, **kwargs}
    )

# Data setup (mpg equivalent)
# plotnine has mpg built-in
from plotnine.data import mpg

# Plotting
# Since geom_simple_point is a custom extension, we use it within a ggplot call
# Note: For the code to execute without a custom rendering backend, 
# standard geom_point is the functional equivalent of a simple point plot.
# r2py:entity:ggplot
(ggplot(mpg, aes(x='displ', y='hwy')) 
# r2py:entity:geom_simple_point_1
 + geom_simple_point())