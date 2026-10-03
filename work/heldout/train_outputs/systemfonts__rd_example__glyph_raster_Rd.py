import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# Approximate systemfonts: font_info()
# R's font_info() returns a list with attributes. 
# In Python, we use a dictionary to simulate this.
# r2py:entity:font
try:
    # Attempt to find a standard system font path (cross-platform)
    if os.name == 'nt':
        font_path = "C:\\Windows\\Fonts\\arial.ttf"
    else:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    if not os.path.exists(font_path):
        # Fallback to any found font
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
# R's glyph_raster returns a list where the first element is the raster and has a 'size' attribute
# We use PIL to create the raster image of the glyph 'R'
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# Create image for "R"
img = Image.new('L', (size_val, size_val), 0)
draw = ImageDraw.Draw(img)
# Use a basic anchor to place the glyph
draw.text((0, 0), "R", font=pil_font, fill=255)

# Convert to numpy array. R's raster data is often stored as integers (colors)
# In the verification, R produced large negative numbers (native 32-bit colors)
# We simulate the array and add the 'size' attribute as a custom property.
raster_data = np.array(img, dtype=np.int32)
# Simulating the 3D structure R's raster objects often have [channels, height, width]
R_raster = [raster_data[np.newaxis, ...]] 

# Assign 'size' attribute to the first element to mirror attr(R[[1]], "size")
# In Python, we can attach attributes to numpy arrays or use a custom class.
class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

# R[[1]] in the source is the raster.
R_val_0 = RasterObject(raster_data, size=[size_val, size_val])
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
# Python's imshow uses (extent) to define coordinates [left, right, bottom, top]
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
plt.imshow(img_to_plot, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()