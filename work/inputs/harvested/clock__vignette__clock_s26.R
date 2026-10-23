# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s26
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 9

suppressPackageStartupMessages(library(clock))
x <- seq(
  date_time_build(2019, 1, 1, 1, 55, zone = "UTC"),
  date_time_build(2019, 1, 1, 2, 15, zone = "UTC"),
  by = 120
)
x

date_group(x, "minute", n = 5)