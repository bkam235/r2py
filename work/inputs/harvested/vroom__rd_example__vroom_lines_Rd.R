# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: vroom_lines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 7

suppressPackageStartupMessages(library(vroom))
lines <- vroom_lines(vroom_example("mtcars.csv"))

length(lines)
head(lines, n = 2)
tail(lines, n = 2)
sample(lines, size = 2)