# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_add_space.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 19

suppressPackageStartupMessages(library(gtable))
library(grid)

rect <- rectGrob()
rect_mat <- matrix(rep(list(rect), 9), nrow = 3)

gt <- gtable_matrix("rects", rect_mat, widths = unit(rep(1, 3), "null"),
                    heights = unit(rep(1, 3), "null"))

plot(gt)

# Add spacing between the grobs
# same height between all rows
gt <- gtable_add_row_space(gt, unit(0.5, "cm"))

# Different width between the columns
gt <- gtable_add_col_space(gt, unit(c(0.5, 1), "cm"))

plot(gt)