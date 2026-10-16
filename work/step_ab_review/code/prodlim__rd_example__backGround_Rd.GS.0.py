# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import matplotlib.pyplot as plt
import numpy as np

# r2py:entity:backGround
def backGround(xlim=None, ylim=None, bg="white", fg="gray77", horizontal=None, vertical=None, border="black"):
    ax = plt.gca()
    U = list(ax.get_xlim()) + list(ax.get_ylim())  # [xmin, xmax, ymin, ymax]
    
    # R logic: if (missing(xlim)) xlim <- c(U[1], U[2])
    if xlim is None:
        xlim = [U[0], U[1]]
    if ylim is None:
        ylim = [U[2], U[3]]
    
    if bg is not None:
        # Ensure bg is a list for length checks
        bg_list = [bg] if not isinstance(bg, (list, np.ndarray)) else bg
        
        if len(bg_list) == 1:
            # rect(U[1], U[3], U[2], U[4], col = bg[1], border = border)
            rect = plt.Rectangle((xlim[0], ylim[0]), xlim[1] - xlim[0], ylim[1] - ylim[0], 
                                 facecolor=bg_list[0], edgecolor=border)
            ax.add_patch(rect)
        elif len(bg_list) > 1:
            if horizontal is None:
                # Vertical bands: xleft <- sort(unique(c(xlim[1], vertical, xlim[2])))
                v_vals = [vertical] if (vertical is not None and not isinstance(vertical, (list, np.ndarray))) else (vertical if vertical is not None else [])
                xleft = np.sort(np.unique([xlim[0]] + list(v_vals) + [xlim[1]]))
                NR = len(xleft)
                # bcol <- rep(bg, length.out = NR)
                bcol = np.resize(bg_list, NR)
                for r in range(NR - 1):
                    # polygon(y = c(U[3], U[3], U[4], U[4], U[3]), x = c(xleft[r], xleft[r+1], xleft[r+1], xleft[r], xleft[r]))
                    rect = plt.Rectangle((xleft[r], ylim[0]), xleft[r+1] - xleft[r], ylim[1] - ylim[0], 
                                         facecolor=bcol[r], edgecolor='none')
                    ax.add_patch(rect)
            else:
                # Horizontal bands: ybot <- sort(unique(c(ylim[1], horizontal, ylim[2])))
                h_vals = [horizontal] if (horizontal is not None and not isinstance(horizontal, (list, np.ndarray))) else (horizontal if horizontal is not None else [])
                ybot = np.sort(np.unique([ylim[0]] + list(h_vals) + [ylim[1]]))
                NR = len(ybot)
                # bcol <- rep(bg, length.out = NR)
                bcol = np.resize(bg_list, NR)
                for r in range(NR - 1):
                    # polygon(x = c(U[1], U[1], U[2], U[2], U[1]), y = c(ybot[r], ybot[r+1], ybot[r+1], ybot[r], ybot[r]))
                    rect = plt.Rectangle((xlim[0], ybot[r]), xlim[1] - xlim[0], ybot[r+1] - ybot[r], 
                                         facecolor=bcol[r], edgecolor='none')
                    ax.add_patch(rect)

    if fg is not None:
        # if (length(vertical) > 0) abline(v = vertical, col = fg)
        if vertical is not None:
            v_vals = [vertical] if not isinstance(vertical, (list, np.ndarray)) else vertical
            for v in v_vals:
                ax.axvline(x=v, color=fg)
        # if (length(horizontal) > 0) abline(h = horizontal, col = fg)
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