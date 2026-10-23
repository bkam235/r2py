import matplotlib.pyplot as plt
import numpy as np

# r2py:entity:backGround
def backGround(bg="white", fg="gray77", xlim=None, ylim=None, horizontal=None, vertical=None, border="black"):
    ax = plt.gca()
    
    # Get current axis limits if not provided
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    
    if xlim is None:
        xlim = list(cur_xlim)
    else:
        xlim = list(xlim)
        ax.set_xlim(xlim)
        
    if ylim is None:
        ylim = list(cur_ylim)
    else:
        ylim = list(ylim)
        ax.set_ylim(ylim)

    # Handle background colors
    if bg is not None:
        bg_list = [bg] if isinstance(bg, str) else list(bg)
        
        if len(bg_list) == 1:
            # Solid background
            rect = plt.Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0], 
                                 facecolor=bg_list[0], edgecolor=border, zorder=-1)
            ax.add_patch(rect)
        else:
            # Striped background
            if horizontal is None and vertical is not None:
                # Vertical bands
                v_vals = [vertical] if np.isscalar(vertical) else list(vertical)
                x_coords = np.sort(np.unique([xlim[0]] + v_vals + [xlim[1]]))
                for i in range(len(x_coords) - 1):
                    color = bg_list[i % len(bg_list)]
                    rect = plt.Rectangle((x_coords[i], ylim[0]), x_coords[i+1] - x_coords[i], 
                                         ylim[1] - ylim[0], facecolor=color, edgecolor='none', zorder=-1)
                    ax.add_patch(rect)
            elif horizontal is not None:
                # Horizontal bands
                h_vals = [horizontal] if np.isscalar(horizontal) else list(horizontal)
                y_coords = np.sort(np.unique([ylim[0]] + h_vals + [ylim[1]]))
                for i in range(len(y_coords) - 1):
                    color = bg_list[i % len(bg_list)]
                    rect = plt.Rectangle((xlim[0], y_coords[i]), xlim[1] - xlim[0], 
                                         y_coords[i+1] - y_coords[i], facecolor=color, edgecolor='none', zorder=-1)
                    ax.add_patch(rect)

    # Foreground lines
    if fg is not None:
        if vertical is not None:
            v_vals = [vertical] if np.isscalar(vertical) else list(vertical)
            for v in v_vals:
                ax.axvline(x=v, color=fg)
        if horizontal is not None:
            h_vals = [horizontal] if np.isscalar(horizontal) else list(horizontal)
            for h in h_vals:
                ax.axhline(y=h, color=fg)

# --- Example 1 ---
plt.figure()
# r2py:entity:plot
plt.plot(0, 0)
# r2py:entity:backGround
backGround(bg="beige", fg="red", vertical=0, horizontal=0)

# --- Example 2 ---
plt.figure()
# r2py:entity:plot_1
plt.plot(0, 0)
# r2py:entity:backGround_1
backGround(bg=["yellow", "green"], fg="red", xlim=[-1, 1], ylim=[-1, 1], horizontal=np.arange(0, 1.1, 0.1))
# r2py:entity:backGround_2
backGround(bg=["yellow", "green"], fg="red", horizontal=np.arange(0, 1.1, 0.1))

plt.show()