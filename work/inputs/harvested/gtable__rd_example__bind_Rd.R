# r2py crawler metadata
# package: gtable
# source_type: rd_example
# topic: bind.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\gtable\help
# lines: 24

suppressPackageStartupMessages(library(gtable))
library(grid)
a <- rectGrob(gp = gpar(fill = "red"))
b <- circleGrob()
c <- linesGrob()

row <- matrix(list(a, b), nrow = 1)
col <- matrix(list(a, b), ncol = 1)
mat <- matrix(list(a, b, c, nullGrob()), nrow = 2)

row_gt <- gtable_matrix("demo", row, unit(c(1, 1), "null"), unit(1, "null"))
col_gt <- gtable_matrix("demo", col, unit(1, "null"), unit(c(1, 1), "null"))
mat_gt <- gtable_matrix("demo", mat, unit(c(1, 1), "null"), unit(c(1, 1), "null"))

# cbind
c_binded <- cbind(mat_gt, col_gt, size = "first")
plot(c_binded)

# rbind
r_binded <- rbind(mat_gt, row_gt, size = "last")
plot(r_binded)

# Dimensions must match along bind direction
try(cbind(mat_gt, row_gt))