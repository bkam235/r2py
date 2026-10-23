# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: gtable_matrix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 17

suppressPackageStartupMessages(library(gtable))
library(grid)
a <- rectGrob(gp = gpar(fill = "red"))
b <- circleGrob()
c <- linesGrob()

row <- matrix(list(a, b, c), nrow = 1)
col <- matrix(list(a, b, c), ncol = 1)
mat <- matrix(list(a, b, c, nullGrob()), nrow = 2)

gtable_matrix("demo", row, unit(c(1, 1, 1), "null"), unit(1, "null"))
gtable_matrix("demo", col, unit(1, "null"), unit(c(1, 1, 1), "null"))
gtable_matrix("demo", mat, unit(c(1, 1), "null"), unit(c(1, 1), "null"))

# Can specify z ordering
z <- matrix(c(3, 1, 2, 4), nrow = 2)
gtable_matrix("demo", mat, unit(c(1, 1), "null"), unit(c(1, 1), "null"), z = z)