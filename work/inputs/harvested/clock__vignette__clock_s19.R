# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 4

suppressPackageStartupMessages(library(clock))
x <- "2020-01-01 01:02:03 EST"

date_time_parse_abbrev(x, "America/New_York")