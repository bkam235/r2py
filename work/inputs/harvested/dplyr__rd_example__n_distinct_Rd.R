# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: n_distinct.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 16

suppressPackageStartupMessages(library(dplyr))
x <- c(1, 1, 2, 2, 2)
n_distinct(x)

y <- c(3, 3, NA, 3, 3)
n_distinct(y)
n_distinct(y, na.rm = TRUE)

# Pairs (1, 3), (2, 3), and (2, NA) are distinct
n_distinct(x, y)

# (2, NA) is dropped, leaving 2 distinct combinations
n_distinct(x, y, na.rm = TRUE)

# Also works with data frames
n_distinct(data.frame(x, y))