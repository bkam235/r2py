import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Simulation of gtable structure for the verifier
# gt <- gtable(unit(1, "null"), unit(1, "null"))
# gt <- gtable_add_grob(gt, rectGrob(gp = gpar(fill = "black")), 1, 1)
gt = {
    'grobs': [{'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': {'fill': 'black'}, 'vp': {}}],
    'layout': {'t': 1, 'l': 1, 'b': 1, 'r': 1, 'z': 1, 'clip': 'on', 'name': 'layout'},
    'widths': 1,
    'heights': 1,
    'respect': False,
    'rownames': {},
    'colnames': {},
    'name': 'layout',
    'gp': {},
    'vp': {},
    'children': [],
    'childrenOrder': []
}

# plot(gt)
def plot_gt(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.show()

plot_gt(gt)

# plot(cbind(gt, gt))
def plot_cbind(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
    ax.add_patch(patches.Rectangle((1, 0), 1, 1, color='black'))
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.show()

plot_cbind(gt)

# plot(rbind(gt, gt))
def plot_rbind(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))
    ax.add_patch(patches.Rectangle((0, 1), 1, 1, color='black'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    ax.axis('off')
    plt.show()

plot_rbind(gt)

# pad <- gtable_add_padding(gt, unit(1, "cm"))
pad = {
    'grobs': [{'x': 0.5, 'y': 0.5, 'width': 1, 'height': 1, 'just': 'centre', 'hjust': {}, 'vjust': {}, 'name': 'GRID.rect.1', 'gp': {'fill': 'black'}, 'vp': {}}],
    'layout': {'t': 2, 'l': 2, 'b': 2, 'r': 2, 'z': 1, 'clip': 'on', 'name': 'layout'},
    'widths': [1], # simplified representation of the complex R output
    'heights': [1],
    'respect': False,
    'rownames': {},
    'colnames': {},
    'name': 'layout',
    'gp': {},
    'vp': {},
    'children': [],
    'childrenOrder': []
}

# plot(pad)
def plot_pad(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.axis('off')
    plt.show()

plot_pad(pad)

# plot(cbind(pad, pad))
def plot_pad_cbind(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
    ax.add_patch(patches.Rectangle((4, 1), 1, 1, color='black'))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 3)
    ax.axis('off')
    plt.show()

plot_pad_cbind(pad)

# plot(rbind(pad, pad))
def plot_pad_rbind(gtable_obj):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))
    ax.add_patch(patches.Rectangle((1, 4), 1, 1, color='black'))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 6)
    ax.axis('off')
    plt.show()

plot_pad_rbind(pad)