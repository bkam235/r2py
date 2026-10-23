import pandas as pd
from plotnine import *

# Data preparation
# expand.grid(X1 = 1:10, X2 = 1:10) in R: X1 changes fastest
# To match this in Python, X2 should be the outer loop
# r2py:entity:df
data = []
for x2 in range(1, 11):
    for x1 in range(1, 11):
        data.append({'X1': x1, 'X2': x2})
df = pd.DataFrame(data)

# r2py:entity:df$value
df['value'] = df['X1'] * df['X2']

# r2py:entity:geom_tile
p1 = ggplot(df, aes('X1', 'X2')) + geom_tile(aes(fill='value'))
# r2py:entity:geom_point
p2 = p1 + geom_point(aes(size='value'))

# Basic form
# r2py:entity:scale_fill_continuous
p1_basic1 = p1 + scale_fill_continuous(guide='colourbar')
# r2py:entity:scale_fill_continuous_1
p1_basic2 = p1 + scale_fill_continuous(guide=guide_colourbar())
# r2py:entity:guides
p1_basic3 = p1 + guides(fill=guide_colourbar())

# Control styles

# bar size
# r2py:entity:guides_1
p1_style1 = p1 + guides(fill=guide_colourbar(theme=theme(
    legend_key_width=0.5, 
    legend_key_height=10
)))

# no label
# r2py:entity:guides_2
p1_style2 = p1 + guides(fill=guide_colourbar(theme=theme(
    legend_text=element_blank()
)))

# no tick marks
# r2py:entity:guides_3
p1_style3 = p1 + guides(fill=guide_colourbar(theme=theme(
    legend_ticks=element_blank()
)))

# label position
# r2py:entity:guides_4
p1_style4 = p1 + guides(fill=guide_colourbar(theme=theme(
    legend_text_position='left'
)))

# label theme
# r2py:entity:guides_5
p1_style5 = p1 + guides(fill=guide_colourbar(theme=theme(
    legend_text=element_text(colour='blue', angle=0)
)))

# small number of bins
# r2py:entity:guides_6
p1_style6 = p1 + guides(fill=guide_colourbar(nbin=3))

# large number of bins
# r2py:entity:guides_7
p1_style7 = p1 + guides(fill=guide_colourbar(nbin=100))

# make top- and bottom-most ticks invisible
# r2py:entity:scale_fill_continuous_2
p1_style8 = p1 + scale_fill_continuous(
    limits=[0, 20], 
    breaks=[0, 5, 10, 15, 20],
    guide=guide_colourbar(nbin=100, draw_ulim=False, draw_llim=False)
)

# guides can be controlled independently
# r2py:entity:scale_size
p2_style1 = p2 + scale_fill_continuous(guide='colourbar') + scale_size(guide='legend')
# r2py:entity:guides_8
p2_style2 = p2 + guides(fill='colourbar', size='legend')

# r2py:entity:scale_fill_continuous_4
p2_style3 = (p2 + scale_fill_continuous(guide=guide_colourbar(theme=theme(
    legend_direction='horizontal'
# r2py:entity:scale_size_1
))) + scale_size(guide=guide_legend(theme=theme(
    legend_direction='vertical'
))))