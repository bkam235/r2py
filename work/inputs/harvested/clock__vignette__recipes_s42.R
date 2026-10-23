# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s42
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- seq(as.Date("2019-01-01"), by = 3, length.out = 10)

origin <- as.Date("2018-12-31")

date_floor(x, "week", n = 2, origin = origin)