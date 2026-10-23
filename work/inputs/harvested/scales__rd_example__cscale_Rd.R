# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: cscale.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 10

suppressPackageStartupMessages(library(scales))
with(mtcars, plot(disp, mpg, cex = cscale(hp, pal_rescale())))
with(mtcars, plot(disp, mpg, cex = cscale(hp, pal_rescale(),
  trans = transform_sqrt()
)))
with(mtcars, plot(disp, mpg, cex = cscale(hp, pal_area())))
with(mtcars, plot(disp, mpg,
  pch = 20, cex = 5,
  col = cscale(hp, pal_seq_gradient("grey80", "black"))
))