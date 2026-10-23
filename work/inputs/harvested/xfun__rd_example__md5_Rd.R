# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: md5.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 10

suppressPackageStartupMessages(library(xfun))
x1 = 1
x2 = 1:10
x3 = seq(1, 10)
x4 = iris
x5 = paste
(m = xfun::md5(x1, x2, x3, x4, x5))
stopifnot(m[2] == m[3])  # x2 and x3 should be identical

xfun::md5(x1 = x1, x2 = x2)  # named arguments