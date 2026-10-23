# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- seq(date_build(2019, 1, 20), date_build(2019, 2, 5), by = 1)
x

# Grouping by 5 days of the current month
date_group(x, "day", n = 5)