# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s58
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- date_build(2019:2026)
y <- as_year_week_day(x, start = clock_weekdays$monday)

data.frame(x = x, y = y)