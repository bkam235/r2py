# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: transform_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
years <- seq(as.Date("1910/1/1"), as.Date("1999/1/1"), "years")
t <- transform_date()
t$transform(years)
t$inverse(t$transform(years))
t$format(t$breaks(range(years)))