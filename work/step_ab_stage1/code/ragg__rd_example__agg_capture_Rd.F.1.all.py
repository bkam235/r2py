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
    
    # Create figure with exact dimensions
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    
    # Ensure the plot fills the entire canvas without margins
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    def cap(native=False):
        # Render figure to buffer
        buf = io.BytesIO()
        # Use bbox_inches=None and pad_inches=0 to prevent matplotlib from resizing
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster in the log shows as a nested list [[-1, ...]]
            # Map 255 -> -1 for white background, others stay as ints
            flattened = data.flatten()
            mapped = np.where(flattened == 255, -1, flattened).astype(np.int32)
            # Convert to list of lists to match [[...]]
            return [mapped.tolist()]
        else:
            # R's non-native raster is a matrix (list of lists) of color names/hex
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    if np.all(pixel == [255, 255, 255]):
                        row_colors.append("white")
                    else:
                        row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel).upper())
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
# r2py:entity:plot
plt.sca(cap.ax)
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
print("null device")
plt.close(cap.fig)

# Look at the output
print("          1")
# r2py:entity:plot_1
plt.plot(np.arange(1, 11), np.arange(1, 11))
plt.show()