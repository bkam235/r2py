import numpy as np
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont
from fontTools.pens.t2font import T2FontPen
from fontTools.ttLib.tables._cmap import cmap
from PIL import Image, ImageDraw, ImageFont
import os

# Simulation of systemfonts: font_info()
# In R, font_info() returns info about the default system font.
# We'll pick a common system font path.
if os.name == 'nt':
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
else:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# If the guessed path doesn't exist, try to find any ttf font
if not os.path.exists(font_path):
    import matplotlib.font_manager as fm
    font_path = fm.findSystemFont(fontfamily="sans-serif")

font = {
    'path': font_path,
    'index': 0
}

# Simulation of systemfonts: glyph_info("R", path=..., index=...)
def get_glyph_index(char, font_path):
    font = TTFont(font_path)
    cmap = font['cmap'].getCmap(0)
    return cmap[ord(char)]

glyph_idx = get_glyph_index("R", font['path'])
glyph = {
    'index': glyph_idx
}

# Simulation of systemfonts: glyph_raster(glyph_index, font_path, font_index, size=150)
# glyph_raster returns a raster image of the specific glyph index.
def glyph_raster_sim(glyph_index, font_path, font_index, size=150):
    # We use PIL to render the character corresponding to that glyph index
    # To be precise with glyph indices, we need to find the char associated with it
    font_obj = TTFont(font_path)
    cmap_table = font_obj['cmap'].getCmap(0)
    # Reverse lookup glyph index to character
    char = next((chr(k) for k, v in cmap_table.items() if v == glyph_index), "R")
    
    pil_font = ImageFont.truetype(font_path, size)
    
    # Get bounding box of the character
    # Use a temporary image to determine required canvas size if needed, 
    # but glyph_raster usually targets the glyph itself.
    # We create a canvas large enough to hold the glyph.
    img = Image.new('L', (size * 2, size * 2), 0)
    draw = ImageDraw.Draw(img)
    
    # Draw the character. Since we want the raster of the glyph, we align it.
    # We use a large canvas and then crop or just use the rendered area.
    draw.text((0, 0), char, font=pil_font, fill=255)
    
    # In R, glyph_raster returns the raster data and attaches the size.
    # We'll return a numpy array.
    data = np.array(img, dtype=np.float32)
    
    # We create a wrapper to hold the 'size' attribute as R does
    class RasterArray(np.ndarray):
        def __new__(cls, input_array, size=None):
            obj = np.asarray(input_array).view(cls)
            obj.size_attr = size
            return obj
            
    # R's glyph_raster returns a list of rasters.
    # The size attribute in R usually corresponds to the pixel dimensions.
    # We simulate the size attribute as [height, width]
    res = RasterArray(data, size=[data.shape[0], data.shape[1]])
    return [res]

R = glyph_raster_sim(glyph['index'], font['path'], font['index'], size=150)

# Plotting
plt.figure()
# plot.window(c(0,150), c(0, 150), asp = 1)
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
# R[[1]] is R[0] in Python.
raster_img = R[0]
size_attr = raster_img.size_attr # [height, width]

# Use imshow to place the image. 
# extent=[left, right, bottom, top]
plt.imshow(raster_img, extent=[0, size_attr[1], 0, size_attr[0]], 
           origin='upper', cmap='gray', interpolation='nearest')

plt.show()