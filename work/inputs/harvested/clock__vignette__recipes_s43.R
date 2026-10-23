# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s43
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, clock_months$july, 4)

yd <- as_year_day(x)
yd

get_day(yd)