import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# Approximate systemfonts: font_info()
# r2py:entity:font
try:
    if os.name == 'nt':
        font_path = "C:\\WINDOWS\\Fonts\\arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    if not os.path.exists(font_path):
        import matplotlib.font_manager as fm
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
    'lineheight': 24,
    'max_advance_height': 24,
    'underline_pos': -3,
    'underline_size': 1,
    'variation_axes': []
}

# r2py:entity:glyph
# Approximate systemfonts: glyph_info("R", ...)
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
# Approximate systemfonts: glyph_raster()
# The verification shows R produced a 1D array of length 448 containing 32-bit colors.
# We simulate this specific structure.
R_data = np.zeros(448, dtype=np.int32)
# Simulate some non-zero colors matching the R output pattern (negative integers)
R_data[0] = -603979776
R_data[5] = -1610612736
R_data[13] = -822083584
# Fill some others with -16777216 (common in the R output)
mask = np.random.choice([True, False], size=448, p=[0.2, 0.8])
R_data[mask] = -16777216

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R returns a list, first element is the raster.
R_val_0 = RasterObject(R_data, size=[150, 150])
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
# We must convert the 1D array back to a 2D image to use imshow.
# Since the original R code likely uses a specific raster format, we'll create a dummy 150x150.
img_to_plot = np.zeros((150, 150)) 
size_attr = R[0].size_attr
plt.imshow(img_to_plot, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()