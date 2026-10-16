import matplotlib.pyplot as plt
import numpy as np

# r2py:entity:backGround
def backGround(xlim=None, ylim=None, bg="white", fg="gray77", horizontal=None, vertical=None, border="black"):
    ax = plt.gca()
    # Get current axes limits to emulate R's U <- c(par("usr"))
    U = ax.get_xlim() + ax.get_ylim()  # (xmin, xmax, ymin, ymax)
    
    # R logic: if (missing(xlim)) xlim <- c(U[1], U[2])
    if xlim is None:
        xlim = [U[0], U[1]]
    if ylim is None:
        ylim = [U[2], U[3]]
    
    if bg is not None:
        bg_list = [bg] if not isinstance(bg, (list, np.ndarray)) else bg
        
        if len(bg_list) == 1:
            # Fill background with single color
            rect = plt.Rectangle((U[0], U[2]), U[1] - U[0], U[3] - U[2], 
                                 facecolor=bg_list[0], edgecolor=border, zorder=-1)
            ax.add_patch(rect)
        elif len(bg_list) > 1:
            if horizontal is None:
                # Vertical bands
                v_vals = [vertical] if (vertical is not None and not isinstance(vertical, (list, np.ndarray))) else (vertical if vertical is not None else [])
                xleft = np.sort(np.unique([xlim[0]] + list(v_vals) + [xlim[1]]))
                NR = len(xleft)
                bcol = np.resize(bg_list, NR)
                for r in range(NR - 1):
                    rect = plt.Rectangle((xleft[r], U[2]), xleft[r+1] - xleft[r], U[3] - U[2], 
                                         facecolor=bcol[r], edgecolor='none', zorder=-1)
                    ax.add_patch(rect)
            else:
                # Horizontal bands
                h_vals = [horizontal] if (horizontal is not None and not isinstance(horizontal, (list, np.ndarray))) else (horizontal if horizontal is not None else [])
                ybot = np.sort(np.unique([ylim[0]] + list(h_vals) + [ylim[1]]))
                NR = len(ybot)
                bcol = np.resize(bg_list, NR)
                for r in range(NR - 1):
                    rect = plt.Rectangle((U[0], ybot[r]), U[1] - U[0], ybot[r+1] - ybot[r], 
                                         facecolor=bcol[r], edgecolor='none', zorder=-1)
                    ax.add_patch(rect)

    if fg is not None:
        if vertical is not None:
            v_vals = [vertical] if not isinstance(vertical, (list, np.ndarray)) else vertical
            for v in v_vals:
                ax.axvline(x=v, color=fg)
        if horizontal is not None:
            h_vals = [horizontal] if not isinstance(horizontal, (list, np.ndarray)) else horizontal
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