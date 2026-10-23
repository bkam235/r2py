# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 15

suppressPackageStartupMessages(library(clock))
x <- date_time_build(2019:2021, 2:4, 3:5, 4, 5, 6, zone = "America/New_York")
x

# Last moment of the month
date_end(x, "month")

# Notice that this is different from just setting the day to `"last"`
set_day(x, "last")

# Last moment of the year
date_end(x, "year")

# First moment of the hour
date_start(x, "hour")