# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_time_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- date_time_build(
  2021, 03, 14, c(01, 03), c(59, 00), c(59, 00),
  zone = "America/New_York"
)

# x[1] is in EST, x[2] is in EDT
x

info <- date_time_info(x)
info

# `end` can be used to iterate through daylight saving time transitions
date_time_info(info$end)