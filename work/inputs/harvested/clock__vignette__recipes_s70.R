# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s70
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 4

suppressPackageStartupMessages(library(clock))
x <- date_time_parse("2019-01-01 00:00:00", zone = "America/New_York")

date_time_info(x)