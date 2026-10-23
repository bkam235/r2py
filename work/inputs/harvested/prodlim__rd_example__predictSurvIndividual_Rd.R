# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: predictSurvIndividual.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 4

suppressPackageStartupMessages(library(prodlim))
SurvFrame <- data.frame(time=1:10,status=rbinom(10,1,.5))
 x <- prodlim(formula=Hist(time=time,status!=0)~1,data=SurvFrame)
 predictSurvIndividual(x,lag=1)