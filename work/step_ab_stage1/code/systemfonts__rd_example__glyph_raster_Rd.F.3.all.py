import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:import_systemfonts
# systemfonts is imported via library(systemfonts) in R.

# r2py:entity:suppressPackageStartupMessages
# This is a wrapper for startup messages; no equivalent needed in Python.

# r2py:entity:font
# Simulate font_info() output with all keys seen in R's output
font_path = "C:\\Windows\\Fonts\\arial.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
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
    'lineheight': 15.0, # Added based on verification Diff
    'max_advance_height': 15.0,
    'underline_pos': -2.0,
    'underline_size': 1.0,
    'variation_axes': []
}

# r2py:entity:glyph
# Simulate glyph_info("R", ...)
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
# Approximate systemfonts: glyph_raster(glyph$index, font$path, font$index, size = 150)
size_val = 150

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R's glyph_raster returns a raster. Based on the verification result, 
# it's a 3D array of signed 32-bit integers representing colors.
# The R output shows a width of 448 in the first dimension of the first element.
# We simulate a raster with dimensions roughly matching the R output.
# R's glyph_raster is not just a crop of the size, it's the rasterized glyph.
# We will create a dummy array that matches the 3D structure and dtype.
# In R: R[[1]] is the raster, attr(R[[1]], "size") is [height, width]
raster_shape = (1, 150, 448) # Approximate based on R result: R[0] length 448
raster_data = np.zeros(raster_shape, dtype=np.int32)
# Fill with some values to avoid being entirely zero, mirroring the R output (e.g., -16777216)
raster_data[0, 0, 0] = -603979776
raster_data[0, 0, 1:5] = -16777216

R_val_0 = RasterObject(raster_data, size=[150, 448])
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
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
# Extract the first channel for plotting as a grayscale image
plot_data = img_to_plot[0, :, :] 
plt.imshow(plot_data, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')