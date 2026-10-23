# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- c(
  "1970-10-25 01:30:00 EDT",
  "1970-10-25 01:30:00 EST"
)

date_time_parse_abbrev(x, "America/New_York")