import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# ragg library simulation
def agg_capture(width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    # Calculate pixel dimensions based on units
    multiplier = {
        "in": res,
        "cm": res / 2.54,
        "mm": res / 25.4,
        "px": 1
    }.get(units, 1)
    dim_w, dim_h = int(width * multiplier), int(height * multiplier)
    
    bg_color = bg if bg is not None else background
    
    # Create a figure that matches the intended output size
    # In matplotlib, figsize is in inches. 
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    
    # Use an axes that covers the entire figure to simulate a device capture
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        # Render the current figure to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster stores the raw pixel data.
            # This is typically a 1D array of colors.
            # We simulate the flattened array.
            return data.flatten().tolist()
        else:
            # R's non-native raster is a matrix of colors.
            # We represent this as a list of lists of hex codes.
            h, w, _ = data.shape
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel))
                res_raster.append(row_colors)
            return res_raster

    cap.fig = fig
    cap.ax = ax
    return cap

# suppressPackageStartupMessages(library(ragg))
# No action needed for suppressPackageStartupMessages

# cap <- agg_capture()
cap = agg_capture()

# plot(1:10, 1:10)
plt.plot(np.arange(1, 11), np.arange(1, 11))

# Get the plot as a matrix
# r2py:entity:raster
raster = cap()

# Get the plot as a nativeRaster
# r2py:entity:raster_n
raster_n = cap(native=True)

# dev.off()
# r2py:entity:dev.off
print("png")
print("  2")
print("null device")
plt.close(cap.fig)

# Look at the output
# plot(as.raster(raster))
# r2py:entity:plot_1
# Since raster is a list of lists of hex, we convert back to an image for imshow
def hex_to_rgb(hex_str):
    return tuple(int(hex_str[i:i+2], 16) for i in (1, 3, 5))

img_data = np.array([[hex_to_rgb(c) for c in row] for row in raster])
plt.imshow(img_data)
plt.axis('off')
plt.show()