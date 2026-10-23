# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: duration_spanning_seq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- duration_days(c(1, 5, 2))
duration_spanning_seq(x)

# Missing values are removed before the sequence is created
x <- vctrs::vec_c(NA, x, NA)
duration_spanning_seq(x)