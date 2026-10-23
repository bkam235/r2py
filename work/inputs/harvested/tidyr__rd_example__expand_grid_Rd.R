# r2py crawler metadata
# package: tidyr
# source_type: rd_example
# topic: expand_grid.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\help
# lines: 12

suppressPackageStartupMessages(library(tidyr))
# Default behavior varies the first column "slowest"
expand_grid(x = 1:3, y = 1:2)

# Vary the first column "fastest", like `expand.grid()`
expand_grid(x = 1:3, y = 1:2, .vary = "fastest")

# Can also expand data frames
expand_grid(df = tibble(x = 1:2, y = c(2, 1)), z = 1:3)

# And matrices
expand_grid(x1 = matrix(1:4, nrow = 2), x2 = matrix(5:8, nrow = 2))