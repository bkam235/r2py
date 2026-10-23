# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.dist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 7

suppressPackageStartupMessages(library(broom))
cars_dist <- dist(t(mtcars[, 1:4]))
cars_dist

tidy(cars_dist)
tidy(cars_dist, upper = TRUE)
tidy(cars_dist, diagonal = TRUE)