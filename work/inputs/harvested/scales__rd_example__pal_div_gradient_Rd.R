# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: pal_div_gradient.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 9

suppressPackageStartupMessages(library(scales))
x <- seq(-1, 1, length.out = 100)
r <- sqrt(outer(x^2, x^2, "+"))
image(r, col = pal_div_gradient()(seq(0, 1, length.out = 12)))
image(r, col = pal_div_gradient()(seq(0, 1, length.out = 30)))
image(r, col = pal_div_gradient()(seq(0, 1, length.out = 100)))

pal <- pal_div_gradient(low = "#2E6A70")
image(r, col = pal(seq(0, 1, length.out = 100)))