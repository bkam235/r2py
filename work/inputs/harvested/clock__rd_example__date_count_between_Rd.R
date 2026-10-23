# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_count_between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# See method specific documentation for more examples

start <- date_parse("2000-05-05")
end <- date_parse(c("2020-05-04", "2020-05-06"))

# Age in years
date_count_between(start, end, "year")

# Number of "whole" months between these dates
date_count_between(start, end, "month")