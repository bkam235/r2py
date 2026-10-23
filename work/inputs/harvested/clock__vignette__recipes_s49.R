# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s49
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 4

suppressPackageStartupMessages(library(clock))
x <- date_build(2019, 11, 28)

date_count_between(date_start(x, "year"), x, "week") + 1L