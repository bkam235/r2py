# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_time_build.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 16

suppressPackageStartupMessages(library(clock))
# The zone argument is required!
# clock always requires you to be explicit about your choice of `zone`.
try(date_time_build(2020))

date_time_build(2020, zone = "America/New_York")

# Nonexistent time due to daylight saving time gap from 01:59:59 -> 03:00:00
try(date_time_build(1970, 4, 26, 1:12, 30, zone = "America/New_York"))

# Resolve with a nonexistent time resolution strategy
date_time_build(
  1970, 4, 26, 1:12, 30,
  zone = "America/New_York",
  nonexistent = "roll-forward"
)