# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- "2020-01-01T01:02:03-0500"

date_time_parse_RFC_3339(x, offset = "%z")

x <- "2020-01-01T01:02:03-05:00"

date_time_parse_RFC_3339(x, offset = "%Ez")