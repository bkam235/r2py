# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_show_layout.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 4

suppressPackageStartupMessages(library(gtable))
gt <- gtable(widths = grid::unit(c(1, 0.5, 2), c("null", "cm", "null")),
             heights = grid::unit(c(0.2, 1, 3), c("inch", "null", "cm")))
gtable_show_layout(gt)