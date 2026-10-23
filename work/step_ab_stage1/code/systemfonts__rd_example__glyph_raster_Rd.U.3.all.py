import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# r2py:entity:import_systemfonts
# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(func):
    return func

# r2py:entity:font
# Mocking systemfonts::font_info()
font_path = "C:\\Windows\\Fonts\\arial.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if not os.path.exists(font_path):
    import matplotlib.font_manager as fm
    font_path = fm.findSystemFont(fontfamily="sans-serif")

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
    'lineheight': 15, # Added missing keys from R output
    'max_advance_height': 24,
    'underline_pos': -3,
    'underline_size': 1,
    'variation_axes': []
}

# r2py:entity:glyph
# Mocking systemfonts::glyph_info()
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
# Mocking systemfonts::glyph_raster()
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val)
except:
    pil_font = ImageFont.load_default()

# To simulate glyph_raster, we create a mask of the specific character 'R'
# We use a larger canvas to ensure we capture the glyph and then crop/resize if needed, 
# but glyph_raster usually produces the glyph at the requested size.
img = Image.new('L', (size_val * 2, size_val * 2), 0)
draw = ImageDraw.Draw(img)
draw.text((0, 0), "R", font=pil_font, fill=255)

# Crop to the bounding box of the text to simulate a glyph raster
bbox = draw.textbbox((0, 0), "R", font=pil_font)
glyph_crop = img.crop(bbox)
glyph_crop = glyph_crop.resize((size_val, size_val))

# R's glyph_raster returns a list of rasters.
# The values in R's output are specific integer color codes (native 32-bit).
# We map 255 to a value similar to those seen in the R output (e.g., -603979776) and 0 to -16777216.
raster_data = np.array(glyph_crop, dtype=np.int32)
raster_data = np.where(raster_data == 255, -603979776, -16777216)
# Handle the background zeros
raster_data = np.where(np.array(glyph_crop) == 0, -16777216, raster_data)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

R_val_0 = RasterObject(raster_data, size=[size_val, size_val])
R = [R_val_0]

# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
# Use imshow to simulate rasterImage
plt.imshow(img_to_plot, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()