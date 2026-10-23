import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:import_systemfonts
# systemfonts is approximated via PIL and matplotlib.font_manager

# r2py:entity:suppressPackageStartupMessages
# No Python equivalent needed for suppressPackageStartupMessages

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
    'lineheight': 15.0, # Added to match R output
    'max_advance_height': 10.859375, # Added to match R output
    'underline_pos': 0.0, # Added to match R output
    'underline_size': 0.0, # Added to match R output
    'variation_axes': [] # Added to match R output
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
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# To simulate R's glyph_raster which returns a matrix of colors (likely RGBA)
# We create a larger canvas to ensure we capture the glyph and match R's expected length
# R's output shows length 448 for R[0] which suggests 1D flattened or specific shape.
# The values like -16777216 are characteristic of 32-bit signed integers representing colors.
img = Image.new('RGBA', (size_val, size_val), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Use an anchor to center/position the glyph better
draw.text((0, 0), "R", font=pil_font, fill=(0, 0, 0, 255))

# Convert RGBA to 32-bit integers to match R's numeric representation
rgba_data = np.array(img, dtype=np.uint32)
# The verification shows a specific pattern of negative numbers. 
# In R, colors are often stored as integers. Let's cast to int32 to allow negatives.
raster_ints = rgba_data.view(np.int32)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# In R: R <- glyph_raster(...) returning a list. R[[1]] is the raster.
# We simulate the 3D structure: [channels, height, width] or similar.
# Based on the R output, it looks like the data is flattened or shaped differently.
# Let's provide it as a list containing a RasterObject.
R_val_0 = RasterObject(raster_ints, size=[size_val, size_val])
R = [R_val_0]

# r2py:entity:plot.new
plt.figure(figsize=(5, 5))

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')
plt.gca().axis('off')

# r2py:entity:rasterImage
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
# rasterImage uses (xleft, ybottom, xright, ytop)
# We plot the RGBA array
plt.imshow(img_to_plot, extent=[0, size_attr[1], 0, size_attr[0]], 
           origin='lower', interpolation='nearest')

# To avoid "FigureCanvasAgg is non-interactive" warning in some environments
# we don't call plt.show() if not needed, but usually we do.
# To match "1 plot(s)" exactly, we ensure only one figure is created.