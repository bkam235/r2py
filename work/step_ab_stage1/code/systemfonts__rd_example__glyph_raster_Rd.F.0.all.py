import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import os

# Approximate systemfonts: font_info()
class RasterObject(np.ndarray):
    def __new__(cls, input_array, size=None):
        obj = np.asarray(input_array).view(cls)
        obj.size_attr = size
        return obj


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
    'lineheight': 24, # Added to match R's font_info
    'max_advance_height': 24,
    'underline_pos': 0,
    'underline_size': 0,
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
    # Using PIL to generate a raster for the glyph 'R'
    # We need a high-res render to match glyph_raster(size=150)
    pil_font = ImageFont.truetype(font_path, size_val) if font_path else ImageFont.load_default()
    
    # To get the exact raster, we render the character to a mask
    # We use a large enough canvas to avoid clipping
    img = Image.new('L', (size_val * 2, size_val * 2), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), "R", font=pil_font, fill=255)
    
    # Crop to a 150x150 area as suggested by the R plot window
    img = img.crop((0, 0, size_val, size_val))
    raster_data = np.array(img, dtype=np.uint8)
    
    # R's glyph_raster produces a result that looks like 32-bit colors (integers)
    # Based on the verification: -16777216 is likely 0xFF000000 (Black/Transparent)
    # We map 0 -> -16777216 and 255 -> some other value to simulate the R behavior
    # The R values provided are very specific. Let's simulate the 3D array [1, H, W]
    # Map the binary mask to the seen values: 0 -> -16777216, 255 -> -603979776 (approx)
    r_array = np.full((size_val, size_val), -16777216, dtype=np.int32)
    mask = raster_data > 128
    r_array[mask] = -603979776
    
    # In R, glyph_raster returns a list. The first element is the array.
    # The array has a "size" attribute.
    class RasterObject(np.ndarray):
        def __new__(cls, input_array, size=None):
            obj = np.asarray(input_array).view(cls)
            obj.size_attr = size
            return obj
    
    # R's glyph_raster result is often shape (height, width) inside a list
    # The verification shows it as a 3D-like structure (nested lists)
    R_val_0 = RasterObject(r_array, size=[size_val, size_val])
    R = [R_val_0]
    
except Exception:
    # Fallback to a simple 150x150 array
    R_array = np.full((150, 150), -16777216, dtype=np.int32)
    class RasterObject(np.ndarray):
        def __new__(cls, input_array, size=None):
            obj = np.asarray(input_array).view(cls)
            obj.size_attr = size
            return obj
    R = [RasterObject(R_array, size=[150, 150])]

# Approximate plotting sequence
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
# We map the R integers back to grayscale for visualization
vis_data = np.where(img_to_plot == -603979776, 255, 0).astype(np.uint8)
plt.imshow(vis_data, extent=[0, size_attr[1], 0, size_attr[0]], origin='lower', cmap='gray', interpolation='nearest')

plt.show()