# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: greycol.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 5

suppressPackageStartupMessages(library(shape))
filled.contour(volcano, color = graycol, asp = 1, main = "greycol,graycol")
graycol(10)
image(
      matrix(nrow = 1, ncol = 100, data = 1:100),
      col = graycol(100),
      main = "greycol,graycol"
)
