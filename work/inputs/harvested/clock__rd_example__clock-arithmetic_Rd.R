# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: clock-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 4

suppressPackageStartupMessages(library(clock))
# See each sub-page for more specific examples
x <- year_month_day(2019, 2, 1)
add_months(x, 1)