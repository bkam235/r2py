# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: femmecol.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 5

suppressPackageStartupMessages(library(shape))
filled.contour(volcano, color = femmecol, asp = 1, main = "femmecol")
femmecol(10)
image(matrix(nrow = 1, ncol = 100, data = 1:100), 
      col = femmecol(100), main = "femmecol")