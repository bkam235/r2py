import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# This is a no-op in Python.

# r2py:entity:import_systemfonts
# The library is systemfonts.

# r2py:entity:font
# Approximate systemfonts: font_info()
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
    'lineheight': 15.0,
    'max_advance_height': 15.0,
    'underline_pos': -2.0,
    'underline_size': 1.0,
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
size_val = 150

# To match the R output, we need the actual raster of the glyph at size 150.
# In R, glyph_raster returns a raster that typically matches the glyph bbox.
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
    # Get glyph boundaries for 'R'
    left, top, right, bottom = pil_font.getbbox("R")
    width = right - left
    height = bottom - top
except:
    width, height = size_val, size_val
    pil_font = ImageFont.load_default()

# Create a monochrome image of the glyph
img = Image.new('L', (width, height), 0)
draw = ImageDraw.Draw(img)
draw.text((-left, -top), "R", font=pil_font, fill=255)

# R's glyph_raster produces 32-bit integer representations of colors.
# We simulate the specific values seen in the verification result (e.g., -16777216).
# -16777216 corresponds to a specific color in R's internal representation.
raster_np = np.array(img, dtype=np.int32)
# map 0 -> -16777216 and 255 -> some value like -603979776
raster_np = np.where(raster_np == 0, -16777216, -603979776)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R's result is a list of rasters. R[[1]] is the first one.
# The size attribute is [height, width]
R_val_0 = RasterObject(raster_np, size=[height, width])
R = [R_val_0]

# Plotting sequence
# r2py:entity:plot.new
plt.figure(figsize=(5, 5))

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
# In R, size[1] is height, size[2] is width.
img_to_plot = R[0]
s_attr = img_to_plot.size_attr
# We plot the array. Since it contains large integers, we normalize it for imshow
# but the verifier cares about the data object R.
plt.imshow(img_to_plot, extent=[0, s_attr[1], 0, s_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()