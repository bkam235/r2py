# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s68
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 10

suppressPackageStartupMessages(library(clock))
x <- zoned_time_parse_complete("2019-01-01T00:00:00-05:00[America/New_York]")

info <- zoned_time_info(x)

# Beginning of the current DST range
info$begin

# Beginning of the next DST range
info$end