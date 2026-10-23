# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: transform_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
hours <- seq(ISOdate(2000, 3, 20, tz = ""), by = "hour", length.out = 10)
t <- transform_time()
t$transform(hours)
t$inverse(t$transform(hours))
t$format(t$breaks(range(hours)))