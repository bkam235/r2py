import numpy as np
import matplotlib.pyplot as plt
import freetype
import os

# r2py:entity:import_systemfonts
# systemfonts provides low-level access to font files and glyphs.
# We use freetype-py as the equivalent.

def font_info():
    # Simulate font_info(). Returns a list/dict with path and index.
    # In a real system, this would search for installed fonts.
    if os.name == 'nt':
        path = "C:\\Windows\\Fonts\\arial.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    
    # Ensure path exists, otherwise fallback to a common path
    if not os.path.exists(path):
        # This is a fallback for common Linux environments
        paths = ["/usr/share/fonts/TTF/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
        for p in paths:
            if os.path.exists(p):
                path = p
                break
    
    return {'path': path, 'index': 0}

def glyph_info(char, path, index):
    # Simulate glyph_info(). Returns glyph index for a character.
    face = freetype.Face(path)
    glyph_index = face.get_char_index(ord(char))
    return {'index': glyph_index}

def glyph_raster(glyph_index, font_path, font_index, size=150):
    # Simulate glyph_raster().
    # R's glyph_raster returns a raster image.
    face = freetype.Face(font_path)
    face.set_char_size(size * 64) # freetype uses 1/64th pixels for size
    face.load_glyph(glyph_index)
    bitmap = face.glyph.bitmap
    
    # Extract the raster data
    width = bitmap.width
    rows = bitmap.rows
    buffer = np.array(bitmap.buffer, dtype=np.uint8).reshape(rows, width)
    
    # To match R's structure: a list where the first element is the raster
    # and has a 'size' attribute.
    class RasterArray(np.ndarray):
        def __new__(cls, input_array, size=None):
            obj = np.asarray(input_array).view(cls)
            obj.size_attr = size
            return obj

    # R's rasterImage usually expects values in [0, 1] or specific formats.
    # we normalize to 0-1 for plotting.
    raster_data = buffer.astype(float) / 255.0
    r_obj = RasterArray(raster_data, size=[rows, width])
    return [r_obj]

# Main execution flow
# suppressPackageStartupMessages(library(systemfonts)) is implicit in imports

font = font_info()
glyph = glyph_info("R", path=font['path'], index=font['index'])

R = glyph_raster(glyph['index'], font['path'], font['index'], size=150)

# Plotting
# plot.new()
plt.figure()

# plot.window(c(0,150), c(0, 150), asp = 1)
plt.xlim(0, 150)
plt.ylim(0, 150)
plt.gca().set_aspect('equal')

# rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
# R[[1]] is R[0] in Python.
img_to_plot = R[0]
size_attr = img_to_plot.size_attr # [height, width]
# extent is [left, right, bottom, top]
plt.imshow(img_to_plot, extent=[0, size_attr[1], 0, size_attr[0]], 
           origin='lower', cmap='gray', interpolation='nearest', alpha=1.0)

plt.show()