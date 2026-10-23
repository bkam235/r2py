# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 5

suppressPackageStartupMessages(library(clock))
from <- as_naive_time(year_month_day(2019, 1, 1, 2, 30, 00))
to <- as_naive_time(year_month_day(2019, 1, 1, 12, 30, 00))

seq(from, to, by = duration_minutes(90))