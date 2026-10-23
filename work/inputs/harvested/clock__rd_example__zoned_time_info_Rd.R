# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: zoned_time_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
x <- as_naive_time(x)
x <- as_zoned_time(x, "America/New_York")

# x[1] is in EST, x[2] is in EDT
x

info <- zoned_time_info(x)
info

# `end` can be used to iterate through daylight saving time transitions
zoned_time_info(info$end)