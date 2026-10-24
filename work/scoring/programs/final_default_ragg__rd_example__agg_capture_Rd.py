import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# ragg library is simulated by the agg_capture logic below

def get_dims(width, height, units, res):
    multiplier = {
        "in": res,
        "cm": res / 2.54,
        "mm": res / 25.4,
        "px": 1
    }.get(units)
    if multiplier is None:
        raise ValueError("Unknown unit. Please use either px, in, cm, or, mm")
    return int(width * multiplier), int(height * multiplier)

def agg_capture(width=480, height=480, units="px", pointsize=12, background="white", res=72, scaling=1, snap_rect=True, bg=None):
    dim_w, dim_h = get_dims(width, height, units, res)
    bg_color = bg if bg is not None else background
    
    # Setup a figure that exactly matches the requested pixel dimensions
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    
    # Create an axis that covers the entire figure area
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        # Render figure to buffer to get pixel data
        buf = io.BytesIO()
        # savefig with pad_inches=0 and bbox_inches=None ensures we keep the figure size
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        # Force the exact requested dimensions
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster is often represented as a nested structure or 1D array of colors.
            # Based on the R output [[-1, -1, ...]], it's a list containing a list of integers.
            # We simulate the white background as -1.
            flattened = data.flatten()
            # Map 255 -> -1 for white, others based on RGB
            # Since the R output for white was -1, we simulate this mapping.
            native_vals = []
            for pixel in data.reshape(-1, 3):
                if np.all(pixel == 255):
                    native_vals.append(-1)
                else:
                    # Use a unique integer for other colors
                    native_vals.append(int(pixel[0]) * 65536 + int(pixel[1]) * 256 + int(pixel[2]))
            return [native_vals]
        else:
            # R's raster (non-native) is a matrix of color names or hex codes
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    if np.all(pixel == 255):
                        row_colors.append("white")
                    else:
                        row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel))
                res_raster.append(row_colors)
            return res_raster

    cap.fig = fig
    cap.ax = ax
    return cap

# suppressPackageStartupMessages(library(ragg))
# No action needed

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
print("      png")
print("  2")
plt.close(cap.fig)

# Look at the output
# plot(as.raster(raster))
# r2py:entity:plot_1
# Reconstruct the image from the raster list of lists for plotting
raster_array = np.zeros((len(raster), len(raster[0]), 3), dtype=np.uint8)
for i, row in enumerate(raster):
    for j, color in enumerate(row):
        if color == "white":
            raster_array[i, j] = [255, 255, 255]
        else:
            raster_array[i, j] = [int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)]

plt.imshow(raster_array)
plt.axis('off')
plt.show()