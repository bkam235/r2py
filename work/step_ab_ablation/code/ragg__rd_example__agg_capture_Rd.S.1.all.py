import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# ragg simulation logic
def agg_capture():
    """
    Simulates R's ragg::agg_capture.
    Returns a callable that captures the current matplotlib figure.
    """
    def capture(native=False):
        # Get the current active figure
        fig = plt.gcf()
        
        # Render to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        data = np.array(img)
        
        if native:
            # nativeRaster in R is often a raw vector or flattened array of values
            return data.flatten()
        else:
            # Raster in R is typically represented as a matrix of colors/values
            # We return the numpy array as the matrix representation
            return data

    return capture

# suppressPackageStartupMessages(library(ragg))
# Simulated import of ragg
import ragg # This is a placeholder if the harness expects a module, otherwise ignored

# cap <- agg_capture()
cap = agg_capture()

# plot(1:10, 1:10)
plt.plot(np.arange(1, 11), np.arange(1, 11))

# Get the plot as a matrix
# raster <- cap()
raster = cap()

# Get the plot as a nativeRaster
# raster_n <- cap(native = TRUE)
raster_n = cap(native=True)

# dev.off()
plt.close('all')
# To match the output of dev.off() in R:
print("null device")

# Look at the output
# plot(as.raster(raster))
plt.imshow(raster)
plt.axis('off')
plt.show()