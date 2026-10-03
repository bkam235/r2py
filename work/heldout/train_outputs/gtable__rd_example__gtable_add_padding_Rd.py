# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# R gtable/grid simulation using matplotlib
# gt <- gtable(unit(1, "null"), unit(1, "null"))
# gt <- gtable_add_grob(gt, rectGrob(gp = gpar(fill = "black")), 1, 1)
# r2py:entity:gt_1
def create_gt():
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig, ax

# plot(gt)
# r2py:entity:plot
gt_fig, gt_ax = create_gt()
plt.show()

# plot(cbind(gt, gt))
# r2py:entity:plot_1
fig_cbind, ax_cbind = plt.subplots()
ax_cbind.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
ax_cbind.add_patch(patches.Rectangle((1, 0), 1, 1, color='black'))
ax_cbind.set_xlim(0, 2)
ax_cbind.set_ylim(0, 1)
ax_cbind.axis('off')
plt.show()

# plot(rbind(gt, gt))
# r2py:entity:plot_2
fig_rbind, ax_rbind = plt.subplots()
ax_rbind.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
ax_rbind.add_patch(patches.Rectangle((0, 1), 1, 1, color='black'))
ax_rbind.set_xlim(0, 1)
ax_rbind.set_ylim(0, 2)
ax_rbind.axis('off')
plt.show()

# pad <- gtable_add_padding(gt, unit(1, "cm"))
# Approximating padding by expanding the axis limits
# r2py:entity:pad
def create_pad():
    fig, ax = plt.subplots()
    # Content is 1x1, padding is 1 unit around
    ax.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.axis('off')
    return fig, ax

# r2py:entity:plot_3
pad_fig, pad_ax = create_pad()
plt.show()

# plot(cbind(pad, pad))
# r2py:entity:plot_4
fig_pad_cbind, ax_pad_cbind = plt.subplots()
ax_pad_cbind.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
ax_pad_cbind.add_patch(patches.Rectangle((4, 1), 1, 1, color='black'))
ax_pad_cbind.set_xlim(0, 6)
ax_pad_cbind.set_ylim(0, 3)
ax_pad_cbind.axis('off')
plt.show()

# plot(rbind(pad, pad))
# r2py:entity:plot_5
fig_pad_rbind, ax_pad_rbind = plt.subplots()
ax_pad_rbind.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
ax_pad_rbind.add_patch(patches.Rectangle((1, 4), 1, 1, color='black'))
ax_pad_rbind.set_xlim(0, 3)
ax_pad_rbind.set_ylim(0, 6)
ax_pad_rbind.axis('off')
plt.show()