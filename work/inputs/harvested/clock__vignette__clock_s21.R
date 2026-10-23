# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- "1970-01-01 02:30:30 IST"

# IST = India Standard Time
date_time_parse_abbrev(x, "Asia/Kolkata")

# IST = Israel Standard Time
date_time_parse_abbrev(x, "Asia/Jerusalem")