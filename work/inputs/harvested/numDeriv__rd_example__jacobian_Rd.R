# r2py crawler metadata
# package: numDeriv
# source_type: rd_example
# topic: jacobian.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\numDeriv\help
# lines: 5

suppressPackageStartupMessages(library(numDeriv))
func2 <- function(x) c(sin(x), cos(x))
   x <- (0:1)*2*pi
   jacobian(func2, x)
   jacobian(func2, x, "complex")