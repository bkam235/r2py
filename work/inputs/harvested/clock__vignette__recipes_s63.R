# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: recipes_s63
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\recipes.R
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- "2020-10-25 01:30:00 IST"

zoned_time_parse_abbrev(x, "Asia/Kolkata")
zoned_time_parse_abbrev(x, "Asia/Jerusalem")