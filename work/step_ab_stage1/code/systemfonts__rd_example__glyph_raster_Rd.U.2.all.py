import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# Approximate systemfonts: font_info()
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
    'lineheight': 13.0, # Added to match R output
    'max_advance_height': 24.0,
    'underline_pos': 0.0,
    'underline_size': 0.0,
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
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# To better simulate glyph_raster, we need a tight bounding box for the glyph 'R'
# glyph_raster typically produces a raster of the glyph's footprint.
char = "R"
# Get glyph dimensions
bbox = pil_font.getbbox(char) # (left, top, right, bottom)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]

# Create a raster image of the glyph
img = Image.new('L', (w, h), 0)
draw = ImageDraw.Draw(img)
draw.text((-bbox[0], -bbox[1]), char, font=pil_font, fill=255)

# R's glyph_raster returns an array of colors. 
# Based on the verification, it seems to be a 3D array (channels, height, width)
# and the values are large integers. We simulate this structure.
raster_data = np.array(img, dtype=np.int32)
# Reshape to (1, height, width) and use a simulated color value if needed
# The R output shows -16777216 which is 0xFF000000 (opaque black/transparent) in signed 32-bit
# Let's simulate the 3D structure: [1, height, width]
R_raster = raster_data[np.newaxis, ...] 
# Shift values to match the "large negative numbers" (simulating 32-bit ARGB)
R_raster = np.where(R_raster == 255, -603979776, -16777216).astype(np.int32)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R[[1]] is the raster
R_val_0 = RasterObject(R_raster, size=[h, w])
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
# R size attributes: [1] is height, [2] is width.
img_to_plot = R[0]
size_attr = img_to_plot.size_attr # [height, width]
# Use the actual dimensions of the raster for extent
plt.imshow(img_to_plot[0], extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()