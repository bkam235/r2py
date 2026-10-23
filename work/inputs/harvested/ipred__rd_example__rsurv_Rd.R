# r2py crawler metadata
# package: ipred
# source_type: rd_example
# topic: rsurv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ipred\help
# lines: 5

suppressPackageStartupMessages(library(ipred))
library("survival")
# 3*X1 + X2
simdat <- rsurv(500, model="C")
coxph(Surv(time, cens) ~ ., data=simdat)