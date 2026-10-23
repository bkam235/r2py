# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_weekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- as_naive_time(year_month_day(2019, 01, 05))

# This is a Saturday!
as_weekday(x)

# See the examples in `?weekday` for more usage.