# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: gen_tbl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 14

suppressPackageStartupMessages(library(vroom))
# random 10 x 5 table with random column types
rand_tbl <- gen_tbl(10, 5)
rand_tbl

# all double 25 x 4 table
dbl_tbl <- gen_tbl(25, 4, col_types = "dddd")
dbl_tbl

# Use the dots in long form column types to change the random function and options
types <- rep(times = 4, list(col_double(f = stats::runif, min = -10, max = 25)))
types
dbl_tbl2 <- gen_tbl(25, 4, col_types = types)
dbl_tbl2