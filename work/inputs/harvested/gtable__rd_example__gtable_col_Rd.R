# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_col.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 9

suppressPackageStartupMessages(library(gtable))
library(grid)
a <- rectGrob(gp = gpar(fill = "red"))
b <- circleGrob()
c <- linesGrob()
gt <- gtable_col("demo", list(a, b, c))
gt
plot(gt)
gtable_show_layout(gt)