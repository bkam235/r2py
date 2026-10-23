# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-and-date-time-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# See type specific documentation for more examples

x <- date_build(2019, 2:4)

date_end(x, "month")

x <- date_time_build(2019, 2:4, 3:5, 4, 5, zone = "America/New_York")

# Note that the hour, minute, and second components are also adjusted
date_end(x, "month")