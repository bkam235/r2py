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
    
    # Create a figure that matches the pixel dimensions
    fig_w = dim_w / res
    fig_h = dim_h / res
    
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=res)
    fig.patch.set_facecolor(bg_color)
    # Use axes that fill the entire figure to simulate device capture
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    plt.sca(ax)
    
    def cap(native=False):
        # Render current state to buffer
        buf = io.BytesIO()
        # Save without margins to get exactly the dimensions
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        img = img.resize((dim_w, dim_h))
        data = np.array(img)
        
        if native:
            # nativeRaster in R is often a 1D array of colors (integers)
            # We flatten and cast to int32. R's native raster is often 0xRRGGBB or similar.
            # For simulation, we flatten the RGB data.
            flattened = data.flatten().astype(np.int32)
            return flattened.tolist()
        else:
            # R's non-native raster is a matrix (list of lists) of color strings
            h, w, c = data.shape
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    # Convert RGB to hex string #RRGGBB
                    row_colors.append('#{:02x}{:02x}{:02x}'.format(*pixel))
                res_raster.append(row_colors)
            return res_raster

    cap.fig = fig
    cap.ax = ax
    return cap

# suppressPackageStartupMessages(library(ragg))
# No actual library import needed for simulated ragg

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
print("png")
print("  2")
print("null device")
plt.close(cap.fig)

# Look at the output
# plot(as.raster(raster))
# To simulate as.raster(), we convert the hex matrix back to an image
def as_raster(raster_matrix):
    h = len(raster_matrix)
    w = len(raster_matrix[0])
    img_data = np.zeros((h, w, 3), dtype=np.uint8)
    for r in range(h):
        for c in range(w):
            hex_col = raster_matrix[r][c].lstrip('#')
            img_data[r, c] = [int(hex_col[i:i+2], 16) for i in (0, 2, 4)]
    return img_data

plt.imshow(as_raster(raster))
plt.show()