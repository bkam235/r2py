# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: followup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 9

suppressPackageStartupMessages(library(prodlim))
set.seed(8)
d <- SimCompRisk(117)

# overall
followup(Hist(time,event)~1,data=d)

# in strata defined by variable X1 
followup(Hist(time,event)~X1,data=d)