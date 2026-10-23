# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: sizeGrowthRatio.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 6

suppressPackageStartupMessages(library(shiny))
f <- sizeGrowthRatio(500, 500, 1.25)
f(c(400, 400))
f(c(500, 500))
f(c(530, 550))
f(c(625, 700))