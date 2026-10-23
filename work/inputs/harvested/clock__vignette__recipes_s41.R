# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s41
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 4

suppressPackageStartupMessages(library(clock))
x <- seq(as.Date("2019-01-01"), as.Date("2019-12-31"), by = 20)

date_floor(x, "day", n = 60)