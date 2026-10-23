# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s61
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- date_build(2019:2026)
iso <- as_year_week_day(x, start = clock_weekdays$monday)
epi <- as_year_week_day(x, start = clock_weekdays$sunday)

data.frame(x = x, iso = iso, epi = epi)