# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_add_grob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 13

suppressPackageStartupMessages(library(gtable))
library(grid)

gt <- gtable(widths = unit(c(1, 1), 'null'), heights = unit(c(1, 1), 'null'))
pts <- pointsGrob(x = runif(5), y = runif(5))

# Add a grob to a single cell (top-right cell)
gt <- gtable_add_grob(gt, pts, t = 1, l = 2)

# Add a grob spanning multiple cells
gt <- gtable_add_grob(gt, pts, t = 1, l = 1, b = 2)

plot(gt)