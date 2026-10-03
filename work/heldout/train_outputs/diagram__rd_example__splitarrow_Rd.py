# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__splitarrow_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__splitarrow_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# r2py:entity:openplotmat
def openplotmat(asp=None, main=None):
    plt.figure()
    if main:
        plt.title(main)
    plt.axis('off')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal')

# r2py:entity:pos
def coordinates(pos=None, mx=0, my=0, N=None, hor=True, relsize=1):
    if pos is None:
        if N is None:
            raise ValueError("Either pos or N must be provided")
        alpha0 = np.pi / 2
        alpha = alpha0 - (np.arange(1, N + 1)) * 2 * np.pi / N
        xl = np.cos(alpha) * 0.4 + 0.5
        yl = np.sin(alpha) * 0.4 + 0.5
        elpos = np.column_stack([xl, yl])
    else:
        nr = len(pos)
        if N is None or len(pos) != N * 2:
            dx_max = 1.0 / max(pos)
            dy = 1.0 / nr
            elpos = []
            ypos = np.linspace(dy * 0.5, nr * dy, nr)[::-1]
            for i in range(nr):
                count = pos[i]
                dx = 1.0 / count
                # R: xpos <- dx * 0.5 + seq(0, pos[i] * dx, dx)
                # seq(0, pos[i]*dx, dx) produces pos[i]+1 elements: 0, dx, ..., pos[i]*dx
                # However, the loop 'for (j in 1:pos[i])' only takes the first pos[i] elements.
                xpos = dx * 0.5 + np.arange(count) * dx
                for j in range(count):
                    elpos.append([xpos[j], ypos[i]])
            elpos = np.array(elpos)
            if not hor:
                # Rotate 90 deg around (0.5, 0.5)
                # x' = -(y-0.5) + 0.5, y' = (x-0.5) + 0.5
                rotated = np.zeros_like(elpos)
                rotated[:, 0] = -(elpos[:, 1] - 0.5) + 0.5
                rotated[:, 1] = (elpos[:, 0] - 0.5) + 0.5
                elpos = rotated
        else:
            elpos = np.array(pos).reshape(-1, 2)

    # Handle relsize (simplified as usr is usually [0,1,0,1] for openplotmat)
    # elpos is already relative to [0,1] range.
    return elpos + np.array([mx, my])

# r2py:entity:splitarrow
def straightarrow(from_val, to_val, lwd=2, lty=1, lcol="black", arr_col="black", arr_pos=0.5, endhead=False, segment=(0, 1)):
    f = np.array(from_val)
    t = np.array(to_val)
    
    # segment handling
    start = segment[0] * t + (1 - segment[0]) * f if segment[0] != 0 else f
    end = segment[1] * t + (1 - segment[1]) * f if segment[1] != 1 else t
    
    # endhead
    meanpi = arr_pos * end + (1 - arr_pos) * start
    if endhead:
        end = meanpi
        
    plt.plot([start[0], end[0]], [start[1], end[1]], color=lcol, linewidth=lwd, zorder=1)
    
    # Arrowhead logic from R:
    # mid2 <- (arr.pos - 0.01) * to + (1 - arr.pos + 0.01) * from
    # mid1 <- (arr.pos) * to + (1 - arr.pos) * from
    # Arrows(mid2, mid1)
    m2 = (arr_pos - 0.01) * t + (1 - arr_pos + 0.01) * f
    m1 = arr_pos * t + (1 - arr_pos) * f
    
    # Draw arrow head using annotate
    plt.annotate('', xy=m1, xytext=m2,
                 arrowprops=dict(arrowstyle='->', color=arr_col, lw=lwd, mutation_scale=10), zorder=2)
    return m1

def splitarrow(from_val, to_val, lwd=2, lty=1, lcol="black", arr_col="black", arr_side=2, arr_pos=0.5, centre=None, dd=0.5):
    From = np.atleast_2d(from_val)
    To = np.atleast_2d(to_val)
    
    meanFrom = np.mean(From, axis=0)
    meanTo = np.mean(To, axis=0)
    
    if centre is None:
        centre = meanFrom + dd * (meanTo - meanFrom)
    else:
        centre = np.array(centre)
        
    def sarr(p1, p2, drawarr):
        if drawarr:
            straightarrow(p1, p2, lwd=lwd, lty=lty, lcol=lcol, arr_col=arr_col, arr_pos=arr_pos)
        else:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=lcol, linewidth=lwd, zorder=1)

    # arr_side is used as a vector/set for %in%
    side_set = set(arr_side) if isinstance(arr_side, (list, tuple, np.ndarray)) else {arr_side}
    
    for i in range(From.shape[0]):
        sarr(From[i], centre, 1 in side_set)
    for i in range(To.shape[0]):
        sarr(centre, To[i], 2 in side_set)

# r2py:entity:textrect
def textrect(mid, radx, lab="", cex=2, rady=None, lwd=1, shadow_size=0.01, adj=(0.5, 0.5), box_col="white", lcol="black", shadow_col="grey", angle=0):
    if rady is None:
        rady = radx * len(lab) if isinstance(lab, (list, tuple, np.ndarray)) else radx * 1 # R: radx * length(lab)
    
    mid = np.array(mid)
    pin_ratio = 1.0 # simplified
    dd = np.array([shadow_size, -shadow_size * pin_ratio])
    
    xy = np.array([
        [mid[0] - radx, mid[1] - rady],
        [mid[0] - radx, mid[1] + rady],
        [mid[0] + radx, mid[1] + rady],
        [mid[0] + radx, mid[1] - rady]
    ])
    
    if shadow_size > 0:
        xyshad = xy + dd
        poly_shad = patches.Polygon(xyshad, closed=True, facecolor=shadow_col, edgecolor='none', zorder=0)
        plt.gca().add_patch(poly_shad)
        
    poly_box = patches.Polygon(xy, closed=True, facecolor=box_col, edgecolor=lcol, linewidth=lwd, zorder=1)
    plt.gca().add_patch(poly_box)
    
    # textplain
    if not isinstance(lab, (list, tuple, np.ndarray)):
        plt.text(mid[0], mid[1], str(lab), fontsize=cex, ha='center', va='center', zorder=2)
    else:
        # Handle multiple labels
        y1 = mid[1] + rady
        ddy = 2 * rady / (len(lab) + 1)
        for i, l in enumerate(lab):
            plt.text(mid[0], y1 - ddy * (i + 1), str(l), fontsize=cex, ha='center', va='center', zorder=2)

# --- Execution ---

# r2py:entity:openplotmat
openplotmat(main="splitarrow")
# r2py:entity:pos
pos = coordinates(pos=[1, 2, 2, 4, 1])
# r2py:entity:splitarrow
splitarrow(from_val=pos[0], to_val=pos[1:10], arr_side=1, centre=[0.5, 0.625])
# r2py:entity:textrect
for i in range(1, 11):
    textrect(pos[i-1], radx=0.05, lab=i, cex=2)
plt.show()

# r2py:entity:openplotmat_1
openplotmat(main="splitarrow")
# r2py:entity:pos_1
pos = coordinates(pos=[1, 3])
# r2py:entity:splitarrow_1
splitarrow(from_val=pos[0], to_val=pos[1:4], arr_side=1)
# r2py:entity:splitarrow_2
splitarrow(from_val=pos[0], to_val=pos[1:4], arr_side=2)
# r2py:entity:textrect_1
for i in range(1, 5):
    textrect(pos[i-1], radx=0.05, lab=i, cex=2)
plt.show()

# r2py:entity:openplotmat_2
openplotmat(main="splitarrow")
# r2py:entity:pos_2
pos_circ = coordinates(N=6)
# r2py:entity:pos_3
pos = np.vstack([np.array([0.5, 0.5]), pos_circ])
# r2py:entity:splitarrow_3
splitarrow(from_val=pos[0], to_val=pos[1:7], arr_side=2)
# r2py:entity:textrect_2
for i in range(1, 8):
    textrect(pos[i-1], radx=0.05, lab=i, cex=2)
plt.show()