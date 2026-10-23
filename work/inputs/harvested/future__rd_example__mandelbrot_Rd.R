# r2py crawler metadata
# package: future
# source_type: rd_example
# topic: mandelbrot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\future\help
# lines: 9

suppressPackageStartupMessages(library(future))
counts <- mandelbrot(xmid = -0.75, ymid = 0, side = 3)
str(counts)

plot(counts)



demo("mandelbrot", package = "future", ask = FALSE)