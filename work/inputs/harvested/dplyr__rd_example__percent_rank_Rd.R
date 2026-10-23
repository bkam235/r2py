# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: percent_rank.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 11

suppressPackageStartupMessages(library(dplyr))
x <- c(5, 1, 3, 2, 2)

cume_dist(x)
percent_rank(x)

# You can understand what's going on by computing it by hand
sapply(x, function(xi) sum(x <= xi) / length(x))
sapply(x, function(xi) sum(x < xi)  / (length(x) - 1))
# The real computations are a little more complex in order to
# correctly deal with missing values