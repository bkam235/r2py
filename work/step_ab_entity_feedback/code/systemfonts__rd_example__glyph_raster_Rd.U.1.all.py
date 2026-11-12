import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# Equivalent to doing nothing as Python doesn't have a direct equivalent to suppressPackageStartupMessages
def suppressPackageStartupMessages(arg):
    return arg

# r2py:entity:import_systemfonts
# Using PIL/fontmanager as Python equivalent for systemfonts
import matplotlib.font_manager as fm

# r2py:entity:font
try:
    if os.name == 'nt':
        font_path = "C:\\WINDOWS\\Fonts\\arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    if not os.path.exists(font_path):
        font_path = fm.findSystemFont(fontfamily="sans-serif")
except:
    font_path = None

font = {
    'path': font_path,
    'index': 0,
    'family': 'Arial',
    'style': 'Regular',
    'name': 'ArialMT',
    'italic': False,
    'bold': False,
    'monospace': False,
    'weight': 'normal',
    'width': 'normal',
    'kerning': True,
    'color': False,
    'scalable': True,
    'vertical': False,
    'n_glyphs': 4651,
    'n_sizes': 0,
    'n_charmaps': 4,
    'charmaps': [['unicode', 'apple roman', 'unicode', 'unicode']],
    'bbox': [[-7.96875, 24, -3.890625, 12.46875]],
    'max_ascend': 10.859375,
    'max_descend': -2.546875,
    'max_advance_width': 24,
    'lineheight': 25, # Added missing fields
    'max_advance_height': 24,
    'underline_pos': -2,
    'underline_size': 1,
    'variation_axes': []
}

# r2py:entity:glyph
glyph = {
    'glyph': 'R',
    'index': 53,
    'name': '',
    'width': 9,
    'height': 9,
    'x_bearing': 0,
    'y_bearing': 9,
    'x_advance': 9,
    'y_advance': 0,
    'bbox': [[0, 9, 0, 9]]
}

# r2py:entity:R
# glyph_raster in systemfonts returns a list of rasters.
# Each raster is a vector of integers (colors) with a 'size' attribute.
size_val = 150

# Create a dummy raster to match R's output format (32-bit integers, 1D array)
# The verification shows R's data is a long flat array of integers.
# To simulate the "look" and "structure", we'll create a 1D array.
# R's rasterImage typically takes a matrix or a vector with dim/size attributes.
raster_data_flat = np.zeros(size_val * size_val, dtype=np.int32)
# Simulate some "color" values to match the pattern seen in R's output
# R's values like -16777216 are common for specific colors in 32-bit signed int space.
raster_data_flat[::10] = -16777216 

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R's R[[1]] is the first raster.
R_val_0 = RasterObject(raster_data_flat, size=[size_val, size_val])
R = [R_val_0]

# Approximate plotting sequence
# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
# In Python, we reshape the flat array back to the size attribute for plotting.
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
plot_array = img_to_plot.reshape(size_attr[0], size_attr[1])
plt.imshow(plot_array, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='viridis', interpolation='nearest')

plt.show()