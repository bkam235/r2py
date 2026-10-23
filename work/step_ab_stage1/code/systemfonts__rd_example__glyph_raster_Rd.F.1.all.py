import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# This is a no-op in Python.

# r2py:entity:import_systemfonts
# The systemfonts package is approximated using PIL and numpy.

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

# Updated to match R's font_info() keys exactly
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
    'lineheight': 15.0, # Added missing key
    'max_advance_height': 24.0, # Added missing key
    'underline_pos': 0.0, # Added missing key
    'underline_size': 0.0, # Added missing key
    'variation_axes': [] # Added missing key
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
# Approximate systemfonts: glyph_raster(glyph$index, font$path, font$index, size = 150)
size_val = 150

# To simulate glyph_raster, we render the glyph "R" using PIL
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# glyph_raster typically returns the raster of the specific glyph
# We create a temporary image to find the glyph's bounding box
temp_img = Image.new('L', (size_val * 2, size_val * 2), 0)
temp_draw = ImageDraw.Draw(temp_img)
temp_draw.text((0, 0), "R", font=pil_font, fill=255)

# Crop to the actual ink (non-zero) pixels to simulate the glyph-specific raster
bbox = temp_img.getbbox()
if bbox:
    glyph_img = temp_img.crop(bbox)
else:
    glyph_img = Image.new('L', (size_val, size_val), 0)

# Convert to numpy array and flatten to match R's raster internal representation
raster_data = np.array(glyph_img, dtype=np.int32).flatten()

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R's glyph_raster returns a list where R[[1]] is the raster
# The size attribute in R for rasterImage is [height, width]
actual_h, actual_w = glyph_img.size[1], glyph_img.size[0]
R_val_0 = RasterObject(raster_data, size=[actual_h, actual_w])
R = [R_val_0]

# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
img_to_plot = R[0]
size_attr = img_to_plot.size_attr # [height, width]
# Reshape the flat array back to 2D for plotting
plot_data = img_to_plot.reshape(size_attr[0], size_attr[1])
plt.imshow(plot_data, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()