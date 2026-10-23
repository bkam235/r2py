# r2py crawler metadata
# package: glmnet
# source_type: rd_example
# topic: stratifySurv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\help
# lines: 4

suppressPackageStartupMessages(library(glmnet))
y <- survival::Surv(1:10, rep(0:1, length.out = 10))
strata <- rep(1:3, length.out = 10)
y2 <- stratifySurv(y, strata)  # returns stratifySurv object