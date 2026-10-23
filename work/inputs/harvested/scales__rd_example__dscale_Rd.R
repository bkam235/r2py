# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: dscale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 5

suppressPackageStartupMessages(library(scales))
with(mtcars, plot(disp, mpg,
  pch = 20, cex = 3,
  col = dscale(factor(cyl), pal_brewer())
))