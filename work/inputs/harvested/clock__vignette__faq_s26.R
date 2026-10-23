# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 4

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-01-01 23:00:00", "America/New_York")

as.Date(x, tz = date_time_zone(x))