# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import matplotlib.pyplot as plt
import numpy as np

# r2py:entity:backGround
def backGround(xlim=None, ylim=None, bg="white", fg="gray77", horizontal=None, vertical=None, border="black"):
    ax = plt.gca()
    
    # Get current limits if not provided
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    
    # R: if (missing(xlim)) xlim <- c(U[1], U[2])
    final_xlim = xlim if xlim is not None else list(cur_xlim)
    final_ylim = ylim if ylim is not None else list(cur_ylim)
    
    if bg is not None:
        bg_list = [bg] if not isinstance(bg, (list, np.ndarray)) else list(bg)
        
        if len(bg_list) == 1:
            # Fill the entire specified area
            rect = plt.Rectangle((final_xlim[0], final_ylim[0]), 
                                 final_xlim[1] - final_xlim[0], 
                                 final_ylim[1] - final_ylim[0], 
                                 facecolor=bg_list[0], edgecolor=border)
            ax.add_patch(rect)
        elif len(bg_list) > 1:
            if horizontal is None:
                # Vertical bands: xleft <- sort(unique(c(xlim[1], vertical, xlim[2])))
                v_vals = []
                if vertical is not None:
                    v_vals = [vertical] if not isinstance(vertical, (list, np.ndarray)) else list(vertical)
                xleft = np.sort(np.unique([final_xlim[0]] + v_vals + [final_xlim[1]]))
                
                bcol = np.resize(bg_list, len(xleft))
                for r in range(len(xleft) - 1):
                    rect = plt.Rectangle((xleft[r], final_ylim[0]), 
                                         xleft[r+1] - xleft[r], 
                                         final_ylim[1] - final_ylim[0], 
                                         facecolor=bcol[r], edgecolor='none')
                    ax.add_patch(rect)
            else:
                # Horizontal bands: ybot <- sort(unique(c(ylim[1], horizontal, ylim[2])))
                h_vals = []
                if horizontal is not None:
                    h_vals = [horizontal] if not isinstance(horizontal, (list, np.ndarray)) else list(horizontal)
                ybot = np.sort(np.unique([final_ylim[0]] + h_vals + [final_ylim[1]]))
                
                bcol = np.resize(bg_list, len(ybot))
                for r in range(len(ybot) - 1):
                    rect = plt.Rectangle((final_xlim[0], ybot[r]), 
                                         final_xlim[1] - final_xlim[0], 
                                         ybot[r+1] - ybot[r], 
                                         facecolor=bcol[r], edgecolor='none')
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
plt.plot(0, 0, 'o') # plot(0,0) creates a point and sets axes
# r2py:entity:backGround
backGround(bg="beige", fg="red", vertical=0, horizontal=0)

# --- Example 2 ---
plt.figure()
# r2py:entity:plot_1
plt.plot(0, 0, 'o')
# r2py:entity:backGround_1
backGround(bg=["yellow", "green"], fg="red", xlim=[-1, 1], ylim=[-1, 1], horizontal=np.arange(0, 1.1, 0.1))
# r2py:entity:backGround_2
backGround(bg=["yellow", "green"], fg="red", horizontal=np.arange(0, 1.1, 0.1))

plt.show()