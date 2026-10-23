# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: jackknife.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 17

suppressPackageStartupMessages(library(prodlim))
## pseudo-values for survival models

d=SimSurv(20) 
f=prodlim(Hist(time,status)~1,data=d) 
jackknife(f,times=c(3,5))

## in some situations it may be useful to attach the
## the event time history to the result
jackknife(f,times=c(3,5),keepResponse=TRUE)

# pseudo-values for competing risk models
set.seed(15)
d=SimCompRisk(15) 
f=prodlim(Hist(time,event)~1,data=d) 
jackknife(f,times=c(3,5),cause=1)
jackknife(f,times=c(1,3,5),cause=2)