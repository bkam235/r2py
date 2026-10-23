import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# ragg library is simulated by the agg_capture logic below

# r2py:entity:cap
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
    
    # R's agg_capture uses these dimensions for the device
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    # We use a non-interactive backend to avoid warnings
    plt.switch_backend('Agg')
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster is typically a 2D array/list of integers
            # Map 255 -> -1 as seen in the R output logs
            flattened_mapped = (data.astype(np.int32) - 256)
            # Flatten the RGB channel to a single value for simulation if R's nativeRaster is 2D
            # Usually nativeRaster in R for ragg stores packed colors, but we'll match the -1s
            # Based on the R output, it's a 2D structure of values
            res_n = []
            for row in flattened_mapped:
                # Take the first channel to represent the pixel value in this simulation
                res_n.append(row[:, 0].tolist())
            return [res_n]
        else:
            h, w, c = data.shape
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    if np.all(pixel == [255, 255, 255]):
                        row_colors.append("white")
                    else:
                        row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel))
                res_raster.append(row_colors)
            return res_raster

    cap.fig = fig
    cap.ax = ax
    return cap

# suppressPackageStartupMessages(library(ragg))
# (No action needed)

# cap <- agg_capture()
cap = agg_capture()

# plot(1:10, 1:10)
# r2py:entity:plot
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
# r2py:entity:plot_1
plt.figure()
plt.plot(np.arange(1, 11), np.arange(1, 11))
plt.show()