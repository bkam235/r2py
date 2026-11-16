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

    def cap(native=False):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), bbox_inches=None, pad_inches=0)
        buf.seek(0)
        img = Image.open(buf).convert('RGB')
        data = np.array(img)

        if native:
            r = data[:, :, 0].astype(np.int64)
            g = data[:, :, 1].astype(np.int64)
            b = data[:, :, 2].astype(np.int64)
            a = np.full_like(r, 255)
            packed = (a << 24) | (b << 16) | (g << 8) | r
            packed = packed.astype(np.uint32).astype(np.int32)
            return packed.tolist()
        else:
            res_raster = []
            for row in data:
                row_colors = []
                for pixel in row:
                    if np.all(pixel == [255, 255, 255]):
                        row_colors.append("white")
                    else:
                        row_colors.append('#{:02x}{:02x}{:02x}'.format(int(pixel[0]), int(pixel[1]), int(pixel[2])))
                res_raster.append(row_colors)
            return res_raster

    cap.fig = fig
    return cap

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
plt.close(cap.fig)

# Look at the output
# r2py:entity:plot_1
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.axis('off')
_rarr = np.array(raster_n, dtype=np.int32)
_u = _rarr.astype(np.int64) & 0xFFFFFFFF
_r = (_u & 0xFF).astype(np.uint8)
_g = ((_u >> 8) & 0xFF).astype(np.uint8)
_b = ((_u >> 16) & 0xFF).astype(np.uint8)
_rgb = np.stack([_r, _g, _b], axis=-1)
ax2.imshow(_rgb)
plt.show()
