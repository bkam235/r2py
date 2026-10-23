# r2py crawler metadata
# package: xfun
# source_type: rd_example
# topic: decimal_dot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xfun\help
# lines: 7

suppressPackageStartupMessages(library(xfun))
opts = options(OutDec = ",")
as.character(1.234)  # using ',' as the decimal separator
print(1.234)  # same
xfun::decimal_dot(as.character(1.234))  # using dot
xfun::decimal_dot(print(1.234))  # using dot
options(opts)