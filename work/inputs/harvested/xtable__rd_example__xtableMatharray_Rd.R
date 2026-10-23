# r2py crawler metadata
# package: xtable
# source_type: rd_example
# topic: xtableMatharray.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\help
# lines: 8

suppressPackageStartupMessages(library(xtable))
V <- matrix(c(1.140380e-03,  3.010497e-05,  7.334879e-05,
              3.010497e-05,  3.320683e-04, -5.284854e-05,
              7.334879e-05, -5.284854e-05,  3.520928e-04), nrow = 3)
mth <- xtableMatharray(V)
class(mth)
str(mth)
unclass(mth)