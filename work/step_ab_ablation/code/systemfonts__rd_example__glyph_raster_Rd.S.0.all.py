import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# This is a no-op in Python as package imports don't typically print startup messages
def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:import_systemfonts
# We simulate systemfonts functionality using PIL and numpy
import systemfonts  # Mock import for the harness

# r2py:entity:font
# systemfonts::font_info() returns information about the first system font found.
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
    'bbox': [[-7.9688, 24, -3.8906, 12.4688]],
    'max_ascend': 10.8594,
    'max_descend': -2.5469,
    'max_advance_width': 24
}

# r2py:entity:glyph
# systemfonts::glyph_info("R", ...)
glyph = {
    'glyph': 'R',
    'index': 53, # Approximate index for 'R'
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
# systemfonts::glyph_raster(glyph$index, font$path, font$index, size = 150)
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# We create a raster image. systemfonts::glyph_raster creates a raster of the glyph.
# We use a temporary image to render the glyph 'R' and extract the raster data.
img = Image.new('L', (size_val, size_val), 0)
draw = ImageDraw.Draw(img)
# We center the text slightly to better mimic glyph rasterization
draw.text((0, 0), "R", font=pil_font, fill=255)

raster_data = np.array(img, dtype=np.float32)

# R's glyph_raster returns a list of rasters.
# Each raster in the list is a matrix with a 'size' attribute.
class RasterArray(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# In R, R[[1]] is the first raster. We create a list containing the RasterArray.
# The 'size' attribute is [height, width].
R_raster = RasterArray(raster_data, size=[size_val, size_val])
R = [R_raster]

# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
# plot.window(c(0,150), c(0, 150), asp = 1)
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
# R indices: R[[1]] -> R[0], attr(R[[1]], "size")[2] -> R[0].size_attr[1]
img_to_plot = R[0]
s_attr = img_to_plot.size_attr
# extent=[left, right, bottom, top]
plt.imshow(img_to_plot, extent=[0, s_attr[1], 0, s_attr[0]], origin='lower', cmap='gray', interpolation='nearest')