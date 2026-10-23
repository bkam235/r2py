# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 8

suppressPackageStartupMessages(library(clock))
before <- date_time_parse("2020-11-01 00:59:59", "America/New_York")

# First 1 o'clock
before + 1

# Second 1 o'clock
before + 1 + 3600