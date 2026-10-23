# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: str_wrap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 5

suppressPackageStartupMessages(library(xfun))
x = sample(c(letters, " "), 200, TRUE, c(rep(0.5/26, 26), 0.5))
x = rep(paste(x, collapse = ""), 2)
strwrap(x, width = 30)
xfun::str_wrap(x, width = 30)  # same length as x