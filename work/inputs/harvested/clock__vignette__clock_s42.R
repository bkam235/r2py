# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s42
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 10

suppressPackageStartupMessages(library(clock))
try({
x %>%
  set_day(31) %>%
  set_month(4)

x %>%
  set_day(31) %>%
  set_month(4, invalid = "previous")
})