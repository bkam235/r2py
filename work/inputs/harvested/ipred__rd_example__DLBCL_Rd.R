# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: DLBCL.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 7

suppressPackageStartupMessages(library(ipred))
suppressWarnings(RNGversion("3.5.3"))
set.seed(290875)

data("DLBCL", package="ipred")
library("survival")
survfit(Surv(time, cens) ~ 1, data=DLBCL)