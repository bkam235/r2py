# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: try_silent.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 3

library(xfun)
z = try_silent(stop("Wrong!"))
inherits(z, "try-error")