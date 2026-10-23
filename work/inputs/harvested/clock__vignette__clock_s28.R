# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- seq(date_build(1970, 01, 01), date_build(1970, 05, 10), by = 20)

date_floor(x, "day", n = 60)
date_ceiling(x, "day", n = 60)