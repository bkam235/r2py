# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s45
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- year_month_day(1980, 12, 14:16)
today <- year_month_day(2005, 12, 15)

# Note that the month and day of the month are taken into account!
# (Time of day would also be taken into account if there was any.)
calendar_count_between(x, today, "year")