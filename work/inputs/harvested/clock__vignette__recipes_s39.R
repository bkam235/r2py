# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s39
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- seq(as_naive_time(year_month_day(2019, 1, 1)), by = 3, length.out = 10)
x

thursdays <- time_point_floor(x, "day", n = 14)
thursdays

as_weekday(thursdays)