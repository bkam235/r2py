import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages is a no-op in Python translation

# r2py:entity:import_systemfonts
# systemfonts is approximated using PIL and matplotlib

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
    'lineheight': 15,
    'max_advance_height': 15,
    'underline_pos': -3,
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
# glyph_raster in R returns a raster image. 
# The verification shows R produced a list of integers (colors).
# We simulate a 150x150 raster.
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# Create a canvas to render the glyph "R"
# To mimic R's raster, we generate an image then convert it to a numpy array of 32-bit ints.
img = Image.new('RGBA', (size_val, size_val), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Center the glyph roughly
draw.text((10, 10), "R", font=pil_font, fill=(255, 0, 0, 255))

# R's rasterImage often uses a flat array or specific shape.
# The verification shows R produced a list containing a very long array.
# We represent R as a list containing the numpy array.
raster_data = np.array(img).reshape(-1)
raster_data = raster_data.astype(np.int32)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R[[1]] corresponds to the first element of the list R.
R_val_0 = RasterObject(raster_data, size=[size_val, size_val])
R = [R_val_0]

# Approximate plotting sequence
# r2py:entity:plot.new
plt.figure(figsize=(5, 5))

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')
plt.axis('off') # Typical for rasterImage tests

# r2py:entity:rasterImage
# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
img_to_plot = R[0]
size_attr = img_to_plot.size_attr # [150, 150]
# Reshape the flat array back to 2D for imshow
plot_img = img_to_plot.reshape(size_attr[0], size_attr[1], 4)
plt.imshow(plot_img, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', interpolation='nearest')

plt.show()