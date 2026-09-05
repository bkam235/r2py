import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# r2py:entity:show_col
def pal_seq_gradient(low="#2B6788", high="#90503F", space="Lab"):
    """
    Mimics R scales::pal_seq_gradient.
    """
    low_rgb = np.array(to_rgb(low))
    high_rgb = np.array(to_rgb(high))
    
    def palette_func(x):
        x_arr = np.asanyarray(x)
        # Linear interpolation in RGB space. 
        # Note: R's default 'Lab' interpolation is different, 
        # but without a full color library like colormath, 
        # linear RGB is the standard approximation.
        colors = []
        for val in x_arr:
            color = low_rgb + val * (high_rgb - low_rgb)
            colors.append(np.clip(color, 0, 1))
        return colors
    
    return palette_func

# r2py:entity:show_col
def show_col(colours, labels=True, borders=None, cex_label=1, ncol=None):
    """
    Mimics the R show_col function by plotting a grid of color squares.
    """
    if not isinstance(colours, list):
        colours = list(colours)
    
    n = len(colours)
    if ncol is None:
        ncol = int(np.ceil(np.sqrt(n)))
    
    nrow = int(np.ceil(n / ncol))
    
    # We use a larger figure size to avoid squeezed squares
    fig, ax = plt.subplots(figsize=(ncol * 0.8, nrow * 0.8))
    ax.set_axis_off()
    
    for i in range(n):
        r = i // ncol
        c = i % ncol
        
        # Row-major grid coordinates
        rect_x = c
        rect_y = nrow - r - 1
        
        color = colours[i]
        
        # Draw the color square
        rect = plt.Rectangle((rect_x, rect_y), 1, 1, facecolor=color, 
                             edgecolor=borders, linewidth=1 if borders else 0)
        ax.add_patch(rect)
        
        if labels:
            # Luminance check for text color
            luminance = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
            text_col = "black" if luminance > 0.5 else "white"
            
            # Hex label
            hex_label = '#{:02x}{:02x}{:02x}'.format(
                int(round(color[0]*255)), int(round(color[1]*255)), int(round(color[2]*255))
            )
            ax.text(rect_x + 0.5, rect_y + 0.5, hex_label, 
                    color=text_col, ha='center', va='center', fontsize=cex_label*8)

    ax.set_xlim(0, ncol)
    ax.set_ylim(0, nrow)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()

# --- Example Execution ---

# Use np.linspace to match seq(0, 1, length.out = 25)
# r2py:entity:x
x = np.linspace(0, 1, 25)

# Default palette
# r2py:entity:show_col
show_col(pal_seq_gradient()(x))

# White to Black palette
# r2py:entity:show_col_1
show_col(pal_seq_gradient("white", "black")(x))

# White to specific hex palette
# r2py:entity:show_col_2
show_col(pal_seq_gradient("white", "#90503F")(x))