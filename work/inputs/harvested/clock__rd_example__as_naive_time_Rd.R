# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_naive_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")
as_naive_time(x)

ym <- year_month_day(2019, 02)

# A minimum of day precision is required
try(as_naive_time(ym))

ymd <- set_day(ym, 10)
as_naive_time(ymd)