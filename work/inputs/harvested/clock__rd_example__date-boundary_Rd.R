# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
x <- date_build(2019:2021, 2:4, 3:5)
x

# Last day of the month
date_end(x, "month")

# Last day of the year
date_end(x, "year")

# First day of the year
date_start(x, "year")