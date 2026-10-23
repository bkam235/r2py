# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy_xyz.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 4

suppressPackageStartupMessages(library(broom))
A <- list(x = 1:5, y = 1:3, z = matrix(runif(5 * 3), nrow = 5))
image(A)
tidy(A)