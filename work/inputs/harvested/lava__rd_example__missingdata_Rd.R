# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: missingdata.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
data(missingdata)
e0 <- estimate(lvm(c(y1,y2)~b*x,y1~~y2),missingdata[[1]]) ## No missing
e1 <- estimate(lvm(c(y1,y2)~b*x,y1~~y2),missingdata[[2]]) ## CC (MCAR)
e2 <- estimate(lvm(c(y1,y2)~b*x,y1~~y2),missingdata[[2]],missing=TRUE) ## MCAR
e3 <- estimate(lvm(c(y1,y2)~b*x,y1~~y2),missingdata[[3]]) ## CC (MAR)
e4 <- estimate(lvm(c(y1,y2)~b*x,y1~~y2),missingdata[[3]],missing=TRUE) ## MAR