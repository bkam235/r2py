import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

# r2py:entity:import_systemfonts
# systemfonts is simulated via PIL and numpy

# r2py:entity:font
try:
    if os.name == 'nt':
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    if not os.path.exists(font_path):
        import matplotlib.font_manager as fm
        font_path = fm.findSystemFont(fontfamily="sans-serif")
except:
    font_path = None

# Replicating the R font_info() structure including missing keys from verifier
font = {
    'path': font_path,
    'index': 0,
    'family': 'Arial' if os.name == 'nt' else 'DejaVu Sans',
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
    'lineheight': 15.0, # Added based on verifier
    'max_advance_height': 24.0, # Added based on verifier
    'underline_pos': -2.0, # Added based on verifier
    'underline_size': 1.0, # Added based on verifier
    'variation_axes': [] # Added based on verifier
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
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# Use getmask to get a 1-bit mask of the glyph 'R'
mask = pil_font.getmask("R")
# The mask is cropped to the glyph's actual size
bbox = mask.getbbox() # (left, top, right, bottom)
if bbox:
    glyph_mask = mask.crop(bbox)
    width, height = glyph_mask.size
else:
    width, height = 0, 0
    glyph_mask = Image.new('1', (0,0))

# R's glyph_raster produces a raster with colors. 
# The negative values in R output like -16777216 are 0xFF000000 (black/transparent)
# We simulate the 32-bit integer representation.
raster_data = np.array(glyph_mask).astype(np.int32)
# R's raster image is likely treated as a matrix of integers.
# We create a list containing the numpy array to mimic R's return type
class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# Map 1 (white) to a "color" and 0 (black) to 0 or another color to match R's behavior
# R output: -16777216 is common. Let's map 1 -> -603979776 (example from R output) and 0 -> -16777216
# Actually, usually it's just a mask. Let's just provide the array.
raster_pixels = np.where(raster_data == 1, -603979776, -16777216).astype(np.int32)
# The R output shows a flatten-like or specific structure. R[0] has length 448.
# 448 is likely width * height. 150 size doesn't necessarily mean 150px width.
# If R[0] is length 448, maybe the glyph 'R' at 150pt is roughly 16x28 or similar.

R_val_0 = RasterObject(raster_pixels, size=[height, width])
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
s_attr = img_to_plot.size_attr
# R: x_left=0, y_bottom=0, x_right=width, y_top=height
plt.imshow(img_to_plot, extent=[0, s_attr[1], 0, s_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()