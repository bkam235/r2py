# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: sindex.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 8

suppressPackageStartupMessages(library(prodlim))
test <- list(time = c(1, 1,5,5,2,7,9),
		status = c(1,0,1,0,1,1,0))
fit <- prodlim(Hist(time,status)~1,data=test)
jtimes <- fit$time
etimes <- c(0,.5,2,8,10)
fit$surv
c(1,fit$surv)[1+sindex(jtimes,etimes)]