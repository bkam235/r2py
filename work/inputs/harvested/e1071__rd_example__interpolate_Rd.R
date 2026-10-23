# r2py crawler metadata
# package: e1071
# source_type: rd_example
# topic: interpolate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\e1071\help
# lines: 6

suppressPackageStartupMessages(library(e1071))
x <- seq(0,3,0.2)
z <- outer(x,x, function(x,y) sin(x*y))
dimnames(z) <- list(x,x)
sin(1.1*2.1)
interpolate(c(1.1, 2.1),z)