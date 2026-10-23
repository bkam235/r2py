# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 5

suppressPackageStartupMessages(library(clock))
zone <- "America/New_York"

date_time_build(2019:2021, 3, 8, 2, 30, zone = zone, nonexistent = "roll-forward")
date_time_build(2019:2021, 3, 8, 2, 30, zone = zone, nonexistent = "roll-backward")