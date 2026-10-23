# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 11

suppressPackageStartupMessages(library(clock))
days <- as_naive_time(year_month_day(2019, c(1, 2), 1))

# A Tuesday and a Friday
as_weekday(days)

monday <- weekday(clock_weekdays$monday)

time_point_shift(days, monday)

as_weekday(time_point_shift(days, monday))