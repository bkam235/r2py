# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-and-date-time-rounding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 9

suppressPackageStartupMessages(library(clock))
# See the type specific documentation for more examples

x <- as.Date("2019-03-31") + 0:5
x

# Flooring by 2 days, note that this is not tied to the current month,
# and instead counts from the specified `origin`.
date_floor(x, "day", n = 2)