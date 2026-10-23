# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: predict.prodlim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 21

suppressPackageStartupMessages(library(prodlim))
dat <- SimSurv(400)
fit <- prodlim(Hist(time,status)~1,data=dat)

## predict the survival probs at selected times 
predict(fit,times=c(3,5,10))

## NA is returned when the time point is beyond the
## range of definition of the Kaplan-Meier estimator:
predict(fit,times=c(-1,0,10,100,1000,10000))

## when there are strata, newdata is required 
## or neighborhoods (i.e. overlapping strata)
mfit <- prodlim(Hist(time,status)~X1+X2,data=dat)
predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,])

## this can be requested in matrix form
predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix")

## and even transposed
predict(mfit,times=c(-1,0,10,100,1000,10000),newdata=dat[18:21,],mode="matrix",bytime=TRUE)