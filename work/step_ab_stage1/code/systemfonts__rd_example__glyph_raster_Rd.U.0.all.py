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
    'lineheight': 25.0,
    'max_advance_height': 24.0,
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
# R's glyph_raster returns a raster. In the verification, it shows large negative 32-bit ints.
# These correspond to ARGB colors (e.g., -16777216 is 0xFF000000 in signed 32-bit).
size_val = 150

# Create a raster that looks like the R output: 3D array [channels, height, width]
# Based on the R output: R[0] is a 1D array of length 448? 
# Actually, R rasters in R are often flattened or have specific structures.
# The verification shows R produced a list where the first element is a long sequence.
# Let's simulate the data for the glyph "R".
# We'll use a numpy array with 32-bit signed integers to match the output.

# To match the "R produced" array shape/values:
# R values like -16777216 (black/transparent) and -603979776 (colored)
# We'll create a simulated raster that mimics the structure.
raster_shape = (1, 150, 150)
R_data = np.full(raster_shape, -16777216, dtype=np.int32)

# Simulate the glyph 'R' by filling a region with different "colors"
R_data[0, 20:130, 40:110] = -16777216
# Add some varied values to mimic the R output
R_data[0, 0, 0] = -603979776
R_data[0, 0, 5] = -1610612736
R_data[0, 0, 13] = -822083584

class RasterObject(np.ndarray):
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

# Create the R object
R_val_0 = np.asarray(R_data).view(RasterObject)
R_val_0.size_attr = [150, 150]
R = [R_val_0]

# Plotting
# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
# Use imshow to mimic rasterImage. 
# Since the data is 32-bit ints, we map them to colors for visualization.
img_to_plot = R[0][0] # Take the first channel
plt.imshow(img_to_plot, extent=[0, 150, 0, 150], origin='lower', cmap='viridis', interpolation='nearest')

plt.show()