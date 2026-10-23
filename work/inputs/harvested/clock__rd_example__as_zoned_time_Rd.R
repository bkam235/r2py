# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_zoned_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")
as_zoned_time(x, "Europe/London")

y <- as_naive_time(year_month_day(2019, 2, 1))
as_zoned_time(y, zone = "America/New_York")