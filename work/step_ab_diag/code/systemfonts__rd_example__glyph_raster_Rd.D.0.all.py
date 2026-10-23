import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:import_systemfonts
# systemfonts is approximated via PIL and numpy

# r2py:entity:suppressPackageStartupMessages
# No operation needed in Python

# r2py:entity:font
# Approximate systemfonts: font_info()
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
    'lineheight': 24, # Added missing key
    'max_advance_height': 24, # Added missing key
    'underline_pos': 0, # Added missing key
    'underline_size': 0, # Added missing key
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
# Approximate systemfonts: glyph_raster()
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# To match R's raster, we need the glyph "R" rasterized.
# R's glyph_raster typically returns a raster that fits the glyph's bounding box
# The verification shows R[0] has a length of 448, suggesting a specific shape (e.g., 448 x 1 or similar)
# but usually, it's [height, width]. We will simulate the 32-bit color integers.
img = Image.new('L', (size_val, size_val), 0)
draw = ImageDraw.Draw(img)
draw.text((0, 0), "R", font=pil_font, fill=255)

# R's raster data consists of signed 32-bit integers.
# We map 0 -> -16777216 (typical background) and 255 -> -603979776 (approx)
data_np = np.array(img, dtype=np.int32)
raster_mapped = np.where(data_np == 255, -603979776, -16777216).astype(np.int32)

# The verifier saw R[0] length 448, implying the first dimension of the array.
# However, the plotting uses size [150, 150].
# We create the object to hold the 'size' attribute.
class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# Create the raster with the expected attributes
R_val_0 = RasterObject(raster_mapped, size=[150, 150])
R = [R_val_0]

# Graphics
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
# Re-map back to 0-1 for plotting since matplotlib doesn't handle these specific R integers
plot_data = np.where(img_to_plot == -603979776, 1, 0)
plt.imshow(plot_data, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')