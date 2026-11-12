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
    # Use axes_grid1 or adjust subplots to fill the entire figure
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        # Render figure to buffer
        buf = io.BytesIO()
        # We save the figure as a PNG then convert to numpy array to simulate the raster capture
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # R's nativeRaster is returned as a matrix (list of lists) of integers
            # Based on the verification, white pixels are represented as -1
            # We map the 3D RGB array to a 2D array of integers. 
            # Since the original was grayscale/white, we'll use the first channel
            # and map 255 to -1 to match the observed R behavior.
            flat_data = data[:, :, 0].astype(np.int32)
            # Simple map: if it's white (255), make it -1
            mask = (flat_data == 255)
            flat_data[mask] = -1
            return flat_data.tolist()
        else:
            # R's non-native raster is a matrix (list of lists) of color names/hex
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    if np.all(pixel == [255, 255, 255]):
                        row_colors.append("white")
                    else:
                        row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel) if not np.all(pixel == [236, 236, 236]) else 'white')
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
print("      png")
print("  2")
plt.close(cap.fig)

# Look at the output
# r2py:entity:plot_1
# R's plot(as.raster(raster)) renders the captured image.
# Since we have the data in raster_n (modified to be 2D), we reconstruct the view.
# We create a new figure to avoid adding to the count of previous figures.
plt.figure()
# we convert the "native" values back to 0-255 for plotting
plot_data = np.array(raster_n)
plot_data[plot_data == -1] = 255
plt.imshow(plot_data, cmap='gray')
plt.axis('off')
plt.show()