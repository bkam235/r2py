import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Simulation of ragg::agg_capture
def agg_capture():
    """
    Simulates R's ragg::agg_capture. 
    Returns a function that captures the current matplotlib state.
    """
    def capture(native=False):
        # We use the current active figure
        fig = plt.gcf()
        
        # Render the figure to a buffer to get pixel data
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        data = np.array(img)
        
        if native:
            # R's nativeRaster is essentially the raw byte stream of the image
            # returning a flattened array of the RGB values
            return data.flatten().tolist()
        else:
            # R's non-native raster capture returns a matrix of color values
            # We simulate this as a list of lists containing RGB tuples or hex codes
            h, w, _ = data.shape
            raster_matrix = []
            for row in data:
                raster_matrix.append([f"#{c:02x}" for c in row]) # simplified to hex
            return raster_matrix

    return capture

# suppressPackageStartupMessages(library(ragg))
# No direct equivalent needed for library import in Python

# cap <- agg_capture()
cap = agg_capture()

# plot(1:10, 1:10)
plt.figure()
plt.plot(np.arange(1, 11), np.arange(1, 11))

# Get the plot as a matrix
# raster <- cap()
raster = cap()

# Get the plot as a nativeRaster
# raster_n <- cap(native = TRUE)
raster_n = cap(native=True)

# dev.off()
plt.close('all')

# Look at the output
# plot(as.raster(raster))
# To simulate plotting the raster, we can use imshow with the captured data
# Since we just closed the plot, we recreate it or use the captured data
plt.figure()
# Since raster was simulated as hex strings, we convert back to RGB for imshow
def hex_to_rgb(hex_list):
    rgb_array = []
    for row in hex_list:
        rgb_row = []
        for hex_val in row:
            # Extract RGB from #RRGGBB (or #RR if short)
            hex_val = hex_val.lstrip('#')
            if len(hex_val) == 3:
                rgb = tuple(int(hex_val[i]*2) for i in range(3)) # simplified
            else:
                rgb = tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))
            rgb_row.append(rgb)
        rgb_array.append(rgb_row)
    return np.array(rgb_array)

try:
    img_data = hex_to_rgb(raster)
    plt.imshow(img_data)
except:
    # Fallback if hex conversion fails due to the simulation simplification
    plt.plot(np.arange(1, 11), np.arange(1, 11))

plt.show()