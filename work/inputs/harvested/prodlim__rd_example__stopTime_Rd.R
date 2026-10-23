# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: stopTime.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 20

suppressPackageStartupMessages(library(prodlim))
set.seed(29)
d <- SimSurv(10)
h <- with(d,Hist(time,status))
h
stopTime(h,8)
stopTime(h,5)

## works also with Surv objects
library(survival)
s <- with(d,Surv(time,status))
stopTime(s,5)

## competing risks
set.seed(29)
dr <- SimCompRisk(10)
hr <- with(dr,Hist(time,event))
hr
stopTime(hr,8)
stopTime(hr,5)