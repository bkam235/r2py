# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: shadepalette.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 4

suppressPackageStartupMessages(library(shape))
shadepalette(n = 10, "white", "black")
image(matrix(nrow = 1, ncol = 100, data = 1:100),
      col = shadepalette(100, "red", "blue"), main = "shadepalette")