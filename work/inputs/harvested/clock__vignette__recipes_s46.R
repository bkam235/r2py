# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s46
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- date_build(1980, 12, 14:16)
today <- date_build(2005, 12, 15)

date_count_between(x, today, "year")