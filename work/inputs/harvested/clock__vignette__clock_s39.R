# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s39
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 8

suppressPackageStartupMessages(library(clock))
try({
x <- date_time_build(1970, 04, 25, 02, 30, 00, zone = "America/New_York")
x

# Daylight saving time gap on the 26th between 01:59:59 -> 03:00:00
x %>% add_days(1)
})