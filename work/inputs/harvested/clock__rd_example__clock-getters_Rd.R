# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: clock-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1:3, 5:7, 1, 20, 30)
get_month(x)
get_day(x)
get_second(x)