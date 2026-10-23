# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 7

suppressPackageStartupMessages(library(clock))
from <- as_naive_time(year_month_day(2019, 1, 1))
to <- as_naive_time(year_month_day(2019, 12, 31))

x <- seq(from, to, by = duration_days(20))

x