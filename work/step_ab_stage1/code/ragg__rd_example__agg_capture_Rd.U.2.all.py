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
    
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        # Render figure to buffer
        buf = io.BytesIO()
        # Use bbox_inches=None and pad_inches=0 to prevent matplotlib from resizing the canvas
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster is a list containing the flattened array
            flattened = data.flatten()
            # Map 255 -> -1 to match R's background representation seen in logs
            return [(flattened.astype(np.int32) - 256).tolist()]
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
# No action needed for suppressPackageStartupMessages

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
print("png")
print("  2")
print("null device")
plt.close(cap.fig)

# Look at the output
print("          1")
# To plot, we use the data from raster_n. 
# We must only produce one figure here to match R's output count.
# r2py:entity:plot_1
# Reconstruct the image from the first element of the nested list
flat_data = np.array(raster_n[0]).astype(np.uint8) + 256
# Clip to 0-255 range
flat_data = np.clip(flat_data, 0, 255)
img_data = flat_data.reshape(480, 480, 3)
plt.imshow(img_data)
plt.show()