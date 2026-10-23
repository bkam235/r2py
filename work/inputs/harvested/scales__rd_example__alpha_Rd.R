# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: alpha.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 5

suppressPackageStartupMessages(library(scales))
alpha("red", 0.1)
alpha(colours(), 0.5)
alpha("red", seq(0, 1, length.out = 10))
alpha(c("first" = "gold", "second" = "lightgray", "third" = "#cd7f32"), .5)