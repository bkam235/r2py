# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: as.data.table.prodlim.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 6

suppressPackageStartupMessages(library(prodlim))
library(data.table)
set.seed(8)
d <- SimCompRisk(17)
fit <- prodlim(Hist(time,event)~X1,data=d)
as.data.table(fit)