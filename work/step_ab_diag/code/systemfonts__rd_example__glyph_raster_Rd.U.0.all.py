import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

# Approximate systemfonts: font_info()
# r2py:entity:font
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
    'lineheight': 12.0,
    'max_advance_height': 12.0,
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
# R's glyph_raster returns a raster for a specific glyph index.
# The verification shows R producing values like -16777216 (which is 0xFF000000 in signed 32-bit)
# and -603979776. These are typically ARGB colors.
size_val = 150
try:
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
except:
    pil_font = ImageFont.load_default()

# To mimic glyph_raster, we render the character and crop to the glyph's bounding box
# In a real translation of systemfonts, this would use FreeType's glyph rendering.
img = Image.new('L', (size_val * 2, size_val * 2), 0)
draw = ImageDraw.Draw(img)
draw.text((0, 0), "R", font=pil_font, fill=255)

# Get bounding box of the rendered text to crop to the "glyph"
bbox = img.getbbox()
if bbox:
    glyph_img = img.crop(bbox)
    # Resize to roughly fit the 150x150 request if necessary, 
    # though glyph_raster's size argument usually controls the font size.
    glyph_img = glyph_img.resize((150, 150), Image.Resampling.LANCZOS)
else:
    glyph_img = Image.new('L', (150, 150), 0)

raster_data = np.array(glyph_img, dtype=np.int32)
# Convert grayscale to the specific 32-bit signed integers R uses for colors
# R's -16777216 is often a background color.
# We map 0 -> -16777216 and 255 -> some other value to match the structure.
final_raster = np.where(raster_data == 0, -16777216, -603979776).astype(np.int32)

class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj

R_val_0 = RasterObject(final_raster, size=[150, 150])
R = [R_val_0]

# Approximate plotting sequence
# r2py:entity:plot.new
plt.figure()

# r2py:entity:plot.window
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# r2py:entity:rasterImage
img_to_plot = R[0]
size_attr = img_to_plot.size_attr
# We map the R colors back to grayscale for imshow
plot_data = np.where(img_to_plot == -16777216, 0, 255)
plt.imshow(plot_data, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()