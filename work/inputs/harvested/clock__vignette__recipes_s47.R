# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s47
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 11, 28)

# lubridate::week(as.Date(x))
# [1] 48

x_start <- calendar_start(x, "year")
x_start

time_point_count_between(
  as_naive_time(x_start),
  as_naive_time(x),
  "week"
) + 1L