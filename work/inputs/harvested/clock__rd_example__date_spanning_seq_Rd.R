# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_spanning_seq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 18

suppressPackageStartupMessages(library(clock))
x <- date_build(2020, c(1, 2, 1), c(10, 5, 12))
date_spanning_seq(x)

# Missing and infinite dates are removed before the sequence is generated
x <- c(x, NA, Inf, -Inf)
x

date_spanning_seq(x)

# For date-times, sequences are generated at second precision
x <- date_time_build(
  2020, 1, 2, 3, c(5, 4, 5), c(10, 48, 12),
  zone = "America/New_York"
)
x

date_spanning_seq(x)