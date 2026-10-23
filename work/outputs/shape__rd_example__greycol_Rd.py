# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/shape__rd_example__greycol_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__greycol_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['volcano']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# r2py:entity:graycol
def graycol(n=100, interval=(0, 0.7)):
    """
    Produces a sequence of grey colors.
    R's graycol calls shadepalette which interpolates between white and black 
    within the specified interval.
    """
    # In R, graycol(n, interval=c(0, 0.7)) interpolates from white (0) to black (1)
    # but only uses the segment of the gradient defined by interval.
    # Since it's a grey scale, we can simply map the interval [0, 0.7] to [1, 0] in luminosity.
    
    # Map the interval to a range of greys. 
    # R: inicol="white" (1.0), endcol="black" (0.0)
    # interval [0, 0.7] means we take values from 1.0 down to (1.0 - 0.7) = 0.3
    start_grey = 1.0 - interval[0]
    end_grey = 1.0 - interval[1]
    
    vals = np.linspace(start_grey, end_grey, n)
    return [f"#{int(v*255):02x}{int(v*255):02x}{int(v*255):02x}" for v in vals]

# Mocking R's 'volcano' dataset
# volcano is an 87x87 matrix of elevation data
from statsmodels.datasets import get_rdataset

# filled.contour(volcano, color = graycol, asp = 1, main = "greycol,graycol")
# r2py:entity:filled.contour
plt.figure()
cmap = LinearSegmentedColormap.from_list("greycol", graycol(100), N=100)
plt.contourf(volcano, cmap=cmap)
plt.gca().set_aspect('equal') # asp = 1
plt.title("greycol,graycol")
plt.colorbar()
plt.show()

# graycol(10)
# r2py:entity:graycol
print(graycol(10))

# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = graycol(100), main = "greycol,graycol")
# r2py:entity:image
data_matrix = np.arange(1, 101).reshape(1, 100)
plt.figure()
# For image(), we create a custom cmap from the colors returned by graycol
custom_cmap = LinearSegmentedColormap.from_list("greycol_image", graycol(100))
plt.imshow(data_matrix, aspect='auto', cmap=custom_cmap)
plt.title("greycol,graycol")
plt.axis('off')
plt.show()